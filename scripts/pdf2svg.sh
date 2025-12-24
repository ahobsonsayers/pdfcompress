#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "Usage: $(basename "$0") <input-dir> <output-dir>"
  exit 1
fi

INPUT_DIR="$1"
OUTPUT_DIR="$2"

mkdir -p "$INPUT_DIR"
mkdir -p "$OUTPUT_DIR"

PDF_PATHS="$(
  find "$INPUT_DIR" \
    -type f \
    -name '*.pdf'
)"

while read -r PDF_PATH; do
  PDF_NAME="$(basename "$PDF_PATH")"
  FILE_NAME="${PDF_NAME%.*}"
  SVG_PATH="$OUTPUT_DIR/$FILE_NAME.svg"

  echo "Converting pdf to svg: $FILE_NAME"
  pdf2svg "$PDF_PATH" "$SVG_PATH"
  echo

done <<<"$PDF_PATHS"
