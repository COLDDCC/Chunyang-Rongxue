#!/usr/bin/env python3
"""Render validated report data as Markdown; keep narrative as optional context."""
import argparse
import json
from pathlib import Path
from audit import validate, DIMENSIONS, GATES


def cell(value):
    if isinstance(value, list):
        value = ', '.join(map(str, value))
    return str(value).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('|', '&#124;').replace('\n', ' ')


LABELS = {
    'primary_job': 'Primary job', 'current_weakness': 'Current weakness',
    'strongest_opportunity': 'Strongest opportunity', 'innovation_hypothesis': 'Innovation (hypothesis)',
    'shortest_success_path': 'Shortest success path',
    'objective': 'Objective', 'conversion_action': 'Conversion action', 'success_metric': 'Success metric',
}


def narrative(report):
    """One-screen summary and business goal, rendered before the scorecard."""
    lines = [f"Profile: {report.get('profile', 'product')}", '']
    for title, key in (('Summary', 'summary'), ('Business goal', 'business_goal')):
        block = report.get(key)
        if block:
            lines += ['## ' + title, '']
            lines += [f"- **{LABELS.get(k, k)}:** {cell(v)}" for k, v in block.items() if k in LABELS]
            lines.append('')
    return lines


def render(report):
    errors, result = validate(report)
    if errors:
        raise ValueError('; '.join(errors))
    lines = ['# ' + cell(report['product']), '', f"Mode: {report['mode']} · Status: {result['assessment_status']}", '',
             f"Coverage: {result['coverage']} · Weighted score: {result['weighted_score']} · Acceptance eligible: {result['acceptance_eligible']}", '',
             *narrative(report),
             '## Scores', '', '| Dimension | Weight | Score | Evidence / N/A reason |', '|---|---:|---:|---|']
    for key in DIMENSIONS:
        item = report['scores'].get(key, {})
        lines.append('| ' + ' | '.join(map(cell, (key,report['weights'][key],'N/A' if item.get('not_applicable') else item.get('score','unknown'),item.get('reason') if item.get('not_applicable') else item.get('evidence','')))) + ' |')
    lines += ['', '## Gates', '', '| Gate | Result |', '|---|---|']
    lines += [f'| {k} | {report["gates"][k]} |' for k in GATES]
    for title, key, fields in (
        ('Advantages','advantages',('id','source_url','observed_at','evidence_level','transfer_decision','user_mechanism','our_synthesis','success_metric')),
        ('Roadmap','roadmap',('id','task','priority','kind','advantage_ids','success_criteria')),
        ('Labelled estimates','estimates',('id','claim','value','basis','as_of','disclosure','sources'))):
        if report.get(key):
            lines += ['', '## '+title, '', '| '+' | '.join(fields)+' |','|'+'---|'*len(fields)]
            lines += ['| '+' | '.join(cell(item.get(f,'')) for f in fields)+' |' for item in report[key]]
    lines += ['', 'Validation checks structure and declared evidence, not whether observations are true.', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('report')
    parser.add_argument('output')
    args = parser.parse_args()
    try:
        text = render(json.loads(Path(args.report).read_text(encoding='utf-8')))
    except (OSError, ValueError) as exc:
        parser.exit(1, str(exc)+'\n')
    Path(args.output).write_text(text, encoding='utf-8')

if __name__ == '__main__':
    main()
