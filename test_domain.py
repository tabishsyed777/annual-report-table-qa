import unittest
import core

class DomainTests(unittest.TestCase):
    def test_mixed_units(self):
        rows=core.read(core.DEFAULT)
        rows[1]["unit"]="USD"
        self.assertIsNone(core.answer(rows,"Change in revenue from 2024 to 2025?")["answer"])

    def test_nonfinite(self):
        rows=core.read(core.DEFAULT)
        rows[0]["value"]="NaN"
        with self.assertRaises(ValueError): core.validate(rows)

    def test_real_table_import(self):
        import import_table
        self.assertEqual(import_table.convert(core.DEFAULT.with_name("demo-report.csv")),core.read(core.DEFAULT))

    def test_challenge_queries(self):
        rows=core.validate(core.read(core.DEFAULT))
        for query,expected in core.read(core.DEFAULT.parent.parent/"qa/challenge.json"):
            with self.subTest(query=query):
                self.assertEqual(core.answer(rows,query)["answer"],expected)
