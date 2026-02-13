#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="${ROOT_DIR}/dist"
OUT_FILE="${OUT_DIR}/excel_dependency_explorer_changed_files.zip"

mkdir -p "${OUT_DIR}"

cd "${ROOT_DIR}"

FILES=(
  README.md
  app.py
  requirements.txt
  src/dependency_graph.py
  src/workbook_reader.py
  static/styles.css
  templates/index.html
  templates/result.html
  tests/test_workflow.py
)

zip -q -r "${OUT_FILE}" "${FILES[@]}"

echo "Created: ${OUT_FILE}"
