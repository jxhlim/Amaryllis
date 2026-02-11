# Pinterest Board → Instagram Carousel Draft Tool

A lightweight Flask app that:
1. Downloads images from a Pinterest board (via `gallery-dl`) in the highest available quality.
2. Organizes downloaded files into date folders (`YYYY-MM-DD`).
3. Creates an Instagram carousel draft payload (`.json`) and preview caption/order in the app.

## Step-by-step setup (first time)

### 1) Open a terminal and go to your project folder

Use the folder where this repo exists on **your machine** (not `/workspace/Amaryllis`, which was only for my environment):

```bash
cd /path/to/Amaryllis
```

If you have not cloned the repo yet:

```bash
git clone <your-repo-url> Amaryllis
cd Amaryllis
```

### 2) Confirm you're in the right folder

```bash
pwd
ls
```

You should see `app.py`, `requirements.txt`, `src`, `templates`.

### 3) Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 4) Install dependencies

```bash
pip install -r requirements.txt
```

### 5) Run the app

```bash
python app.py
```

Then open `http://localhost:8000`.

### What to enter in the form

- **Pinterest board URL**: `https://au.pinterest.com/limjxh/amaryllis_a/`
- **Output directory**: `./output`
- **Max images**: optional (leave blank for all)

Click **Run pipeline**.

## One-command startup option

If you prefer, from inside the repo root run:

```bash
./run_local.sh
```

This script will:
- create `.venv` if missing,
- install/update dependencies,
- start the Flask app on port 8000.

## Daily use (after first setup)

```bash
cd /path/to/Amaryllis
source .venv/bin/activate
python app.py
```

Or just run:

```bash
cd /path/to/Amaryllis
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

- If terminal says `No such file or directory` for `requirements.txt` or `app.py`, you're not in the repo root. Run `pwd`, then `cd` into the folder that contains those files.
- If `gallery-dl` cannot access a private board, configure gallery-dl authentication.
- This app creates local drafts only; posting to Instagram remains manual.

## Notes

- Follow Pinterest and Instagram Terms of Service, API/platform rules, and applicable copyright/licensing requirements.
