#!/usr/bin/env bash
set -euo pipefail # Strict

if [[ $# -ne 3 ]]; then
  echo "Usage: $(basename "$0") <input-dir> <output-dir> <dpi>"
  exit 1
fi

INPUT_DIR="$1"
OUTPUT_DIR="$2"
DPI="$3"

mkdir -p "$INPUT_DIR"
mkdir -p "$OUTPUT_DIR"

SVG_PATHS="$(
  find "$INPUT_DIR" \
    -type f \
    \( -name '*.svg' -o -name '*.svgz' \)
)"

while read -r SVG_PATH; do
  SVG_NAME="$(basename "$SVG_PATH")"
  IMAGE_NAME="${SVG_NAME%.*}"
  PNG_PATH="$OUTPUT_DIR/$IMAGE_NAME.png"

  echo "Converting svg to png: $IMAGE_NAME"
  inkscape "$SVG_PATH" \
    --export-type=png \
    --export-dpi="$DPI" \
    --export-filename="$PNG_PATH"
  echo

done <<<"$SVG_PATHS"
