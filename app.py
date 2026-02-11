from __future__ import annotations

from pathlib import Path
from flask import Flask, flash, redirect, render_template, request, url_for

from src.validation import looks_like_pinterest_board
from src.workflow import PinterestDownloadError, Workflow

app = Flask(__name__)
app.secret_key = "replace-me"
workflow = Workflow()



@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/run", methods=["POST"])
def run_pipeline():
    board_url = request.form.get("board_url", "").strip()
    output_dir = request.form.get("output_dir", "./output").strip()
    max_images = request.form.get("max_images", "").strip()

    if not board_url:
        flash("Please provide a Pinterest board URL.", "error")
        return redirect(url_for("index"))

    if not looks_like_pinterest_board(board_url):
        flash("Please provide a valid Pinterest board URL, for example: https://www.pinterest.com/<user>/<board>/", "error")
        return redirect(url_for("index"))

    parsed_limit = int(max_images) if max_images.isdigit() else None

    try:
        images, draft = workflow.run(
            board_url=board_url,
            output_root=Path(output_dir).expanduser().resolve(),
            max_images=parsed_limit,
        )
    except PinterestDownloadError as err:
        flash(str(err), "error")
        return redirect(url_for("index"))
    except Exception as err:  # pragma: no cover - safety fallback for UI
        flash(f"Unexpected error: {err}", "error")
        return redirect(url_for("index"))

    return render_template(
        "result.html",
        images=[str(path) for path in images],
        draft_path=str(draft.draft_path),
        caption=draft.payload["caption"],
        source=draft.payload["source"],
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
