# Build « Tu ne pries pas pour informer Dieu »: style « manuscrit vivant ». The HeyGen avatar read changes shape
# (full frame → arch → medallion, gold frame) while parchment Bible pages ink each verse word as it is spoken, a page
# turns from Matthieu 6:8 to 6:9, handwritten notes get stamped, a list crumples, an arch opens on a painting, an
# open hand redraws as a heart. Karaoke captions, « Enracinée avec Adeline Nana » logo (intro card, corner mark, end
# card). usage: python3 build.py
import json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
INTRO = 1.6  # logo card before the avatar; every voice-synced time below is shifted by it
WORDS = [dict(w, start=w['start'] + INTRO, end=w['end'] + INTRO)
         for w in json.load(open(os.path.join(ROOT, 'source/transcript.json'))) if re.search(r'\w', w['text'])]
VIDEO_LEN = 53.25
VIDEO_END = INTRO + VIDEO_LEN
END = round(VIDEO_END + 2.8, 2)
LOGO_POSITION = 'top-right'  # corner mark, switch per video
LOGO_POS_CSS = {'top-right': 'right: 40px; top: 52px;', 'top-left': 'left: 40px; top: 52px;',
                'bottom-right': 'right: 40px; bottom: 260px;', 'bottom-left': 'left: 40px; bottom: 260px;'}
KEYS = {'dieu', 'prier', 'prier?', 'pries', 'père', 'relation', 'enfant', 'rapprocher', 'main', 'cœur', 'informer'}
js = []


def norm(s):
    return re.sub(r'[^\w’\'-]', '', s).lower().replace('’', "'")


def W(word, near, edge='start'):
    near += INTRO  # `near` is given on the source read's clock
    hits = [w for w in WORDS if norm(word) == norm(w['text'])]
    best = min(hits, key=lambda w: abs(w['start'] - near))
    assert abs(best['start'] - near) < 1.5, f'« {word} » expected near {near}s, nearest at {best["start"]}s'
    return best[edge]


def ft(s, frm, to, t):
    js.append(f'tl.fromTo("{s}", {frm}, {to}, {max(0, t):.3f});')


def to(s, props, t):
    js.append(f'tl.to("{s}", {props}, {max(0, t):.3f});')


def fade(s, t, y=30, dur=0.6):
    ft(s, f'{{opacity: 0, y: {y}}}', f'{{opacity: 1, y: 0, duration: {dur}, ease: "power2.out"}}', t)


def out(s, t, dur=0.4):
    to(s, f'{{opacity: 0, duration: {dur}, ease: "power2.in"}}', t)


def draw(sel, t, dur=1.0):
    """Stroke-by-stroke draw-on of a line drawing whose paths carry pathLength="1"."""
    js.append(f'tl.fromTo(gsap.utils.toArray("{sel} .dr"), {{strokeDashoffset: 1}}, {{strokeDashoffset: 0, duration: {dur}, '
              f'ease: "power1.inOut", stagger: 0.12}}, {max(0, t):.3f});')


# ── the avatar's shape: full frame, arch (face window at the top) or medallion; a gold frame follows it ─────────────
SHAPES = {  # clip inset (top right bottom left) + radii, and the matching frame box
    'full': ('0px 0px 0px 0px', '0px 0px 0px 0px', None),
    'arch': ('190px 230px 900px 190px', '330px 330px 34px 34px', (190, 190, 660, 830)),
    'medal': ('250px 330px 1210px 290px', '230px 230px 230px 230px', (290, 250, 460, 460)),
}


def shape(name, t, dur=0.8):
    ins, rad, box = SHAPES[name]
    to('#avwrap', f'{{clipPath: "inset({ins} round {rad})", duration: {dur}, ease: "power3.inOut"}}', t)
    if box:
        x, y, w, h = box
        to('#avframe', f'{{x: {x}, y: {y}, width: {w}, height: {h}, borderRadius: "{rad}", opacity: 1, duration: {dur}, ease: "power3.inOut"}}', t)
    else:
        to('#avframe', f'{{opacity: 0, duration: {dur * 0.6}}}', t)


def words_html(text, cls, ids):
    """One span per word (ids from the read, so each inks in when spoken)."""
    return ' '.join(f'<span class="{cls}" id="{i}">{w}</span>' for w, i in zip(text.split(' '), ids))


