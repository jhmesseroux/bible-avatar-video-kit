# Build « Le silence de Dieu »: style « de la nuit à l'aube ». The HeyGen avatar read sits under a starry night sky
# (full frame → moon medallion → arch); prayer lanterns rise unanswered, the Psaume 13 verse lights letter by letter
# like stars, then the psalm scrolls from verse 2 to verse 6 while the sky turns to dawn. A candle keeps burning, a
# dawn painting carries the takeaway. Karaoke captions, « Enracinée avec Adeline Nana » logo (intro card, corner
# mark, end card). usage: python3 build.py
import json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
INTRO = 1.6  # logo card before the avatar; every voice-synced time below is shifted by it
WORDS = [dict(w, start=w['start'] + INTRO, end=w['end'] + INTRO)
         for w in json.load(open(os.path.join(ROOT, 'source/transcript.json'))) if re.search(r'\w', w['text'])]
VIDEO_LEN = 54.68
VIDEO_END = INTRO + VIDEO_LEN
END = round(VIDEO_END + 2.8, 2)
LOGO_POSITION = 'top-right'  # corner mark, switch per video
LOGO_POS_CSS = {'top-right': 'right: 40px; top: 52px;', 'top-left': 'left: 40px; top: 52px;',
                'bottom-right': 'right: 40px; bottom: 260px;', 'bottom-left': 'left: 40px; bottom: 260px;'}
KEYS = {'dieu', 'dieu.', 'silence', 'absence?', 'david', 'confiance', 'bonté.', 'silencieux?', 'foi,', 'parler.'}
FIX = {'éternelle,': 'Éternel !', 'abandonnée.': 'abandonné.', "s'écrit": "s'écrie"}  # Whisper slips, per the script
SILVER, GOLD = 'rgba(201,214,234,.85)', 'rgba(226,184,102,.9)'
js = []


def norm(s):
    return re.sub(r'[^\w’\'-]', '', s).lower().replace('’', "'")


def W(word, near, edge='start'):
    near += INTRO  # `near` is given on the source read's clock
    hits = [w for w in WORDS if norm(word) == norm(w['text'])]
    best = min(hits, key=lambda w: abs(w['start'] - near))
    assert abs(best['start'] - near) < 1.5, f'« {word} » expected near {near}s, nearest at {best["start"]}s'
    return best[edge]


def span(a, b):
    return [w for w in WORDS if a <= w['start'] <= b]


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


def blur_in(sel, t):
    ft(sel, '{opacity: 0, y: 16, filter: "blur(6px)"}', '{opacity: 1, y: 0, filter: "blur(0px)", duration: 0.35, ease: "power2.out"}', t)


def ink(sel, t):
    ft(sel, '{opacity: 0, clipPath: "inset(0% 100% 0% 0%)"}', '{opacity: 1, clipPath: "inset(0% 0% 0% 0%)", duration: 0.35, ease: "power1.out"}', t)


def text(w):
    return FIX.get(w['text'], w['text']).replace('?', ' ?').replace('!', ' !').replace('«', '').replace('»', '').strip()


class Rand:  # deterministic LCG: star field and letter order are the same on every build
    def __init__(self, seed): self.s = seed
    def __call__(self):
        self.s = (self.s * 1103515245 + 12345) % 2 ** 31
        return self.s / 2 ** 31


# ── the avatar's shape: full frame, moon medallion around the face, or arch; a silver→gold frame follows it ─────────
SHAPES = {  # clip inset (top right bottom left) + radii, and the matching frame box
    'full': ('0px 0px 0px 0px', '0px 0px 0px 0px', None),
    'moon': ('250px 330px 1210px 290px', '230px 230px 230px 230px', (290, 250, 460, 460)),
    'arch': ('190px 230px 900px 190px', '330px 330px 34px 34px', (190, 190, 660, 830)),
}


def shape(name, t, dur=0.8):
    ins, rad, box = SHAPES[name]
    to('#avwrap', f'{{clipPath: "inset({ins} round {rad})", duration: {dur}, ease: "power3.inOut"}}', t)
    if box:
        x, y, w, h = box
        to('#avframe', f'{{x: {x}, y: {y}, width: {w}, height: {h}, borderRadius: "{rad}", opacity: 1, duration: {dur}, ease: "power3.inOut"}}', t)
    else:
        to('#avframe', f'{{opacity: 0, duration: {dur * 0.6}}}', t)


def stars_svg(cls, n, seed, h=1920):
    r = Rand(seed)
    dots = ''.join(f'<circle cx="{r() * 1080:.0f}" cy="{r() * h:.0f}" r="{0.8 + r() * r() * 2.6:.1f}" opacity="{0.35 + r() * 0.65:.2f}"/>' for _ in range(n))
    return f'<svg class="{cls}" viewBox="0 0 1080 {h}" aria-hidden="true">{dots}</svg>'


STARS = ''.join(stars_svg(f'stars s{k}', 70, 11 + k * 7) for k in range(3))


