# Mix: Adeline's ElevenLabs read (source/voice.mp3, untouched) placed where the avatar's lips say it (+0.43 s in the
# video, + the intro card) over the Bible ethereal bed levelled to BED_DB, ducked under the voice, 2 s fade in /
# 3 s fade out, plus one soft SFX per thing that appears (paper, ink, page turn, stamps). usage: python3 mix.py
import json, os, re, subprocess, contextlib, io
with contextlib.redirect_stdout(io.StringIO()):
    from build import W, END, VIDEO_END, INTRO, TURN, CRUMPLE
VOICE_OFFSET = INTRO + 0.43  # the mp3 starts 0.43 s before the avatar's own audio
BED_DB = -25.0
music = 'assets/bgm/bible-spirituality-ethereal.mp3'
SFX = os.path.expanduser('~/.claude/skills/bible-avatar-video/assets/sfx')

cues = []
def c(t, name, vol): cues.append([round(max(0.0, t), 3), name, vol])
c(0.15, 'sparkle-logo', 0.11)                                               # intro logo card
c(INTRO - 0.4, 'whoosh-soft', 0.08)
c(W('besoins?', 3.5), 'swipe-scroll', 0.08)                                 # « informer » struck
c(W('Si', 4.2) - 0.2, 'whoosh-soft', 0.08)                                  # avatar → arch
for word, near in (('problèmes,', 5.6), ('inquiétudes', 6.5), ('désirs', 7.9)):
    c(W(word, near) - 0.15, 'paper-rustle', 0.10)
for word, near in (('problèmes,', 5.6), ('inquiétudes', 6.5), ('désirs', 7.9)):
    c(W(word, near) + 0.8, 'drop-thud', 0.11)                                # « Il sait » stamps
c(W('pourquoi', 9.8) - 0.05, 'pop-soft', 0.10)
c(W('Dans', 12.3) - 0.3, 'whoosh-soft', 0.08); c(W('Dans', 12.3), 'page-flip', 0.14)
c(TURN, 'page-flip', 0.16)
c(W('La', 27.2) - 0.2, 'whoosh-soft', 0.08)
c(W('mais', 29.8), 'swipe-scroll', 0.07); c(W('relation', 31.3), 'sparkle-logo', 0.07)
c(W('simplement', 33.5) - 0.1, 'paper-rustle', 0.10)
c(CRUMPLE, 'paper-rustle', 0.14); c(CRUMPLE + 0.35, 'whoosh-up', 0.08)
c(W('Alors', 40.1) - 0.3, 'whoosh-soft', 0.08)
c(W('rapprocher', 45.3) + 0.3, 'swipe-scroll', 0.06)
c(W('main', 51.4) - 0.6, 'whoosh-soft', 0.05); c(W('cœur?', 52.8) - 0.2, 'sparkle-logo', 0.08)
c(VIDEO_END - 0.5, 'whoosh-soft', 0.07)
c(VIDEO_END + 0.5, 'chime-success', 0.08)                                   # end logo
json.dump(sorted(cues), open('sfx-cues.json', 'w'), indent=0)

mean = float(re.search(r'mean_volume: (-?[\d.]+)', subprocess.run(['ffmpeg', '-hide_banner', '-i', music, '-af', 'volumedetect', '-f', 'null', '-'],
                                                                     capture_output=True, text=True).stderr).group(1))
d = int(VOICE_OFFSET * 1000)
g = (f'[1:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{END},asetpts=PTS-STARTPTS,volume={BED_DB - mean:.1f}dB,'
     f'afade=t=in:d=2,afade=t=out:st={END - 3}:d=3[m];'
     f'[0:a]aresample=48000,aformat=sample_rates=48000:channel_layouts=stereo,adelay={d}|{d},apad=whole_dur={END},asplit=2[vs][vm];'
     f'[m][vs]sidechaincompress=threshold=0.03:ratio=4:attack=40:release=600[duck];'
     + ''.join(f'[{k + 2}:a]aresample=48000,aformat=channel_layouts=stereo,volume={v},adelay={int(t * 1000)}|{int(t * 1000)},apad=whole_dur={END}[x{k}];'
               for k, (t, n, v) in enumerate(cues))
     + '[vm][duck]' + ''.join(f'[x{k}]' for k in range(len(cues)))
     + f'amix=inputs={2 + len(cues)}:normalize=0:dropout_transition=0,atrim=0:{END},alimiter=limit=0.89:level=disabled[out]')
os.makedirs('.read', exist_ok=True)
open('.read/mix-graph.txt', 'w').write(g)
sfx_in = sum((['-i', f'{SFX}/{n}.wav'] for t, n, v in cues), [])
subprocess.run(['ffmpeg', '-hide_banner', '-v', 'error', '-y', '-i', 'source/voice.mp3', '-i', music] + sfx_in +
               ['-/filter_complex', '.read/mix-graph.txt', '-map', '[out]', '-c:a', 'pcm_s16le', 'assets/mix.wav'], check=True)
print('assets/mix.wav', len(cues), 'cues', f'(bed gain {BED_DB - mean:+.1f} dB, voice at +{VOICE_OFFSET:.2f} s)')