def ink(sel, t):
    ft(sel, '{opacity: 0, clipPath: "inset(0% 100% 0% 0%)"}', '{opacity: 1, clipPath: "inset(0% 0% 0% 0%)", duration: 0.35, ease: "power1.out"}', t)


# ── logo: intro card (on screen at frame 0: it is the thumbnail), corner mark, end card ──────────────────────────
ft('#introlockup', '{opacity: 1, scale: 0.94}', '{opacity: 1, scale: 1, duration: 1.3, ease: "power2.out"}', 0)
out('#intro', INTRO - 0.4, 0.4)
ft('#wm', '{opacity: 0, scale: 0.8}', '{opacity: 0.95, scale: 1, duration: 0.5, ease: "back.out(1.6)"}', INTRO + 0.3)
out('#wm', VIDEO_END - 0.6, 0.4)

# ── 1 · hook: « tu ne pries pas pour informer Dieu » — the word gets struck in ink ──────────────────────────────────
ft('#lowshade', '{opacity: 0}', '{opacity: 1, duration: 0.4}', INTRO)
fade('#hook .l1', W('tu', 1.3) - 0.1, 24, 0.5)
fade('#hook .l2', W('informer', 2.4) - 0.1, 30, 0.5)
ft('#hook .strike', '{scaleX: 0}', '{scaleX: 1, duration: 0.45, ease: "power2.out"}', W('besoins?', 3.5))
out('#hook', W('Si', 4.2) - 0.1, 0.35)
out('#lowshade', W('Si', 4.2) - 0.1, 0.4)

# ── 2 · He already knows: the avatar moves into an arch, three notes, each stamped « Il sait » ───────────────────
shape('arch', W('Si', 4.2) - 0.2)
for k, (word, near) in enumerate((('problèmes,', 5.6), ('inquiétudes', 6.5), ('désirs', 7.9))):
    ft(f'#notes .note:nth-child({k + 1})', '{opacity: 0, y: 60, rotation: 0}', f'{{opacity: 1, y: 0, rotation: {(-5, 3, -2)[k]}, duration: 0.5, ease: "back.out(1.5)"}}', W(word, near) - 0.15)
for k, (word, near) in enumerate((('problèmes,', 5.6), ('inquiétudes', 6.5), ('désirs', 7.9))):
    ft(f'#notes .note:nth-child({k + 1}) .stamp', '{opacity: 0, scale: 2.2}', '{opacity: 1, scale: 1, duration: 0.3, ease: "power3.in"}', W(word, near) + 0.55)
to('#notes', '{opacity: 0, y: 40, duration: 0.35, ease: "power2.in"}', W('pourquoi', 9.8) - 0.3)
ft('#why', '{opacity: 0, scale: 0.9}', '{opacity: 1, scale: 1, duration: 0.5, ease: "power2.out"}', W('pourquoi', 9.8) - 0.05)
out('#why', W('Dans', 12.3) - 0.3, 0.3)

# ── 3 · Matthieu 6:8 on a parchment page, inked word by word; the avatar becomes a medallion ─────────────────────
shape('medal', W('Dans', 12.3) - 0.3)
ft('#pages', '{opacity: 0, y: 160}', '{opacity: 1, y: 0, duration: 0.8, ease: "power3.out"}', W('Dans', 12.3) - 0.1)
ft('#p1 .rubric', '{opacity: 0, scaleX: 1.25}', '{opacity: 1, scaleX: 1, duration: 0.6, ease: "power2.out"}', W('Matthieu', 12.5) - 0.05)
V8 = [w for w in WORDS if W('Votre', 15.1) <= w['start'] <= W('demandiez.', 18.7)]
ft('#p1 .drop', '{opacity: 0, scale: 0.6}', '{opacity: 1, scale: 1, duration: 0.45, ease: "back.out(1.6)"}', V8[0]['start'] - 0.1)
for k, w in enumerate(V8):
    ink(f'#v8-{k}', w['start'] - 0.02)