# ── logo: intro card (on screen at frame 0: it is the thumbnail), corner mark, end card ──────────────────────────
ft('#introlockup', '{opacity: 1, scale: 0.94}', '{opacity: 1, scale: 1, duration: 1.3, ease: "power2.out"}', 0)
out('#intro', INTRO - 0.4, 0.4)
ft('#wm', '{opacity: 0, scale: 0.8}', '{opacity: 0.95, scale: 1, duration: 0.5, ease: "back.out(1.6)"}', INTRO + 0.3)
out('#wm', VIDEO_END - 0.6, 0.4)
for k, d in enumerate((1.7, 2.3, 2.9)):  # the stars twinkle all along
    ft(f'#root .s{k}', '{opacity: 1}', f'{{opacity: 0.35, duration: {d}, ease: "sine.inOut", yoyo: true, repeat: {int(END / d)}}}', 0)

# ── 1 · hook: silence ≠ absence ─────────────────────────────────────────────────────────────────────────────────
ft('#lowshade', '{opacity: 0}', '{opacity: 1, duration: 0.4}', INTRO)
fade('#hook .kick', W('Et', 0.1), 14, 0.4)
fade('#hook .a', W('silence', 1.4) - 0.1, 24, 0.5)
ft('#hook .neq .dr', '{strokeDashoffset: 1}', '{strokeDashoffset: 0, duration: 0.5, ease: "power2.out", stagger: 0.15}', W('pas', 3.2) - 0.1)
fade('#hook .b', W('absence?', 4.2) - 0.35, 24, 0.5)
out('#hook', W('As-tu', 5.3) - 0.25, 0.35)
out('#lowshade', W('As-tu', 5.3) - 0.25, 0.4)

# ── 2 · prayers rise like lanterns into the night… and no answer comes back ──────────────────────────────────────
shape('moon', W('As-tu', 5.3) - 0.3)
for k, (word, near) in enumerate((('prié', 6.0), ('encore', 7.6), ('encore', 8.3))):
    t = W(word, near) - 0.1
    ft(f'#lanterns .ln:nth-child({k + 1})', '{opacity: 0, y: 0, scale: 0.7}', '{opacity: 1, y: -160, scale: 1, duration: 0.7, ease: "power2.out"}', t)
    to(f'#lanterns .ln:nth-child({k + 1})', '{y: -720, opacity: 0, scale: 0.55, duration: 3.6, ease: "power1.in"}', t + 0.7)
ft('#noans', '{opacity: 0, y: 30}', '{opacity: 1, y: 0, duration: 0.5, ease: "back.out(1.5)"}', W('sans', 8.9) - 0.05)
for k in range(3):
    ft(f'#noans .dot:nth-child({k + 1})', '{opacity: 0.25}', '{opacity: 1, duration: 0.35, ease: "sine.inOut", yoyo: true, repeat: 7}', W('sans', 8.9) + 0.3 + k * 0.18)
out('#noans', W('Tu', 11.3) - 0.2, 0.3)

# ── 3 · « Seigneur, est-ce que tu m'entends vraiment ? » on a small prayer note ──────────────────────────────────
Q = span(W('Seigneur,', 13.3), W('vraiment?', 15.1))
ft('#note', '{opacity: 0, y: 70, rotation: 3}', '{opacity: 1, y: 0, rotation: -2, duration: 0.55, ease: "back.out(1.4)"}', W('demander', 12.5) - 0.2)
for k, w in enumerate(Q):
    ink(f'#q-{k}', w['start'] - 0.02)
ft('#note', '{x: 0}', '{x: 4, duration: 0.09, ease: "sine.inOut", yoyo: true, repeat: 5}', W('vraiment?', 15.1) + 0.3)
to('#note', '{opacity: 0, y: 50, duration: 0.4, ease: "power2.in"}', W('Tu', 16.0) - 0.15)

# ── 4 · David at night, Psaume 13 ───────────────────────────────────────────────────────────────────────────────
ft('#david', '{opacity: 1, clipPath: "inset(100% 0% 0% 0% round 420px 420px 26px 26px)"}',
   '{opacity: 1, clipPath: "inset(0% 0% 0% 0% round 420px 420px 26px 26px)", duration: 1.0, ease: "power3.out"}', W('David', 17.1) - 0.3)
ft('#david img', '{scale: 1.15}', '{scale: 1.0, duration: 5, ease: "power1.out"}', W('David', 17.1) - 0.3)
ft('#pchip', '{opacity: 0, y: 20}', '{opacity: 1, y: 0, duration: 0.45, ease: "back.out(1.6)"}', W('psaume', 19.3) - 0.05)
to('#david', '{opacity: 0, duration: 0.45}', W("Jusqu'à", 21.1) - 0.5)
out('#pchip', W("Jusqu'à", 21.1) - 0.5, 0.3)

