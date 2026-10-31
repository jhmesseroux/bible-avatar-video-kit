# Offset between two audio tracks, by cross-correlating their 10 ms loudness envelopes (pure Python, no numpy).
#   sync_offset.py source/avatar.mp4 source/voice.mp3        → how much later the mp3 must start (VOICE_OFFSET - INTRO)
#   sync_offset.py renders/x-4k.mp4 source/avatar.mp4 --at 8   → lip-sync check: should print INTRO (±0.03 s); check at
#   --at 8 and --at 20 (one window can alias on music-heavy stretches: trust two that agree)
import array, subprocess, sys

argv = sys.argv[1:]
at = None
if '--at' in argv:
    k = argv.index('--at')
    at = float(argv[k + 1])
    del argv[k:k + 2]
if len(argv) != 2:
    sys.exit('usage: sync_offset.py <a> <b> [--at SECONDS]')
a_path, b_path = argv


def env(f, ss, t):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(ss), '-t', str(t), '-i', f, '-ac', '1', '-ar', '8000', '-f', 's16le', '-'],
                         capture_output=True, check=True).stdout
    a = array.array('h', raw)
    e = [sum(abs(x) for x in a[i:i + 80]) / 80 for i in range(0, len(a) - 80, 80)]
    if len(e) < 600:
        sys.exit(f'{f}: no audio, or less than 6 s of it from {ss} s')
    mu = sum(e) / len(e)
    return [x - mu for x in e]


if at is None:  # two reads of the same voice: whole length, shifts within ±1 s
    a, b = env(a_path, 0, 600), env(b_path, 0, 600)
    n = min(len(a), len(b)) - 120
    best = max(range(-100, 101), key=lambda k: sum(a[i + k] * b[i] for i in range(110, n)))
    print(f'{a_path} audio = {b_path} delayed by {best / 100:+.2f} s')
else:  # a render against its source: render time = source time + offset, offset searched in 0..pre s
    pre = min(4.0, at)  # the source window starts `pre` s before the render window
    steps = int(round(pre * 100))
    a, b = env(a_path, at, 25), env(b_path, at - pre, 25)
    n = min(len(a), len(b) - steps - 1)
    best = max(range(0, steps + 1), key=lambda d: sum(a[i] * b[i + d] for i in range(0, n)))
    print(f'{a_path} = {b_path} + {pre - best / 100:.2f} s')
