---
name: bible-avatar-video
description: Edit a French Bible / spirituality short from a HeyGen avatar video and its ElevenLabs voice into a finished 4K vertical video in the « Enracinée avec Adeline Nana » style — a new animation concept each time (avatar changing shape, verses revealed word by word, Codex oil paintings, line drawings), karaoke captions, logo intro card + corner mark + end card, ducked worship music bed and soft SFX — plus its thumbnails. Use whenever the user says "/bible-avatar-video", gives a text + an ElevenLabs mp3 + a HeyGen mp4 for Adeline, or says "fais une vidéo comme la dernière", "edit this avatar video like the Bible ones", "monte la vidéo d'Adeline", "make a video for this text and audio", "fais la miniature". Never regenerates the voice.
tags: [video, hyperframes, bible, sermon, heygen, elevenlabs, avatar, thumbnail]
---

# Bible avatar video (Adeline Nana)

Every rule below comes from the owner's feedback. Breaking one means redoing work.

**Inputs from the user:** the script text (may contain ElevenLabs tags like `[softly]`, ignore them on screen), the ElevenLabs voice `.mp3`, the HeyGen avatar `.mp4` (1080×1920, ~50–60 s), sometimes a photo of the avatar for the thumbnail.

**Needs:** the HyperFrames skills (`npx skills add heygen-com/hyperframes --all`, then load `/hyperframes` before authoring), Node, `ffmpeg`, ImageMagick (`magick`), Google Chrome, Python 3. Images come from Codex (`npx hyperframes media-use resolve --type image --provider codex`); without Codex, use any image generator with the same style prompt.

## Hard rules

