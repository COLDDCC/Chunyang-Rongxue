import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from scripts.check_numbers import check, parse_value, main

GOOD = """
| 项目 | USD | 人民币 |
|---|---:|---:|
| 医疗费 | 13,600–18,600 | ¥9.1–12.4 万 |
| 行程 | 2,000–4,000 | ¥1.3–2.7 万 |
| **合计** | **15,600–22,600** | **¥10.4–15.1 万** |
| 约合人民币 | 不参与 | x |
"""

class CheckNumbersTests(unittest.TestCase):
    def test_parse_values(self):
        self.assertEqual(parse_value('**US$13,600–18,600**')[:2], (13600, 18600))
        self.assertEqual(parse_value('≈¥10.4 万')[:2], (10.4, 10.4))
        self.assertIsNone(parse_value('按处方浮动'))
        self.assertEqual(parse_value('**约 12–16 天**')[:2], (12, 16))

    def test_consistent_table_passes(self):
        self.assertEqual(check(GOOD), (1, []))

    def test_mismatch_is_reported_with_column_name(self):
        checked, problems = check(GOOD.replace('2,000–4,000', '2,000–4,200'))
        self.assertEqual(checked, 1)
        self.assertEqual(len(problems), 1)
        self.assertIn('USD', problems[0])

    def test_exact_unless_marked_approximate(self):
        table = "| a | b |\n|---|---|\n| x | 7,550 |\n| y | 8,000 |\n| 合计 | {} |\n"
        self.assertTrue(check(table.format('15,600'))[1])
        self.assertFalse(check(table.format('≈15,600'))[1])
        self.assertTrue(check(table.format('≈15,700'))[1])

    def test_blockquote_tables_and_skipped_text_columns(self):
        quoted = '\n'.join('> ' + line for line in GOOD.strip().splitlines())
        self.assertEqual(check(quoted), (1, []))
        mixed = "| a | b | c |\n|---|---|---|\n| x | 1 | 每年 |\n| y | 2 | 按处方 |\n| Total | 3 | |\n"
        self.assertEqual(check(mixed), (1, []))

    def test_tables_without_totals_are_ignored(self):
        self.assertEqual(check("| 年 | 费用 |\n|---|---|\n| 1 | 800 |\n| 5 | 4,000 |\n"), (0, []))

    def test_cli_exit_codes(self):
        with tempfile.TemporaryDirectory() as folder:
            good, bad = Path(folder)/'good.md', Path(folder)/'bad.md'
            good.write_text(GOOD, encoding='utf-8')
            bad.write_text(GOOD.replace('15,600', '15,900'), encoding='utf-8')
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(main([str(good)]), 0)
                self.assertEqual(main([str(bad)]), 1)
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(main([str(Path(folder)/'missing.md')]), 2)

if __name__ == '__main__':
    unittest.main()
