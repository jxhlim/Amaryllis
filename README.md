# Pinterest Board → Instagram Carousel Draft Tool

A lightweight Flask app that:
1. Downloads images from a Pinterest board (via `gallery-dl`) in the highest available quality.
2. Organizes downloaded files into date folders (`YYYY-MM-DD`).
3. Creates an Instagram carousel draft payload (`.json`) and preview caption/order in the app.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install gallery-dl pytest
python app.py
```

Open http://localhost:8000 and submit:
- Pinterest board URL (`https://www.pinterest.com/<user>/<board>/`)
- Output directory
- Optional image limit

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
- If you see `gallery-dl is not installed`, run `pip install gallery-dl` inside your venv.
- Private boards may require authenticated `gallery-dl` configuration.
- This app creates local drafts only; posting to Instagram remains manual.

## Notes
- Follow Pinterest and Instagram Terms of Service, API/platform rules, and applicable copyright/licensing requirements.
