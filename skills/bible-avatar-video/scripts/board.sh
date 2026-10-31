#!/usr/bin/env bash
# Preview board for the user: snapshot frames (in time order) labelled underneath, 5 per row.
# usage: board.sh <snapshots-dir> <out.png> "label 1" "label 2" ...   (one label per frame-*.png)
set -euo pipefail
SKILL="$(cd "$(dirname "$0")/.." && pwd)"
FONT="$SKILL/assets/fonts/CG-SemiBold.ttf"
SNAP=$1; OUT=$2; shift 2
TMP=$(mktemp -d)
i=0
for f in "$SNAP"/frame-*.png; do
  label=${1:-}; [ $# -gt 0 ] && shift
  magick "$f" -resize 432x768 -background '#0B0F1E' -gravity south -splice 0x56 \
    -font "$FONT" -pointsize 30 -fill '#E6ECF7' -annotate +0+10 "${label//%/%%}" "$TMP/$(printf %02d $i).png"
  i=$((i + 1))
done
magick montage -font "$FONT" "$TMP"/*.png -tile 5x -geometry +14+14 -background '#0B0F1E' "$OUT"
rm -rf "$TMP"
echo "$OUT"