# ── 4 · the page turns to Matthieu 6:9 ──────────────────────────────────────────────────────────────────────────
TURN = W('verset', 21.6) - 0.2
ft('#p1', '{rotationY: 0}', '{rotationY: -180, duration: 1.0, ease: "power2.inOut"}', TURN)
js.append(f'tl.set("#p1", {{opacity: 0}}, {TURN + 0.55:.3f});')
ft('#p2 .rubric', '{opacity: 0, scaleX: 1.25}', '{opacity: 1, scaleX: 1, duration: 0.6, ease: "power2.out"}', TURN + 0.6)
ink('#p2 .intro', W('enseigne', 23.1) - 0.1)
V9 = [w for w in WORDS if W('Notre', 25.0) <= w['start'] <= W('cieux', 26.4)]
ft('#p2 .drop', '{opacity: 0, scale: 0.6}', '{opacity: 1, scale: 1, duration: 0.45, ease: "back.out(1.6)"}', V9[0]['start'] - 0.1)
for k, w in enumerate(V9):
    ink(f'#v9-{k}', w['start'] - 0.02)
ft('#p2 .bang', '{opacity: 0}', '{opacity: 1, duration: 0.3}', V9[-1]['end'])
to('#pages', '{opacity: 0, y: 120, duration: 0.5, ease: "power2.in"}', W('La', 27.2) - 0.25)

# ── 5 · not to inform, but a relation ───────────────────────────────────────────────────────────────────────────
shape('full', W('La', 27.2) - 0.2, 0.9)
ft('#lowshade', '{opacity: 0}', '{opacity: 1, duration: 0.4}', W('La', 27.2))
fade('#rel .r1', W('informer', 28.8) - 0.2, 24, 0.5)
ft('#rel .r1 .strike', '{scaleX: 0}', '{scaleX: 1, duration: 0.4, ease: "power2.out"}', W('mais', 29.8))
to('#rel .r1', '{opacity: 0.45, duration: 0.3}', W('mais', 29.8) + 0.3)
fade('#rel .r2', W('entretenir', 30.4) - 0.2, 30, 0.6)
ft('#rel .uline', '{scaleX: 0}', '{scaleX: 1, duration: 0.6, ease: "power2.inOut"}', W('relation', 31.3))
out('#rel', W('Dieu', 32.9) - 0.2, 0.35)

# ── 6 · not a list: the list crumples, an arch opens on the child running to his father ────────────────────────
ft('#list', '{opacity: 0, y: 80, rotation: 4}', '{opacity: 1, y: 0, rotation: -2, duration: 0.5, ease: "back.out(1.4)"}', W('simplement', 33.5) - 0.1)
for k in range(4):
    ink(f'#list li:nth-child({k + 1})', W('liste', 34.8) - 0.4 + k * 0.28)
CRUMPLE = W('Il', 36.0) - 0.1
to('#list', '{scale: 0.25, rotation: 38, y: 260, opacity: 0, borderRadius: "40%", duration: 0.55, ease: "power3.in"}', CRUMPLE)
out('#lowshade', CRUMPLE, 0.4)
shape('medal', CRUMPLE + 0.1)
ft('#father', '{opacity: 1, clipPath: "inset(100% 0% 0% 0% round 420px 420px 26px 26px)"}',
   '{opacity: 1, clipPath: "inset(0% 0% 0% 0% round 420px 420px 26px 26px)", duration: 1.0, ease: "power3.out"}', CRUMPLE + 0.3)
ft('#father img', '{scale: 1.18}', '{scale: 1.0, duration: 4.5, ease: "power1.out"}', CRUMPLE + 0.3)
to('#father', '{opacity: 0, duration: 0.5}', W('Alors', 40.1) - 0.3)

# ── 7 · « retiens ceci »: hands in prayer behind, the key sentence written word by word ─────────────────────────
shape('arch', W('Alors', 40.1) - 0.3)
ft('#hands', '{opacity: 0}', '{opacity: 1, duration: 0.8}', W('Alors', 40.1) - 0.3)
ft('#hands img', '{scale: 1.0}', '{scale: 1.1, duration: 8, ease: "none"}', W('Alors', 40.1) - 0.3)
fade('#keep .k', W('retiens', 40.6) - 0.1, 14, 0.4)
K1 = [w for w in WORDS if W('la', 41.8) <= w['start'] <= W('ignore,', 44.5)]
K2 = [w for w in WORDS if W('mais', 44.9) <= w['start'] <= W('tout.', 47.5)]
for k, w in enumerate(K1 + K2):
    ft(f'#k-{k}', '{opacity: 0, y: 16, filter: "blur(6px)"}', '{opacity: 1, y: 0, filter: "blur(0px)", duration: 0.35, ease: "power2.out"}', w['start'] - 0.03)
