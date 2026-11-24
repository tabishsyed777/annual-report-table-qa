# Annual Report Table QA

Look up fiscal cells, compare two periods or compute an exact decimal change with citations to both operands.

## Quick start

From this directory, run these commands with Python 3.12 or 3.13. The example corpus is fictional and runs offline with the standard library.

```sh
python3 core.py ask 'What was revenue in FY2024?'
python3 core.py build data/source.json snapshot.json
python3 core.py ask 'What was revenue in FY2025?' --snapshot snapshot.json
python3 -m unittest discover -v
python3 evaluate.py
```

## Asking questions

Use “What was revenue in FY2024?”, “Compare revenue in 2025 and 2024”, or “Change in revenue from 2024 to 2025?”

## Using your own sources

Use the records in `data/source.json` as a schema example. Supply unique citation IDs and usable source locators. Build a new snapshot after additions, edits, or deletions. A successful build atomically replaces the previous snapshot. Results contain the answer, retrieval method and source locators. Unsupported queries return `insufficient_evidence`.

Input consists of normalized fiscal cells from one report per snapshot. Currency conversion, percentage growth and raw PDF extraction are outside this implementation.

See [QA.md](QA.md) for measured results, review status and release limits.

To import a CSV with the same headers as the bundled table, run `python3 import_table.py data/demo-report.csv > cells.json`, then `python3 core.py build cells.json snapshot.json`. Fiscal year columns can appear in any order.