# ── 5 · Psaume 13:2 lights up letter by letter, like stars ─────────────────────────────────────────────────────
ft('#psalm', '{opacity: 0, y: 80}', '{opacity: 1, y: 0, duration: 0.7, ease: "power3.out"}', W("Jusqu'à", 21.1) - 0.45)
ft('#b2 .rubric', '{opacity: 0, scaleX: 1.3}', '{opacity: 1, scaleX: 1, duration: 0.7, ease: "power2.out"}', W("Jusqu'à", 21.1) - 0.3)
V2 = span(W("Jusqu'à", 21.1), W('cesse?', 24.1))
rnd = Rand(5)
v2_html = []
for k, w in enumerate(V2):
    letters = list(text(w).replace(' ', ' '))
    order = sorted(range(len(letters)), key=lambda i: rnd())
    dur = max(0.25, min(w['end'] - w['start'], 0.55))
    v2_html.append('<span class="vw">' + ''.join(f'<span class="st" id="l{k}-{i}">{c if c != " " else "&#8239;"}</span>' for i, c in enumerate(letters)) + '</span>')
    for rank, i in enumerate(order):
        t = w['start'] - 0.05 + dur * rank / len(letters)
        ft(f'#l{k}-{i}', '{opacity: 0, scale: 1.8, textShadow: "0 0 0px rgba(235,242,255,0)"}',
           '{opacity: 1, scale: 1, textShadow: "0 0 22px rgba(235,242,255,1)", duration: 0.22, ease: "power2.out"}', t)
        to(f'#l{k}-{i}', '{textShadow: "0 0 8px rgba(235,242,255,.35)", duration: 0.6, ease: "power1.out"}', t + 0.22)

# ── 6 · « à la fin de ce même psaume »: the psalm scrolls to verse 6 while the night turns to dawn ──────────────
to('#b2', '{opacity: 0.4, duration: 0.5}', W('surprenant,', 25.4))
SCROLL = W('fin', 26.9) - 0.3
to('#col', f'{{y: -1190, duration: {W("Moi,", 29.6) - 0.35 - SCROLL:.2f}, ease: "power2.inOut"}}', SCROLL)
ft('#dawn', '{opacity: 0}', '{opacity: 1, duration: 3.2, ease: "power1.inOut"}', SCROLL)
ft('#sun', '{opacity: 0, y: 260}', '{opacity: 1, y: 0, duration: 3.6, ease: "power2.out"}', SCROLL + 0.2)
to('#sky .stars', '{opacity: 0.12, duration: 3, ease: "power1.in"}', SCROLL)
to('#psalm', f'{{backgroundColor: "rgba(44,28,20,.62)", borderColor: "{GOLD}", duration: 2.5, ease: "power1.inOut"}}', SCROLL + 0.5)
to('#avframe', f'{{borderColor: "{GOLD}", duration: 2.5, ease: "power1.inOut"}}', SCROLL + 0.5)
ft('#b6 .rubric', '{opacity: 0.3}', '{opacity: 1, duration: 0.6}', W('Moi,', 29.6) - 0.5)
V6 = span(W('Moi,', 29.6), W('bonté.', 31.4))
for k, w in enumerate(V6):
    ft(f'#v6-{k}', '{opacity: 0.18, color: "#E9E2D6", textShadow: "0 0 0px rgba(240,190,110,0)"}',
       '{opacity: 1, color: "#F2C879", textShadow: "0 0 28px rgba(240,190,110,.75)", duration: 0.45, ease: "power2.out"}', w['start'] - 0.03)
out('#psalm', W('Sa', 32.2) - 0.25, 0.4)

# ── 7 · not resolved… but he chooses trust ───────────────────────────────────────────────────────────────────────
shape('full', W('Sa', 32.2) - 0.3, 0.9)
ft('#lowshade', '{opacity: 0}', '{opacity: 1, duration: 0.4}', W('Sa', 32.2))
fade('#choice .r1', W('présentée', 33.3) - 0.2, 24, 0.5)
ft('#choice .r1 .strike', '{scaleX: 0}', '{scaleX: 1, duration: 0.4, ease: "power2.out"}', W('mais', 35.0) - 0.1)
to('#choice .r1', '{opacity: 0.45, duration: 0.3}', W('mais', 35.0) + 0.3)
fade('#choice .r2', W('choisit', 35.3) - 0.1, 30, 0.6)
ft('#choice .uline', '{scaleX: 0}', '{scaleX: 1, duration: 0.6, ease: "power2.inOut"}', W('confiance', 36.9))
out('#choice', W('Le', 38.1) - 0.25, 0.35)
out('#lowshade', W('Le', 38.1) - 0.25, 0.4)

