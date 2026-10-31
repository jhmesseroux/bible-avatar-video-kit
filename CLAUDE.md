# Bible avatar video kit — instructions for Claude

This repo holds one Claude Code skill, `skills/bible-avatar-video`, that turns a HeyGen avatar video + its ElevenLabs
voice + the script text into a finished 4K vertical Bible short in the « Enracinée avec Adeline Nana » style, plus
its thumbnails. The person using it speaks French: talk to them in French, in plain words (they are not a developer).

## First session on a machine: get it working

Do this before anything else when the person asks to "get started", "installe", "configure", or when
`/bible-avatar-video` is not in the skill list.

1. Run `./install.sh` from this repo. It is safe to re-run. It checks and installs ffmpeg, ImageMagick, Node and
   Python 3 with Homebrew, links the skill into `~/.claude/skills/bible-avatar-video` (a symlink, so `git pull`
   updates it), installs the HyperFrames skills, and prints what is still missing.
2. Walk the person through each "Still to do" line it prints, one at a time:
   - **Homebrew** missing: they paste the one-line installer from https://brew.sh in their Terminal (it asks for their
     Mac password; you cannot type it for them), then you re-run `./install.sh`.
   - **Google Chrome** missing: they install it from https://www.google.com/chrome/ (the thumbnails are rendered
     with it).
   - **Codex** (the oil paintings): `npm install -g @openai/codex`, then they run `! codex login` themselves in this
     session and sign in with their ChatGPT account. Without a ChatGPT plan, use another image generator with the
     style prompt in the skill and save the images by hand.
   - **HyperFrames skills** failed: `npx skills add heygen-com/hyperframes -g` and answer its prompts with them.
3. Check: `ffmpeg -version | head -1`, `magick -version | head -1`, `node -v`, `python3 -V`,
   `ls ~/.claude/skills/bible-avatar-video/SKILL.md ~/.claude/skills/hyperframes/SKILL.md`.
4. Tell them to restart Claude Code (skills load at start), then to come back with three things: the script text,
   the ElevenLabs `.mp3` and the HeyGen `.mp4` (both downloaded on their Mac).

The first transcription downloads a speech model (a few hundred MB) and the first render downloads a browser: say
so, it is normal that it takes a few minutes once.

## Making a video

Load the `bible-avatar-video` skill and follow it. Its hard rules (never regenerate the voice, plan → preview board →
4K render only after their go, a new animation concept per video, logo placement, export 4K) come from the channel
owner and are not optional.

Projects go in `~/Documents/projects/videos/<slug>` unless the person says otherwise. Never put a project inside
this repo.

## Updating

`git pull` in this repo updates the skill (it is linked, not copied). Then `npx hyperframes skills update` for the
HyperFrames skills. Restart Claude Code.

Don't commit or push to this repo unless the person asks.
