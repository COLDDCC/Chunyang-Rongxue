"""Schema checks: jsonschema is a development-only dependency installed in CI."""
import json
import unittest
from pathlib import Path
try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError:
    Draft202012Validator = None
from test_audit import base
import test_boundaries

@unittest.skipIf(Draft202012Validator is None, 'Install jsonschema==4.23.0 for schema QA')
class SchemaTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(__file__).resolve().parents[1]
        schema = json.loads((self.root/'schema/report.schema.json').read_text())
        Draft202012Validator.check_schema(schema)
        self.validator = Draft202012Validator(schema, format_checker=FormatChecker())

    def test_examples_and_structured_report(self):
        for path in (self.root/'examples').rglob('*.json'):
            self.validator.validate(json.loads(path.read_text()))
        self.validator.validate(base())
        self.validator.validate(test_boundaries.BoundaryTests().traced())

    def test_invalid_score_evidence_and_na(self):
        for value in ({'score':80}, {'score':101,'evidence':'x'}, {'not_applicable':True}, {'not_applicable':True,'reason':'private','score':80}):
            d = base()
            d['scores']['ux'] = value
            self.assertTrue(list(self.validator.iter_errors(d)))

    def test_invalid_dates(self):
        d = test_boundaries.BoundaryTests().traced()
        d['advantages'][0]['observed_at'] = '2026-02-30'
        self.assertTrue(list(self.validator.iter_errors(d)))