- **Never regenerate the voice.** Use the user's mp3 as is. Never ask for or call ElevenLabs.
- **Plan first, then visuals, then render.** The user expects three stops: (1) a beat-by-beat plan table (time, what she says, what we see), (2) a labelled preview board of ~15 key frames (+ optional draft mp4), (3) the 4K render only after they say go. When asked "plan it first" stop after the plan.
- **A new animation concept per video**, matched to the message ("this time I want a different animation"). Done so far (don't repeat as-is): `examples/manuscrit-vivant` (parchment pages inked word by word, page turn, stamped notes, crumpled list, hand → heart drawing) and `examples/nuit-aube` (starry night → dawn, prayer lanterns, verse letters lighting like stars, psalm scrolling while the sky warms, candle). Other ideas: stained glass, seasons/tree roots (« Enracinée »), path and lamp (Ps 119:105), water/well, sowing.
- **Verses:** Louis Segond 1910 text, labelled `LIVRE N · V` + "LOUIS SEGOND 1910". Show the verse in the words she actually says when they differ slightly. Hide captions while a verse or statement already writes the words on screen.
- **Captions:** karaoke chunks (≤5 words), the spoken word on a framboise pill `#9B2E5E`, key words gold. Fix Whisper slips from the script (e.g. « éternelle » → « Éternel », gender agreements) through the `FIX` map in `build.py`.
- **Logo (default, approved):** 1.6 s intro card with `enracinee-lockup-a-vertical-ondark.svg` visible at frame 0 (it is the first frame / thumbnail), the `enracinee-monogram-a-filled-ondark.svg` « A » disc as corner mark (`LOGO_POSITION = 'top-right'`, switchable per video), the same lockup on the end card under the closing question. Her name is **Adeline Nana** (never "Nane"). Show placement mockups before changing any logo placement.
- **Export 4K:** `--resolution portrait-4k -q high -f 30`.
- **Music:** `assets/music/bible-spirituality-ethereal.mp3` is the default bed; the three `sermon-sand-*` beds are alternatives, propose one when it fits the mood better and say which one was used. Bed at −25 dB, sidechain-ducked under the voice, 2 s fade in / 3 s fade out. SFX: one soft sound per thing that appears, volume 0.05–0.16.
- **Images:** warm painterly oil paintings, one fixed style prompt per video (see the prompt in `examples/*/` notes below), no text in images, never depict a false prophet so they look like Jesus.
- Talk to the user in French.

## Workflow

1. **Scaffold** (copies brand, fonts, CSS, music, sources; transcribes; measures the voice offset):
   ```bash
   ~/.claude/skills/bible-avatar-video/scripts/new_project.sh ~/Documents/projects/videos/<slug> <avatar.mp4> <voice.mp3> [bed]
   ```
   The last line prints how much the mp3 is ahead of the avatar's own audio (`+0.43 s`, `+0.02 s`…): that number goes in `mix.py` as `VOICE_OFFSET = INTRO + <it>`.
2. **Read the transcript** (`source/transcript.json`, word timings on the video clock) and locate the face: `ffmpeg -ss 12 -i source/avatar.mp4 -frames:v 1 -vf "scale=540:960,drawgrid=w=50:h=50:t=1:c=red@0.6" grid.jpg`. The avatar shapes (`SHAPES` in `build.py`: clip inset + radii + matching frame box) must keep the face inside.
3. **Write the plan** (table) with the new concept, and stop for the user.
4. **Generate the paintings** (2 is usually enough), save them as `assets/img/<name>.jpg`.
5. **Write `build.py`** starting from the example closest in structure (copy `examples/<style>/build.py` and `mix.py` into the project). Keep its helpers: `W(word, near)` finds a word's time (pass `near` on the source clock, `INTRO` is added), `ft`/`to`/`fade`/`out`/`ink`/`draw`, `shape()`, the caption builder with `HIDE` ranges and `FIX`. Set `VIDEO_LEN` to the avatar duration. One paused GSAP timeline in `window.__timelines["main"]`, the avatar `<video>` muted (the voice is in `assets/mix.wav`).
6. **Mix:** edit the cue list in `mix.py` to the new scenes, run `python3 build.py && python3 mix.py`.
7. **Check:** `npx --yes hyperframes@0.8.188 check` — fix every error. Known acceptable: duplicate lockup img warning, contrast warnings on deliberately dimmed text. Never tween `letterSpacing` (use `scaleX`); a caption chunk must not run into a hidden stretch (the builder cuts it).
8. **Preview board:** `npx --yes hyperframes@0.8.188 snapshot --at <15 times> --no-end --describe false -o snapshots`, then `scripts/board.sh snapshots apercu-style-<concept>.png "label" …` and open it; optionally `render -q draft -o renders/apercu-brouillon.mp4`. Look at every frame yourself first (face covered? text overlapping? orphan « » ?).
9. **After the go:** `python3 build.py && python3 mix.py && npx --yes hyperframes@0.8.188 render --resolution portrait-4k -q high -f 30 -o renders/<slug>-4k.mp4`. Verify: 2160×3840, duration, `ffmpeg -i … -af volumedetect` max below −1 dB, lip sync with `python3 scripts/sync_offset.py renders/<slug>-4k.mp4 source/avatar.mp4 --at 8` and `--at 20` (both must print `+ 1.60 s`).
10. **Thumbnails** (when asked): copy `examples/nuit-aube/thumbnail/make.py`. Cut the avatar out of a calm frame of the video (or the photo the user gives): `npx hyperframes remove-background frame.png -o thumbnail/assets/adeline-cutout.png`; clean leftovers of the burgundy chair if any. Title + handwritten line + verse slip + lockup, vertical 1080×1920 (title and face inside the centre 3:4) and 16:9 1280×720, plus 4K PNGs. Check: no word alone on a line, no hard seam between painting and background.

## Files

| Path | |
|---|---|
| `assets/brand/` | Enracinée lockups (vertical, horizontal) and the « A » monogram, on dark |
| `assets/fonts/` | Cormorant Garamond, DM Sans, Instrument Serif, Caveat (all SIL OFL) |
| `assets/sermon.css` | calm-scripture base styles (dark ground, gold accent, caption block) |
| `assets/music/` | owned ElevenLabs Music beds (ethereal default + 3 sermon-sand) |
| `assets/sfx/` | owned soft SFX (synthesized), normalized to −3 dBFS |
| `examples/nuit-aube/` | « Le silence de Dieu » — build, mix, thumbnail |
| `examples/manuscrit-vivant/` | « Tu ne pries pas pour informer Dieu » — build, mix |
| `scripts/` | `new_project.sh`, `sync_offset.py`, `board.sh` |

Painting style prompt used so far: "Vertical 9:16 portrait composition. Painterly digital oil painting, cinematic chiaroscuro, reverent biblical mood, ancient Middle East setting, no text, no letters, no logos." + a palette line (warm golden-hour amber, or night indigo / dawn gold) + "Scene: …".