to('#keep .l1', '{opacity: 0.5, duration: 0.4}', W('mais', 44.9))
ft('#keep .uline', '{scaleX: 0}', '{scaleX: 1, duration: 0.7, ease: "power2.inOut"}', W('rapprocher', 45.3) + 0.3)
to('#keep', '{opacity: 0, duration: 0.4}', W('Et', 48.1) - 0.3)
to('#hands', '{opacity: 0, duration: 0.6}', W('Et', 48.1) - 0.3)

# ── 8 · the whispered question: an open hand redraws as a heart ──────────────────────────────────────────────────
shape('full', W('Et', 48.1) - 0.3, 0.9)
ft('#vignette', '{opacity: 0}', '{opacity: 1, duration: 1.4, ease: "power1.inOut"}', W('Et', 48.1))
ft('#ill', '{opacity: 0}', '{opacity: 1, duration: 0.3}', W('main', 51.4) - 0.6)
draw('#hand', W('main', 51.4) - 0.6, 0.9)
to('#hand', '{opacity: 0, duration: 0.35}', W('cœur?', 52.8) - 0.45)
draw('#heart', W('cœur?', 52.8) - 0.2, 0.9)
ft('#heart .fillh', '{opacity: 0}', '{opacity: 0.35, duration: 0.6}', W('cœur?', 52.8) + 0.5)

# ── end card ────────────────────────────────────────────────────────────────────────────────────────────────────
ft('#endbg', '{opacity: 0}', '{opacity: 1, duration: 0.7, ease: "power1.inOut"}', VIDEO_END - 0.5)
to('#ill', '{y: -560, scale: 0.7, duration: 0.9, ease: "power2.inOut"}', VIDEO_END - 0.45)
fade('#endq', VIDEO_END - 0.1, 24, 0.7)
ft('#endlockup', '{opacity: 0, y: 30}', '{opacity: 1, y: 0, duration: 0.8, ease: "power2.out"}', VIDEO_END + 0.5)
ft('#fade', '{opacity: 0}', '{opacity: 1, duration: 0.9, ease: "power2.in"}', END - 0.9)


# ── karaoke captions: the spoken word sits on a framboise pill; hidden where the screen already writes the words ──
HIDE = [(0, W('Si', 4.2) - 0.1), (W('Dans', 12.3) - 0.1, W('La', 27.2) - 0.1), (W('Alors', 40.1) - 0.1, W('Et', 48.1) - 0.1)]


def chunks():
    res, cur = [], []
    for w in WORDS:
        cur.append(w)
        if len(cur) >= 5 or (re.search(r'[,:.…?!;»]$', w['text']) and len(cur) >= 2):
            res.append(cur); cur = []
    if cur: res.append(cur)
    return res


cap_html = []
CH = chunks()
for k, ch in enumerate(CH):
    if any(a <= ch[0]['start'] < b for a, b in HIDE): continue
    nxt = CH[k + 1][0]['start'] if k + 1 < len(CH) else ch[-1]['end'] + 0.5
    stop = min(nxt, ch[-1]['end'] + 0.7, VIDEO_END - 0.5) - 0.05
    cid = f'c{k}'
    spans = []
    for i, w in enumerate(ch):
        text = w['text'].replace('6,8,', '6:8').replace('?', ' ?').replace('«', '').replace('»', '').replace('».', '.').strip()
        if not text: continue
        spans.append(f'<span class="cw{" ck" if norm(w["text"]) in KEYS else ""}" id="{cid}-{i}">{text}</span>')
        ft(f'#{cid}-{i}', '{backgroundColor: "rgba(155,46,94,0)"}', f'{{backgroundColor: "rgba(155,46,94,1)", duration: 0.08, ease: "none"}}', w['start'])
        to(f'#{cid}-{i}', '{backgroundColor: "rgba(155,46,94,0)", duration: 0.12, ease: "none"}', max(w['start'] + 0.1, min(w['end'], stop - 0.05)))
    cap_html.append(f'      <div class="s-caption" id="{cid}">{" ".join(spans)}</div>')
    ft(f'#{cid}', '{opacity: 0, y: 14}', '{opacity: 1, y: 0, duration: 0.18, ease: "power2.out"}', ch[0]['start'] - 0.05)
    js.append(f'tl.set("#{cid}", {{opacity: 0}}, {stop:.3f});')

