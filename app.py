from __future__ import annotations

import json
import tempfile
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, url_for

from src.dependency_graph import DependencyGraph, normalize_cell
from src.workbook_reader import read_formulas_from_workbook

app = Flask(__name__)
app.secret_key = "replace-me"


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    workbook = request.files.get("workbook")
    start_cell = request.form.get("start_cell", "").strip()
    max_depth = request.form.get("max_depth", "4").strip()

    if not workbook or not workbook.filename:
        flash("Please upload an .xlsx workbook.", "error")
        return redirect(url_for("index"))

    if not start_cell or "!" not in start_cell:
        flash("Start cell must be in format SheetName!A1.", "error")
        return redirect(url_for("index"))

    try:
        parsed_depth = max(1, min(int(max_depth), 12))
    except ValueError:
        flash("Max depth must be a number.", "error")
        return redirect(url_for("index"))

    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = Path(tmpdir) / workbook.filename
        workbook.save(file_path)
        formulas = read_formulas_from_workbook(file_path)

    graph = DependencyGraph(formulas)
    sheet, addr = start_cell.split("!", 1)
    start = normalize_cell(sheet, addr)

    tree = graph.tree(start, max_depth=parsed_depth)
    edges = graph.subgraph_edges(start, max_depth=parsed_depth)

    nodes = sorted({start, *[s for s, _ in edges], *[t for _, t in edges]})

    return render_template(
        "result.html",
        start_cell=start,
        tree=tree,
        formulas_count=len(formulas),
        nodes_json=json.dumps([{"data": {"id": n, "label": n}} for n in nodes]),
        edges_json=json.dumps([{"data": {"source": s, "target": t}} for s, t in edges]),
        dependents=graph.dependents(start, max_depth=parsed_depth),
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