# ── 8 · a candle keeps burning: his silence is not abandonment ───────────────────────────────────────────────────
shape('moon', W('Le', 38.1) - 0.3)
ft('#vignette', '{opacity: 0}', '{opacity: 1, duration: 0.8}', W('Le', 38.1) - 0.3)
ft('#candle', '{opacity: 0}', '{opacity: 1, duration: 0.3}', W('Le', 38.1) - 0.2)
draw('#candle', W('Le', 38.1) - 0.2, 0.7)
ft('#candle .flame', '{opacity: 0, scale: 0.2}', '{opacity: 1, scale: 1, duration: 0.5, ease: "back.out(2)"}', W('silence', 38.1) + 0.4)
ft('#candle .flame', '{scaleY: 1, rotation: 0}', '{scaleY: 1.12, rotation: 3, duration: 0.42, ease: "sine.inOut", yoyo: true, repeat: 6}', W('silence', 38.1) + 0.9)
ft('#candle .glow', '{opacity: 0}', '{opacity: 1, duration: 0.8}', W('silence', 38.1) + 0.5)
fade('#aband .kick', W('silence', 38.1), 14, 0.4)
fade('#aband .l2', W("n'est", 38.9) - 0.1, 24, 0.5)
ft('#aband .uline', '{scaleX: 0}', '{scaleX: 1, duration: 0.5, ease: "power2.inOut"}', W('abandonnée.', 40.4))
out('#aband', W('Alors', 41.2) - 0.25, 0.35)
out('#candle', W('Alors', 41.2) - 0.25, 0.35)
out('#vignette', W('Alors', 41.2) - 0.25, 0.5)

# ── 9 · dawn painting: « continue de lui parler », then the takeaway ──────────────────────────────────────────────
shape('arch', W('Alors', 41.2) - 0.3)
ft('#aube', '{opacity: 0}', '{opacity: 1, duration: 0.8}', W('Alors', 41.2) - 0.3)
ft('#aube img', '{scale: 1.0}', '{scale: 1.1, duration: 9.5, ease: "none"}', W('Alors', 41.2) - 0.3)
C1 = span(W('même', 41.5), W('pas,', 42.9))
C2 = span(W('continue', 43.2), W('parler.', 44.3))
for k, w in enumerate(C1 + C2):
    blur_in(f'#c-{k}', w['start'] - 0.03)
ft('#talk .uline', '{scaleX: 0}', '{scaleX: 1, duration: 0.5, ease: "power2.inOut"}', W('parler.', 44.3) + 0.2)
out('#talk', W('Car', 44.9) - 0.15, 0.3)
fade('#keep .k', W('foi,', 45.1) - 0.1, 14, 0.4)
K1 = span(W('croire', 46.4), W('répond,', 47.3))
K2 = span(W('lui', 48.4), W('attends.', 49.8))
for k, w in enumerate(K1 + K2):
    blur_in(f'#k-{k}', w['start'] - 0.03)
to('#keep .l1', '{opacity: 0.5, duration: 0.4}', W("c'est", 47.9))
ft('#keep .uline', '{scaleX: 0}', '{scaleX: 1, duration: 0.7, ease: "power2.inOut"}', W('attends.', 49.8) + 0.3)
to('#keep', '{opacity: 0, duration: 0.4}', W('Et', 50.5) - 0.3)
to('#aube', '{opacity: 0, duration: 0.6}', W('Et', 50.5) - 0.3)

# ── 10 · the question, then a sunrise drawn above it on the end card ──────────────────────────────────────────────
shape('full', W('Et', 50.5) - 0.3, 0.9)
ft('#warm', '{opacity: 0}', '{opacity: 1, duration: 1.4, ease: "power1.inOut"}', W('Et', 50.5))
ft('#endbg', '{opacity: 0}', '{opacity: 1, duration: 0.7, ease: "power1.inOut"}', VIDEO_END - 0.5)
ft('#sunrise', '{opacity: 0}', '{opacity: 1, duration: 0.3}', VIDEO_END - 0.3)
draw('#sunrise', VIDEO_END - 0.3, 0.9)
fade('#endq', VIDEO_END - 0.1, 24, 0.7)
ft('#endlockup', '{opacity: 0, y: 30}', '{opacity: 1, y: 0, duration: 0.8, ease: "power2.out"}', VIDEO_END + 0.5)
ft('#fade', '{opacity: 0}', '{opacity: 1, duration: 0.9, ease: "power2.in"}', END - 0.9)


# ── karaoke captions: the spoken word sits on a framboise pill; hidden where the screen already writes the words ──
HIDE = [(0, W('As-tu', 5.3) - 0.1), (W('Seigneur,', 13.3) - 0.3, W('Tu', 16.0) - 0.1),
        (W("Jusqu'à", 21.1) - 0.3, W('Sa', 32.2) - 0.1), (W('Le', 38.1) - 0.1, W('Et', 50.5) - 0.1)]


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
    cut = min([a for a, b in HIDE if a > ch[0]['start']] + [VIDEO_END - 0.5])  # never run into a hidden stretch
    stop = min(nxt, ch[-1]['end'] + 0.7, cut) - 0.05
    cid = f'cap{k}'
    spans = []
    for i, w in enumerate(ch):
        t = text(w)
        if not t: continue
        spans.append(f'<span class="cw{" ck" if norm(w["text"]) in KEYS else ""}" id="{cid}-{i}">{t}</span>')
        ft(f'#{cid}-{i}', '{backgroundColor: "rgba(155,46,94,0)"}', f'{{backgroundColor: "rgba(155,46,94,1)", duration: 0.08, ease: "none"}}', w['start'])
        to(f'#{cid}-{i}', '{backgroundColor: "rgba(155,46,94,0)", duration: 0.12, ease: "none"}', max(w['start'] + 0.1, min(w['end'], stop - 0.05)))
    cap_html.append(f'      <div class="s-caption" id="{cid}">{" ".join(spans)}</div>')
    ft(f'#{cid}', '{opacity: 0, y: 14}', '{opacity: 1, y: 0, duration: 0.18, ease: "power2.out"}', ch[0]['start'] - 0.05)
    js.append(f'tl.set("#{cid}", {{opacity: 0}}, {stop:.3f});')