v8_html = words_html(' '.join(w['text'] for w in V8).replace('Votre', 'otre').replace('»', '').strip(), 'iw', [f'v8-{k}' for k in range(len(V8))])
v9_html = words_html(' '.join(w['text'] for w in V9).replace('Notre', 'otre').replace('est', 'es').replace('».', '').replace('»', '').strip(), 'iw', [f'v9-{k}' for k in range(len(V9))])
k_ids = iter(f'k-{k}' for k in range(len(K1 + K2)))
k1_html = ' '.join(f'<span class="kw" id="{next(k_ids)}">{w["text"]}</span>' for w in K1)
K2_TXT = [w['text'] for w in K2]
k2_spans = [f'<span class="kw" id="{next(k_ids)}">{t}</span>' for t in K2_TXT]
ri = K2_TXT.index('te')  # « te rapprocher » carries the drawn underline
k2_html = ' '.join(k2_spans[:ri]) + f' <span class="hl">{k2_spans[ri]} {k2_spans[ri + 1]}<span class="uline"></span></span> ' + ' '.join(k2_spans[ri + 2:])

HAND = ('<path class="dr" pathLength="1" d="M70 214 C58 176 44 140 40 112 C38 98 54 94 60 108 L72 146"/>'
        '<path class="dr" pathLength="1" d="M72 146 L64 60 C63 46 82 44 84 58 L92 132"/>'
        '<path class="dr" pathLength="1" d="M92 132 L94 42 C94 28 114 28 114 42 L114 130"/>'
        '<path class="dr" pathLength="1" d="M114 130 L122 56 C124 42 143 45 141 59 L134 138"/>'
        '<path class="dr" pathLength="1" d="M134 138 L148 100 C153 88 170 94 165 108 L146 168 C138 192 124 208 104 216 L70 214"/>')
HEART = ('<path class="fillh" d="M110 206 C50 160 18 126 18 88 C18 56 42 34 70 34 C90 34 104 46 110 62 C116 46 130 34 150 34 C178 34 202 56 202 88 C202 126 170 160 110 206 Z" fill="#9B2E5E" stroke="none" opacity="0"/>'
         '<path class="dr" pathLength="1" d="M110 206 C50 160 18 126 18 88 C18 56 42 34 70 34 C90 34 104 46 110 62 C116 46 130 34 150 34 C178 34 202 56 202 88 C202 126 170 160 110 206 Z"/>')
NOISE = ('<svg class="grain" aria-hidden="true"><filter id="{id}"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="3" seed="7"/>'
         '<feColorMatrix values="0 0 0 0 .35  0 0 0 0 .25  0 0 0 0 .12  0 0 0 .55 0"/></filter><rect width="100%" height="100%" filter="url(#{id})"/></svg>')

