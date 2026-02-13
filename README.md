# Excel Dependency Explorer (Arixcel-style + Visual Graph)

A lightweight Flask app to inspect **trace dependents** in Excel workbooks.

## What it does

1. Upload an `.xlsx` file.
2. Enter a starting cell (`SheetName!A1`).
3. Build a formula dependency index.
4. Show recursive dependents as:
   - a hierarchical tree,
   - a flat dependent list,
   - and an interactive node-link flow chart.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open: `http://localhost:8000`

## Notes / current scope

- Supports common A1-style formula references and ranges.
- Range references (`A1:A3`) are expanded into individual cells.
- Sheet references like `Sheet2!B5` are supported.
- Advanced constructs like `INDIRECT` and complex table references are not fully resolved.

## Run tests

```bash
pytest
```