def spans_html(ws, prefix, cls, start=0):
    return ' '.join(f'<span class="{cls}" id="{prefix}-{start + k}">{text(w)}</span>' for k, w in enumerate(ws))


q_html = spans_html(Q, 'q', 'iw')
v6_html = spans_html(V6, 'v6', 'gw')
c1_html = spans_html(C1, 'c', 'kw')
C2T = [text(w) for w in C2]
c2_html = ' '.join(f'<span class="kw" id="c-{len(C1) + k}">{t}</span>' for k, t in enumerate(C2T[:-1])) + \
    f' <span class="hl"><span class="kw" id="c-{len(C1) + len(C2) - 1}">{C2T[-1]}</span><span class="uline"></span></span>'
k1_html = spans_html(K1, 'k', 'kw')
K2T = [text(w) for w in K2]
qi = K2T.index('quand')  # « quand tu attends » carries the drawn underline
k2_spans = [f'<span class="kw" id="k-{len(K1) + k}">{t}</span>' for k, t in enumerate(K2T)]
k2_html = ' '.join(k2_spans[:qi]) + f' <span class="hl">{" ".join(k2_spans[qi:])}<span class="uline"></span></span>'

NEQ = ('<svg class="neq" width="120" height="110" viewBox="0 0 120 110" aria-hidden="true">'
       '<path class="dr" pathLength="1" d="M14 40 H106"/><path class="dr" pathLength="1" d="M14 72 H106"/>'
       '<path class="dr" pathLength="1" d="M78 10 L42 100"/></svg>')
CANDLE = ('<div class="glow"></div><svg width="300" height="420" viewBox="0 0 300 420" aria-hidden="true">'
          '<path class="flame" d="M150 40 C170 80 182 104 182 128 C182 150 168 166 150 166 C132 166 118 150 118 128 C118 104 130 80 150 40 Z" fill="#F7C46A" stroke="#FFE7B0" stroke-width="3"/>'
          '<path class="dr" pathLength="1" d="M150 166 V196"/>'
          '<path class="dr" pathLength="1" d="M104 196 H196 V372 H104 Z"/>'
          '<path class="dr" pathLength="1" d="M60 372 H240 C240 392 220 404 196 404 H104 C80 404 60 392 60 372 Z"/></svg>')
SUNRISE = ('<path class="dr" pathLength="1" d="M20 200 H300"/>'
           '<path class="dr" pathLength="1" d="M80 200 C80 160 112 128 160 128 C208 128 240 160 240 200"/>'
           + ''.join(f'<path class="dr" pathLength="1" d="M{160 + 92 * c:.0f} {200 - 92 * s:.0f} L{160 + 128 * c:.0f} {200 - 128 * s:.0f}"/>'
                     for c, s in ((-0.94, 0.34), (-0.71, 0.71), (0, 1), (0.71, 0.71), (0.94, 0.34))))
PSALM_MID = [('3', 'Jusques à quand aurai-je des soucis dans mon âme…'), ('4', 'Regarde, réponds-moi, Éternel, mon Dieu&#8239;!'),
             ('5', '… si je chancelle.')]

