import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from scripts.audit import validate, main, DIMENSIONS
from test_audit import base

class BoundaryTests(unittest.TestCase):
    def test_na_excluded_from_coverage(self):
        d = base()
        d['weights'].update(seo=0, ux=30)
        d['scores']['seo'] = {'not_applicable': True, 'reason': 'Private tool'}
        d['gates']['technical_seo'] = 'not_applicable'
        errors, r = validate(d)
        self.assertEqual(errors, [])
        self.assertEqual(r['coverage'], 'full')
        self.assertEqual(r['weighted_score'], 80)
        self.assertTrue(r['acceptance_eligible'])

    def test_na_requires_reason_zero_weight_and_no_score(self):
        for entry in ({'not_applicable': True}, {'not_applicable': True, 'reason': 'Private', 'score': 80}):
            d = base()
            d['scores']['seo'] = entry
            self.assertTrue(validate(d)[0])

    def test_zero_weight_is_not_implicitly_na(self):
        d = base()
        d['weights'].update(seo=0, ux=30)
        del d['scores']['seo']
        self.assertEqual(validate(d)[1]['coverage'], 'partial')

    def test_plan_cannot_be_accepted(self):
        d = base()
        d['mode'] = 'plan'
        r = validate(d)[1]
        self.assertFalse(r['acceptance_eligible'])
        self.assertEqual(r['assessment_status'], 'plan_complete')

    def test_all_na_cannot_pass(self):
        d = base()
        d['scores'] = {k: {'not_applicable': True, 'reason': 'N/A'} for k in DIMENSIONS}
        self.assertTrue(validate(d)[0])

    def test_fail_and_unknown_block_acceptance(self):
        for state in ('fail', 'unknown'):
            d = base()
            d['gates']['core_task'] = state
            self.assertFalse(validate(d)[1]['acceptance_eligible'])

    def test_numeric_boundaries(self):
        for value in (True, float('nan'), float('inf'), -1, 101):
            d = base()
            d['scores']['ux']['score'] = value
            self.assertTrue(validate(d)[0])

    def test_cli_exit_codes(self):
        with tempfile.TemporaryDirectory() as folder:
            p = Path(folder)/'report.json'
            for mode, gate, strict, expected in (
                ('build','pass',True,0), ('build','fail',False,0),
                ('build','fail',True,3), ('build','unknown',True,3), ('plan','pass',True,3)):
                d = base()
                d['mode'] = mode
                d['gates']['core_task'] = gate
                p.write_text(json.dumps(d))
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(main([str(p)] + (['--strict'] if strict else [])), expected)
            p.write_text('{}')
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(main([str(p)]), 1)
            p.write_text('{')
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(main([str(p)]), 2)

    def traced(self):
        d = base()
        d['advantages'] = [dict(id='a1',source_url='https://example.org/task',observed_at='2026-10-26', evidence_level='E3',transfer_decision='Experiment',user_mechanism='Hypothesis',our_synthesis='Test first',success_metric='Task success')]
        d['roadmap'] = [dict(id='t1',task='Verify hypothesis',priority='P0',kind='validate',advantage_ids=['a1'],success_criteria='Reproducible observation')]
        return d

    def test_e3_can_prioritize_validation(self):
        self.assertEqual(validate(self.traced())[0], [])

    def test_e3_cannot_alone_justify_p0_implementation(self):
        d = self.traced()
        d['roadmap'][0]['kind'] = 'implement'
        self.assertTrue(validate(d)[0])

    def test_broken_trace_and_invalid_advantage(self):
        for field, value in (('source_url','bad'),('observed_at','2026-02-30'),('evidence_level','E4'),('transfer_decision','Copy'),('success_metric','')):
            d = self.traced()
            d['advantages'][0][field] = value
            self.assertTrue(validate(d)[0])
        d = self.traced()
        d['roadmap'][0]['advantage_ids'] = ['missing']
        self.assertTrue(validate(d)[0])

    def test_rejected_advantage_cannot_be_implemented(self):
        d = self.traced()
        d['advantages'][0]['transfer_decision'] = 'Reject'
        d['roadmap'][0].update(kind='implement', priority='P1')
        self.assertTrue(validate(d)[0])

class MalformedInputTests(unittest.TestCase):
    def test_unhashable_mode_and_gate_are_errors(self):
        d = base()
        d['mode'] = []
        self.assertTrue(validate(d)[0])
        d = base()
        d['gates']['core_task'] = {}
        self.assertTrue(validate(d)[0])

    def test_renderer_preserves_status_and_escapes_cells(self):
        import importlib.util
        import sys
        sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
        spec = importlib.util.spec_from_file_location('render_report', Path(__file__).resolve().parents[1]/'scripts/render_report.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        d = base()
        d['mode'] = 'plan'
        d['scores']['ux']['evidence'] = '<script>|new\nline'
        text = module.render(d)
        self.assertIn('plan_complete', text)
        self.assertIn('Acceptance eligible: False', text)
        self.assertNotIn('<script>', text)
        self.assertIn('&#124;', text)
