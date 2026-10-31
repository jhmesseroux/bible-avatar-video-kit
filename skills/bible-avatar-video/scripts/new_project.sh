#!/usr/bin/env bash
# Scaffold a Bible avatar video project: copies the brand, fonts, scripture CSS and a music bed from the skill,
# the HeyGen avatar video and the ElevenLabs voice into source/, then transcribes the video (Whisper medium, French).
# usage: new_project.sh <dir> <avatar.mp4> <voice.mp3> [music-bed-name]   (bed default: bible-spirituality-ethereal)
set -euo pipefail
SKILL="$(cd "$(dirname "$0")/.." && pwd)"
HF=hyperframes@0.8.188
DIR=$1; AVATAR=$2; VOICE=$3; BED=${4:-bible-spirituality-ethereal}
[ -e "$DIR" ] && { echo "$DIR already exists" >&2; exit 1; }
mkdir -p "$DIR"/{source,assets/{img,bgm},renders,thumbnail/assets,.read}
cp -R "$SKILL/assets/brand" "$SKILL/assets/fonts" "$SKILL/assets/sermon.css" "$DIR/assets/"
cp "$SKILL/assets/music/$BED.mp3" "$DIR/assets/bgm/"
cp "$AVATAR" "$DIR/source/avatar.mp4"
cp "$VOICE" "$DIR/source/voice.mp3"
NAME=$(basename "$DIR")
cat > "$DIR/package.json" <<EOF
{
  "name": "$NAME",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "npx --yes $HF preview",
    "check": "npx --yes $HF check",
    "render": "npx --yes $HF render",
    "publish": "npx --yes $HF publish"
  }
}
EOF
printf '{\n  "id": "%s",\n  "name": "%s",\n  "createdAt": "%s"\n}\n' "$NAME" "$NAME" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$DIR/meta.json"
cat > "$DIR/hyperframes.json" <<'EOF'
{
  "$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",
  "registry": "https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry",
  "paths": { "blocks": "compositions", "components": "compositions/components", "assets": "assets" },
  "media": { "autoProxy": true },
  "authoringSkill": "general-video"
}
EOF
cd "$DIR"
for f in source/avatar.mp4 source/voice.mp3; do printf '%s %ss\n' "$f" "$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")"; done
npx --yes $HF transcribe source/avatar.mp4 -m medium -l fr
python3 "$SKILL/scripts/sync_offset.py" source/avatar.mp4 source/voice.mp3