CSS = """
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #070B18; }
      @font-face { font-family: "Cormorant"; font-weight: 500; src: url("assets/fonts/CG-Medium.ttf"); }
      @font-face { font-family: "Cormorant"; font-weight: 600; src: url("assets/fonts/CG-SemiBold.ttf"); }
      @font-face { font-family: "Cormorant"; font-weight: 500; font-style: italic; src: url("assets/fonts/CG-MediumItalic.ttf"); }
      @font-face { font-family: "Caveat"; src: url("assets/fonts/Caveat.ttf"); }
      #root { position: relative; width: 100%; height: 100%; overflow: hidden; background: #070B18; color: #F5EFE6; font-family: "DM Sans", sans-serif; }
      .night { position: absolute; inset: 0; overflow: hidden; background: radial-gradient(ellipse 1100px 900px at 50% 18%, #1C2850 0%, #0E1530 45%, #070B18 100%); }
      .stars { position: absolute; inset: 0; width: 100%; height: 100%; fill: #EAF0FF; }
      .moonglow { position: absolute; left: 160px; top: 120px; width: 760px; height: 760px; border-radius: 50%; background: radial-gradient(circle, rgba(190,210,255,.28) 0%, rgba(190,210,255,.08) 45%, rgba(190,210,255,0) 70%); }
      #dawn { position: absolute; inset: 0; opacity: 0; background: linear-gradient(rgba(40,40,90,.15) 0%, rgba(150,90,120,.55) 45%, rgba(240,150,90,.85) 80%, rgba(250,190,110,.95) 100%); }
      #sun { position: absolute; left: 140px; top: 1350px; width: 800px; height: 800px; border-radius: 50%; opacity: 0; background: radial-gradient(circle, rgba(255,226,160,.95) 0%, rgba(255,190,110,.55) 25%, rgba(255,170,90,0) 65%); }
      #avwrap { position: absolute; inset: 0; clip-path: inset(0px 0px 0px 0px round 0px 0px 0px 0px); }
      #avatar { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
      #avgrade { position: absolute; inset: 0; background: linear-gradient(rgba(7,11,24,.55) 0%, rgba(7,11,24,0) 18%, rgba(7,11,24,0) 58%, rgba(7,11,24,.5) 74%, rgba(7,11,24,.85) 100%); }
      #avframe { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; border: 3px solid """ + SILVER + """; box-shadow: 0 0 0 10px rgba(201,214,234,.1), 0 0 90px rgba(170,195,255,.35); opacity: 0; }
      #lowshade { position: absolute; left: 0; right: 0; bottom: 0; height: 1000px; opacity: 0; background: linear-gradient(rgba(7,11,24,0) 0%, rgba(7,11,24,.72) 42%, rgba(7,11,24,.9) 100%); }
      #vignette { position: absolute; inset: 0; opacity: 0; background: radial-gradient(ellipse 700px 820px at 50% 46%, rgba(5,6,12,.25) 0%, rgba(5,6,12,.75) 70%, rgba(5,6,12,.92) 100%); }
      #warm { position: absolute; inset: 0; opacity: 0; background: radial-gradient(ellipse 760px 900px at 50% 30%, rgba(30,14,8,0) 35%, rgba(30,14,8,.55) 75%, rgba(30,14,8,.85) 100%), linear-gradient(rgba(240,160,90,0) 55%, rgba(240,160,90,.22)); }
      .serif { font-family: "Instrument Serif", serif; line-height: 1.05; text-shadow: 0 6px 36px rgba(0,0,0,.65); }
      .it { font-style: italic; color: #E2B866; }
      .moonit { font-style: italic; color: #C9D6EA; }
      .kick { font-size: 24px; font-weight: 700; letter-spacing: .3em; text-transform: uppercase; color: #C9D6EA; }
      .strike { position: absolute; left: -10px; right: -10px; top: 56%; height: 7px; border-radius: 4px; background: #C2185B; transform: scaleX(0); transform-origin: 0 50%; }
      .uline { position: absolute; left: 0; right: 0; bottom: -6px; height: 6px; border-radius: 3px; background: #E2B866; transform: scaleX(0); transform-origin: 0 50%; }
      .hl { position: relative; display: inline-block; }
      .dr { fill: none; stroke: #E2B866; stroke-width: 5; stroke-linecap: round; stroke-linejoin: round; stroke-dasharray: 1; stroke-dashoffset: 1; }
      #hook { position: absolute; left: 40px; right: 40px; top: 1080px; text-align: center; }
      #hook .kick { opacity: 0; margin-bottom: 26px; }
      #hook .row { display: flex; align-items: center; justify-content: center; gap: 22px; }
      #hook .a, #hook .b { font-size: 132px; opacity: 0; }
      #hook .neq .dr { stroke: #F0B9D0; stroke-width: 8; }
      #lanterns { position: absolute; left: 0; right: 0; top: 1380px; height: 200px; }
      .ln { position: absolute; width: 74px; height: 104px; border-radius: 34px 34px 18px 18px; opacity: 0;
            background: radial-gradient(ellipse at 50% 60%, #FFE2A0 0%, #F5A94E 45%, #B85C2A 100%); box-shadow: 0 0 40px rgba(255,190,100,.85), 0 0 120px rgba(255,170,80,.45); }
      .ln::before { content: ""; position: absolute; left: 14px; right: 14px; top: -10px; height: 12px; border-radius: 6px 6px 0 0; background: #6B3A1E; }
      #noans { position: absolute; left: 0; right: 0; top: 1060px; text-align: center; opacity: 0; }
      #noans .kick { margin-bottom: 26px; }
      #noans .bubble { display: inline-flex; gap: 26px; padding: 44px 64px; border-radius: 70px; background: rgba(20,28,56,.75); border: 2px solid rgba(201,214,234,.45); }
      #noans .dot { width: 34px; height: 34px; border-radius: 50%; background: #C9D6EA; opacity: .25; }
      #note { position: absolute; left: 150px; right: 150px; top: 1010px; padding: 54px 56px 60px; background: #FBF3DF; color: #2A1A12; border-radius: 6px; box-shadow: 0 24px 60px rgba(0,0,0,.6); opacity: 0;
              font-family: "Caveat", cursive; font-size: 76px; line-height: 1.05; text-align: center; }
      #note::before { content: ""; position: absolute; left: 50%; top: -16px; width: 120px; height: 32px; margin-left: -60px; background: rgba(201,214,234,.6); }
      .iw { display: inline-block; opacity: 0; }
      .arch { position: absolute; left: 150px; right: 150px; top: 780px; height: 680px; overflow: hidden; opacity: 0; box-shadow: 0 30px 80px rgba(0,0,0,.6); }
      .arch img, .full img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
      .archframe { position: absolute; inset: 0; border: 3px solid """ + SILVER + """; border-radius: 420px 420px 26px 26px; }
      #pchip { position: absolute; left: 0; right: 0; top: 1380px; text-align: center; opacity: 0; }
      #pchip span { display: inline-block; padding: 16px 34px; border-radius: 999px; background: rgba(20,28,56,.85); border: 2px solid rgba(201,214,234,.55); font-weight: 700; font-size: 30px; letter-spacing: .24em; color: #E6ECF7; }
      #psalm { position: absolute; left: 70px; right: 70px; top: 770px; height: 860px; overflow: hidden; border-radius: 26px; opacity: 0;
               background-color: rgba(14,20,44,.72); border: 2px solid """ + SILVER + """; box-shadow: 0 30px 90px rgba(0,0,0,.55); }
      #col { position: absolute; left: 0; right: 0; top: 0; }
      .blk { position: relative; padding: 70px 60px 0; }
      #b2, #b6 { height: 860px; }
      .mid { height: 110px; padding: 0 70px; font-family: "Cormorant", serif; font-style: italic; font-size: 44px; color: rgba(230,236,247,.5); }
      .mid b { font-style: normal; font-weight: 600; color: rgba(226,184,102,.7); margin-right: 14px; }
      .rubric { text-align: center; font-family: "Cormorant", serif; font-weight: 600; font-size: 34px; letter-spacing: .32em; color: #C9D6EA; }
      #b6 .rubric { color: #E2B866; }
      .rule { margin: 22px auto 40px; width: 300px; height: 2px; background: linear-gradient(90deg, rgba(201,214,234,0), rgba(201,214,234,.7), rgba(201,214,234,0)); }
      #b6 .rule { background: linear-gradient(90deg, rgba(226,184,102,0), rgba(226,184,102,.8), rgba(226,184,102,0)); }
      .vtext { font-family: "Cormorant", serif; font-weight: 500; font-style: italic; font-size: 92px; line-height: 1.12; text-align: center; color: #EEF2FA; }
      .vw { display: inline-block; white-space: nowrap; }
      .st { display: inline-block; opacity: 0; }
      .gw { display: inline-block; opacity: .18; }
      .src { position: absolute; left: 0; right: 0; bottom: 50px; text-align: center; font-weight: 700; font-size: 22px; letter-spacing: .24em; color: rgba(230,236,247,.55); }
      #choice { position: absolute; left: 60px; right: 60px; top: 1110px; text-align: center; }
      #choice .r1 { position: relative; display: inline-block; font-size: 84px; color: #D8CDBE; opacity: 0; }
      #choice .r2 { margin-top: 22px; font-size: 104px; opacity: 0; }
      #candle { position: absolute; left: 390px; top: 760px; width: 300px; height: 420px; opacity: 0; }
      #candle svg { position: absolute; inset: 0; overflow: visible; }
      #candle .flame { transform-origin: 150px 166px; transform-box: view-box; }
      #candle .glow { position: absolute; left: -210px; top: -200px; width: 720px; height: 720px; border-radius: 50%; opacity: 0; background: radial-gradient(circle, rgba(255,200,110,.5) 0%, rgba(255,180,90,.15) 35%, rgba(255,180,90,0) 65%); }
      #aband { position: absolute; left: 60px; right: 60px; top: 1250px; text-align: center; }
      #aband .kick { opacity: 0; margin-bottom: 20px; color: #E2B866; }
      #aband .l2 { font-size: 104px; opacity: 0; }
      .full { position: absolute; inset: 0; overflow: hidden; opacity: 0; }
      .full .sh { position: absolute; inset: 0; background: linear-gradient(rgba(20,12,8,.5), rgba(20,12,8,.2) 40%, rgba(20,12,8,.84) 60%, rgba(20,12,8,.95)); }
      #talk { position: absolute; left: 70px; right: 70px; top: 1110px; text-align: center; }
      #talk .l1 { font-size: 64px; color: #E9DFCF; }
      #talk .l2 { margin-top: 18px; font-size: 112px; }
      #keep { position: absolute; left: 60px; right: 60px; top: 1090px; text-align: center; }
      #keep .k { opacity: 0; margin-bottom: 26px; color: #E2B866; }
      #keep .l1 { font-size: 62px; color: #E9DFCF; }
      #keep .l2 { margin-top: 22px; font-size: 84px; }
      #keep .hl, #talk .hl { color: #F2C879; font-style: italic; }
      .kw { display: inline-block; opacity: 0; }
      #endbg { position: absolute; inset: 0; opacity: 0; background: radial-gradient(ellipse 1000px 800px at 50% 100%, #8A4A2C 0%, #3A1E18 45%, #140C0A 100%); }
      #sunrise { position: absolute; left: 380px; top: 440px; width: 320px; height: 220px; opacity: 0; overflow: visible; }
      #endq { position: absolute; left: 60px; right: 60px; top: 720px; text-align: center; font-size: 84px; opacity: 0; }
      #intro { position: absolute; inset: 0; }
      #introlockup { position: absolute; left: 50%; top: 660px; width: 520px; margin-left: -260px; }
      #endlockup { position: absolute; left: 50%; top: 1220px; width: 430px; margin-left: -215px; opacity: 0; }
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
      <div id="sky" class="night"><div class="moonglow"></div>{STARS}</div>
      <div id="dawn"></div>
      <div id="sun"></div>
      <div id="aube" class="full"><img src="assets/img/aube.jpg" alt="" /><div class="sh"></div></div>
      <div id="david" class="arch" style="border-radius: 420px 420px 26px 26px"><img src="assets/img/david.jpg" alt="" /><div class="archframe"></div></div>
      <div id="psalm"><div id="col">
        <div id="b2" class="blk"><div class="rubric">PSAUME 13 · 2</div><div class="rule"></div><div class="vtext">{' '.join(v2_html)}</div><div class="src">LOUIS SEGOND 1910</div></div>
{''.join(f'        <div class="mid"><b>{n}</b>{t}</div>{chr(10)}' for n, t in PSALM_MID)}        <div id="b6" class="blk"><div class="rubric">PSAUME 13 · 6</div><div class="rule"></div><div class="vtext">{v6_html}</div><div class="src">LOUIS SEGOND 1910</div></div>
      </div></div>
      <div id="avwrap"><video id="avatar" class="clip" src="source/avatar.mp4" muted playsinline data-start="{INTRO}" data-duration="{VIDEO_LEN}" data-track-index="1"></video><div id="avgrade"></div></div>
      <div id="avframe"></div>
      <div id="lowshade"></div>
      <div id="vignette"></div>
      <div id="warm"></div>

      <div id="hook"><div class="kick">Et si…</div><div class="row"><div class="a serif moonit">silence</div>{NEQ}<div class="b serif">absence</div></div></div>
      <div id="lanterns"><div class="ln" style="left: 230px"></div><div class="ln" style="left: 503px; top: 40px"></div><div class="ln" style="left: 776px"></div></div>
      <div id="noans"><div class="kick">Sa réponse&#8239;?</div><div class="bubble"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div></div>
      <div id="note">{q_html}</div>
      <div id="pchip"><span>PSAUME 13</span></div>
      <div id="choice"><div class="r1 serif">situation déjà résolue<span class="strike"></span></div><div class="r2 serif">il choisit la <span class="hl it">confiance<span class="uline"></span></span></div></div>
      <div id="candle">{CANDLE}</div>
      <div id="aband"><div class="kick">Le silence de Dieu</div><div class="l2 serif">n’est pas un <span class="hl it">abandon<span class="uline"></span></span></div></div>
      <div id="talk"><div class="l1 serif">{c1_html}</div><div class="l2 serif">{c2_html}</div></div>
      <div id="keep"><div class="k kick">La foi, ce n’est pas seulement…</div><div class="l1 serif">{k1_html}</div><div class="l2 serif">{k2_html}</div></div>
{chr(10).join(cap_html)}
      <div id="endbg"></div>
      <svg id="sunrise" viewBox="0 0 320 220" aria-hidden="true">{SUNRISE}</svg>
      <div id="endq" class="serif">Et toi, arrives-tu à lui faire <span class="it">confiance</span>… même quand il semble <span class="it" style="color:#F0B9D0">silencieux</span>&#8239;?</div>
      <img id="wm" src="assets/brand/enracinee-monogram-a-filled-ondark.svg" alt="Enracinée" />
      <img id="endlockup" src="assets/brand/enracinee-lockup-a-vertical-ondark.svg" alt="Enracinée avec Adeline Nana" />
      <div id="intro" class="night"><div class="moonglow"></div>{STARS}
        <img id="introlockup" src="assets/brand/enracinee-lockup-a-vertical-ondark.svg" alt="Enracinée avec Adeline Nana" /></div>
      <div id="fade"></div>
      <audio id="mix" src="assets/mix.wav" data-start="0" data-duration="{END}" data-track-index="9" data-volume="1"></audio>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
{chr(10).join('      ' + j for j in js)}
      tl.to({{}}, {{ duration: {END} }}, 0);
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
open(os.path.join(ROOT, 'index.html'), 'w').write(html)
print('index.html', len(js), 'tweens', len(CH), 'caption chunks', 'END', END)
