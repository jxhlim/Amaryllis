# Pinterest Board → Instagram Carousel Draft Tool

A lightweight Flask app that:
1. Downloads images from a Pinterest board (via `gallery-dl`) in the highest available quality.
2. Organizes downloaded files into date folders (`YYYY-MM-DD`).
3. Creates an Instagram carousel draft payload (`.json`) and preview caption/order in the app.

## Step-by-step setup (first time)

From any terminal, run these commands exactly:

```bash
cd /workspace/Amaryllis
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Then open `http://localhost:8000`.

### What to enter in the form

- **Pinterest board URL**: `https://au.pinterest.com/limjxh/amaryllis_a/`
- **Output directory**: `./output`
- **Max images**: optional (leave blank for all)

Click **Run pipeline**.

## One-command startup option

If you prefer, use the helper script:

```bash
cd /workspace/Amaryllis
./run_local.sh
```

This script will:
- create `.venv` if missing,
- install/update dependencies,
- start the Flask app on port 8000.

## Daily use (after first setup)

```bash
cd /workspace/Amaryllis
source .venv/bin/activate
python app.py
```

Or just run:

```bash
cd /workspace/Amaryllis
./run_local.sh
```

## Output structure

```text
output/
  images_by_day/
    2026-01-04/
      image1.jpg
      image2.jpg
  drafts/
    instagram_draft_YYYYMMDD_HHMMSS.json
```

## Troubleshooting

- If terminal says `No such file or directory: requirements.txt` or `app.py`, you are in the wrong folder. Run `cd /workspace/Amaryllis`.
- If `gallery-dl` cannot access a private board, configure gallery-dl authentication.
- This app creates local drafts only; posting to Instagram remains manual.

## Notes

- Follow Pinterest and Instagram Terms of Service, API/platform rules, and applicable copyright/licensing requirements.
