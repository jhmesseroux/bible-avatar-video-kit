#!/usr/bin/env bash
# Set up a Mac to make the « Enracinée avec Adeline Nana » Bible videos with Claude Code: checks (and with Homebrew
# installs) ffmpeg, ImageMagick, Node and Python 3, links this repo's skill into ~/.claude/skills (so `git pull`
# updates it), installs the HyperFrames skills, and reports what is still missing (Chrome, Codex login).
# usage: ./install.sh            (re-run any time; it only adds what is missing)
set -euo pipefail
REPO="$(cd "$(dirname "$0")" && pwd)"
CLAUDE_HOME="${CLAUDE_HOME:-$HOME/.claude}"
SKILL_SRC="$REPO/skills/bible-avatar-video"
SKILL_DST="$CLAUDE_HOME/skills/bible-avatar-video"
todo=()

have() { command -v "$1" >/dev/null 2>&1; }

echo "== Tools"
if ! have brew; then
  todo+=("Install Homebrew (https://brew.sh), then re-run ./install.sh")
else
  for pair in ffmpeg:ffmpeg magick:imagemagick node:node python3:python; do
    cmd=${pair%%:*}; pkg=${pair#*:}
    if have "$cmd"; then echo "ok   $cmd"; else echo "add  $pkg"; brew install "$pkg"; fi
  done
fi
for cmd in ffmpeg magick node npx python3; do have "$cmd" || todo+=("Missing command: $cmd"); done
[ -d "/Applications/Google Chrome.app" ] && echo "ok   Google Chrome" || todo+=("Install Google Chrome (thumbnails are rendered with it): https://www.google.com/chrome/")

echo "== Skill"
mkdir -p "$CLAUDE_HOME/skills"
if [ -L "$SKILL_DST" ] && [ "$(readlink "$SKILL_DST")" = "$SKILL_SRC" ]; then
  echo "ok   $SKILL_DST → $SKILL_SRC"
else
  if [ -e "$SKILL_DST" ] || [ -L "$SKILL_DST" ]; then
    backup="$CLAUDE_HOME/backups/bible-avatar-video-$(date +%Y%m%d-%H%M%S)"  # outside skills/: never loaded twice
    mkdir -p "$CLAUDE_HOME/backups"
    mv "$SKILL_DST" "$backup"
    echo "kept the previous copy in $backup"
  fi
  ln -s "$SKILL_SRC" "$SKILL_DST"
  echo "link $SKILL_DST → $SKILL_SRC"
fi
chmod +x "$SKILL_SRC"/scripts/*.sh

echo "== HyperFrames skills"
if have npx; then
  if [ -e "$CLAUDE_HOME/skills/hyperframes/SKILL.md" ]; then
    echo "ok   already installed (update: npx hyperframes skills update)"
  else
    npx --yes skills add heygen-com/hyperframes -g -y -s '*' -a claude-code \
      || todo+=("Install the HyperFrames skills by hand: npx skills add heygen-com/hyperframes -g")
  fi
fi

echo "== Images (Codex)"
if have codex; then
  echo "ok   codex $(codex --version 2>/dev/null | tail -1) — make sure you are logged in: codex login"
else
  todo+=("For the oil paintings: npm install -g @openai/codex, then codex login (ChatGPT account). Without it, any image generator works with the style prompt in the skill.")
fi

echo
if [ ${#todo[@]} -eq 0 ]; then
  echo "All set. Restart Claude Code, then type /bible-avatar-video with your text, mp3 and HeyGen mp4."
else
  echo "Still to do:"; for t in "${todo[@]}"; do echo "  - $t"; done
  echo "Then restart Claude Code."
fi