CSS = """
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #110D0A; }
      @font-face { font-family: "Cormorant"; font-weight: 500; src: url("assets/fonts/CG-Medium.ttf"); }
      @font-face { font-family: "Cormorant"; font-weight: 600; src: url("assets/fonts/CG-SemiBold.ttf"); }
      @font-face { font-family: "Cormorant"; font-weight: 500; font-style: italic; src: url("assets/fonts/CG-MediumItalic.ttf"); }
      @font-face { font-family: "Caveat"; src: url("assets/fonts/Caveat.ttf"); }
      #root { position: relative; width: 100%; height: 100%; overflow: hidden; background: #110D0A; color: #F5EFE6; font-family: "DM Sans", sans-serif; }
      #avwrap { position: absolute; inset: 0; clip-path: inset(0px 0px 0px 0px round 0px 0px 0px 0px); }
      #avatar { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
      #avgrade { position: absolute; inset: 0; background: linear-gradient(rgba(17,13,10,.55) 0%, rgba(17,13,10,0) 18%, rgba(17,13,10,0) 58%, rgba(17,13,10,.5) 74%, rgba(17,13,10,.85) 100%); }
      #avframe { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; border: 3px solid rgba(226,184,102,.85); box-shadow: 0 0 0 10px rgba(226,184,102,.12), 0 30px 80px rgba(0,0,0,.55); opacity: 0; }
      #lowshade { position: absolute; left: 0; right: 0; bottom: 0; height: 1000px; opacity: 0; background: linear-gradient(rgba(17,13,10,0) 0%, rgba(17,13,10,.72) 42%, rgba(17,13,10,.9) 100%); }
      #vignette { position: absolute; inset: 0; opacity: 0; background: radial-gradient(ellipse 760px 900px at 50% 30%, rgba(8,6,5,0) 35%, rgba(8,6,5,.6) 75%, rgba(8,6,5,.9) 100%); }
      .serif { font-family: "Instrument Serif", serif; line-height: 1.05; text-shadow: 0 6px 36px rgba(0,0,0,.65); }
      .it { font-style: italic; color: #E2B866; }
      .kick { font-size: 24px; font-weight: 700; letter-spacing: .3em; text-transform: uppercase; color: #E2B866; }
      .strike { position: absolute; left: -10px; right: -10px; top: 56%; height: 7px; border-radius: 4px; background: #C2185B; transform: scaleX(0); transform-origin: 0 50%; }
      #hook { position: absolute; left: 60px; right: 60px; top: 1130px; text-align: center; }
      #hook .l1 { font-size: 78px; opacity: 0; }
      #hook .l2 { font-size: 132px; opacity: 0; margin-top: 4px; }
      #hook .w { position: relative; display: inline-block; }
      #notes { position: absolute; left: 40px; right: 40px; top: 1080px; display: flex; justify-content: center; gap: 26px; }
      .note { position: relative; z-index: 1; width: 300px; padding: 34px 20px 46px; background: #FBF3DF; color: #2A1A12; border-radius: 4px; box-shadow: 0 18px 40px rgba(0,0,0,.5); font-family: "Caveat", cursive; font-size: 54px; line-height: 1; text-align: center; opacity: 0; }
      .note::before { content: ""; position: absolute; left: 50%; top: -14px; width: 90px; height: 28px; margin-left: -45px; background: rgba(226,184,102,.55); }
      .stamp { position: absolute; left: 50%; margin-left: -75px; bottom: -84px; z-index: 2; width: 150px; height: 150px; border-radius: 50%; border: 5px solid #B8862E; color: #B8862E; background: rgba(251,243,223,.9); display: flex; align-items: center; justify-content: center; font-family: "DM Sans", sans-serif; font-weight: 700; font-size: 27px; letter-spacing: .12em; transform: rotate(-14deg); opacity: 0; }
      #why { position: absolute; left: 0; right: 0; top: 1110px; text-align: center; font-size: 150px; opacity: 0; }
      #pages { position: absolute; left: 70px; right: 70px; top: 790px; height: 920px; perspective: 2400px; opacity: 0; }
      .page { position: absolute; inset: 0; padding: 70px 70px 60px; border-radius: 10px; overflow: hidden; color: #2A1A12; backface-visibility: hidden; transform-origin: 0% 50%;
              background: radial-gradient(ellipse at 45% 35%, #F6EBD2 0%, #EBDBB8 55%, #CFB585 100%); box-shadow: 0 34px 90px rgba(0,0,0,.6), inset 0 0 60px rgba(120,80,30,.35); }
      .grain { position: absolute; inset: 0; width: 100%; height: 100%; mix-blend-mode: multiply; opacity: .5; pointer-events: none; }
      .rubric { position: relative; text-align: center; font-family: "Cormorant", serif; font-weight: 600; font-size: 34px; letter-spacing: .32em; color: #9B2E5E; opacity: 0; }
      .rule { position: relative; margin: 22px auto 34px; width: 300px; height: 2px; background: linear-gradient(90deg, rgba(155,46,94,0), rgba(155,46,94,.7), rgba(155,46,94,0)); }
      .vtext { position: relative; font-family: "Cormorant", serif; font-weight: 500; font-size: 80px; line-height: 1.18; }
      .drop { float: left; font-family: "Cormorant", serif; font-weight: 600; font-size: 214px; line-height: .78; margin: 10px 18px 0 0; color: #9B2E5E; opacity: 0; }
      .iw { display: inline-block; opacity: 0; }
      .intro { position: relative; display: block; font-family: "Cormorant", serif; font-style: italic; font-size: 46px; color: #6B5038; margin-bottom: 26px; opacity: 0; }
      #p2 .vtext { font-style: italic; font-size: 92px; line-height: 1.12; }
      #p2 .drop { font-style: normal; font-size: 250px; }
      .src { position: absolute; left: 0; right: 0; bottom: 44px; text-align: center; font-family: "DM Sans", sans-serif; font-weight: 700; font-size: 22px; letter-spacing: .24em; color: #5A4128; }
      #rel { position: absolute; left: 60px; right: 60px; top: 1110px; text-align: center; }
      #rel .r1 { position: relative; display: inline-block; font-size: 90px; color: #D8CDBE; opacity: 0; }
      #rel .r2 { margin-top: 18px; font-size: 104px; opacity: 0; }
      #rel .hl { position: relative; display: inline-block; }
      .uline { position: absolute; left: 0; right: 0; bottom: -6px; height: 6px; border-radius: 3px; background: #C2185B; transform: scaleX(0); transform-origin: 0 50%; }
      #list { position: absolute; left: 230px; width: 620px; top: 1020px; padding: 40px 50px 44px; background: #FBF3DF; color: #2A1A12; border-radius: 6px; box-shadow: 0 24px 60px rgba(0,0,0,.55); opacity: 0;
              background-image: repeating-linear-gradient(transparent 0 63px, rgba(70,110,170,.25) 63px 65px); background-position: 0 92px; }
      #list h3 { font-family: "Caveat", cursive; font-size: 66px; font-weight: 700; color: #9B2E5E; }
      #list ul { list-style: none; margin-top: 4px; }
      #list li { font-family: "Caveat", cursive; font-size: 54px; line-height: 64px; opacity: 0; }
      .arch { position: absolute; left: 150px; right: 150px; top: 780px; height: 680px; overflow: hidden; opacity: 0; box-shadow: 0 30px 80px rgba(0,0,0,.6); }
      .arch img, .full img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
      .archframe { position: absolute; inset: 0; border: 3px solid rgba(226,184,102,.85); border-radius: 420px 420px 26px 26px; }
      .full { position: absolute; inset: 0; overflow: hidden; opacity: 0; }
      .full .sh { position: absolute; inset: 0; background: linear-gradient(rgba(17,13,10,.55), rgba(17,13,10,.25) 40%, rgba(17,13,10,.86) 62%, rgba(17,13,10,.95)); }
      #keep { position: absolute; left: 70px; right: 70px; top: 1090px; text-align: center; }
      #keep .k { opacity: 0; margin-bottom: 26px; }
      #keep .l1 { font-size: 54px; color: #E9DFCF; }
      #keep .l2 { margin-top: 22px; font-size: 80px; }
      .kw { display: inline-block; opacity: 0; }
      #keep .hl { position: relative; display: inline-block; color: #F0B9D0; font-style: italic; }
      #ill { position: absolute; left: 0; right: 0; top: 1020px; height: 360px; display: flex; justify-content: center; opacity: 0; }
      #ill svg { position: absolute; top: 0; overflow: visible; }
      .dr { fill: none; stroke: #E2B866; stroke-width: 5; stroke-linecap: round; stroke-linejoin: round; stroke-dasharray: 1; stroke-dashoffset: 1; }
      #heart .dr { stroke: #F0B9D0; }
      #endbg { position: absolute; inset: 0; opacity: 0; }
      #endq { position: absolute; left: 70px; right: 70px; top: 780px; text-align: center; font-size: 96px; opacity: 0; }
      #intro { position: absolute; inset: 0; }
      #introlockup { position: absolute; left: 50%; top: 660px; width: 520px; margin-left: -260px; }
      #endlockup { position: absolute; left: 50%; top: 1160px; width: 430px; margin-left: -215px; opacity: 0; }
      #wm { position: absolute; """ + LOGO_POS_CSS[LOGO_POSITION] + """ width: 104px; opacity: 0; }
      #fade { position: absolute; inset: 0; background: #080605; opacity: 0; }
      .s-caption { top: 1520px; }
      .s-caption .cw { padding: 2px 12px; margin: 0 -6px; border-radius: 12px; }
      .s-caption .ck { color: #F7D27E; }
"""

html = f"""<!doctype html>
<html lang="fr" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <link rel="stylesheet" href="assets/sermon.css" />
    <style>{CSS}    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{END}" data-width="1080" data-height="1920">
      <div id="bg" class="s-bg"><div class="s-glow-a"></div><div class="s-glow-b"></div><div class="s-dust"></div></div>
      <div id="hands" class="full"><img src="assets/img/hands.jpg" alt="" /><div class="sh"></div></div>
      <div id="father" class="arch" style="border-radius: 420px 420px 26px 26px"><img src="assets/img/father.jpg" alt="" /><div class="archframe"></div></div>
      <div id="pages">
        <div id="p2" class="page">{NOISE.format(id="g2")}<div class="rubric">MATTHIEU 6 · 9</div><div class="rule"></div>
          <div class="vtext"><span class="intro">Voici donc comment vous devez prier :</span><span class="drop">N</span>{v9_html}<span class="iw bang">&#8239;!</span></div><div class="src">LOUIS SEGOND 1910</div></div>
        <div id="p1" class="page">{NOISE.format(id="g1")}<div class="rubric">MATTHIEU 6 · 8</div><div class="rule"></div>
          <div class="vtext"><span class="drop">V</span>{v8_html}</div><div class="src">LOUIS SEGOND 1910</div></div>
      </div>
      <div id="avwrap"><video id="avatar" class="clip" src="source/avatar.mp4" muted playsinline data-start="{INTRO}" data-duration="{VIDEO_LEN}" data-track-index="1"></video><div id="avgrade"></div></div>
      <div id="avframe"></div>
      <div id="lowshade"></div>
      <div id="vignette"></div>

      <div id="hook"><div class="l1 serif">Tu ne pries pas pour</div><div class="l2 serif"><span class="w it">informer<span class="strike"></span></span> Dieu</div></div>
      <div id="notes"><div class="note">mes problèmes<div class="stamp">IL SAIT</div></div><div class="note">mes inquiétudes<div class="stamp">IL SAIT</div></div><div class="note">mes désirs<div class="stamp">IL SAIT</div></div></div>
      <div id="why" class="serif">Pourquoi <span class="it">prier</span>&#8239;?</div>
      <div id="rel"><div class="r1 serif">informer Dieu<span class="strike"></span></div><div class="r2 serif">entretenir ta <span class="hl it">relation<span class="uline"></span></span></div></div>
      <div id="list"><h3>Ma liste…</h3><ul><li>un travail</li><li>la guérison</li><li>une solution</li><li>de l’argent</li></ul></div>
      <div id="keep"><div class="k kick">Retiens ceci</div><div class="l1 serif">{k1_html}</div><div class="l2 serif">{k2_html}</div></div>
{chr(10).join(cap_html)}
      <div id="endbg" class="s-bg"><div class="s-glow-a"></div><div class="s-glow-b"></div><div class="s-dust"></div></div>
      <div id="ill"><svg id="hand" width="330" height="360" viewBox="0 0 220 240" aria-hidden="true">{HAND}</svg><svg id="heart" width="330" height="360" viewBox="0 0 220 240" aria-hidden="true">{HEART}</svg></div>
      <div id="endq" class="serif">La <span class="it">main</span> de Dieu…<br />ou aussi son <span class="it" style="color:#F0B9D0">cœur</span>&#8239;?</div>
      <img id="wm" src="assets/brand/enracinee-monogram-a-filled-ondark.svg" alt="Enracinée" />
      <img id="endlockup" src="assets/brand/enracinee-lockup-a-vertical-ondark.svg" alt="Enracinée avec Adeline Nana" />
      <div id="intro" class="s-bg"><div class="s-glow-a"></div><div class="s-glow-b"></div><div class="s-dust"></div>
        <img id="introlockup" src="assets/brand/enracinee-lockup-a-vertical-ondark.svg" alt="Enracinée avec Adeline Nana" /></div>
      <div id="fade"></div>
      <audio id="mix" src="assets/mix.wav" data-start="0" data-duration="{END}" data-track-index="9" data-volume="1"></audio>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      tl.fromTo(".s-glow-a", {{ x: 0, y: 0, scale: 1 }}, {{ x: 90, y: 60, scale: 1.08, duration: 4, ease: "sine.inOut", yoyo: true, repeat: 14 }}, 0);
      tl.fromTo(".s-glow-b", {{ x: 0, y: 0 }}, {{ x: -80, y: -70, duration: 4, ease: "sine.inOut", yoyo: true, repeat: 14 }}, 0);
{chr(10).join('      ' + j for j in js)}
      tl.to({{}}, {{ duration: {END} }}, 0);
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
open(os.path.join(ROOT, 'index.html'), 'w').write(html)
print('index.html', len(js), 'tweens', len(CH), 'caption chunks', 'END', END)
