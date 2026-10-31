# Thumbnails for « Le silence de Dieu », in the video's « de la nuit à l'aube » look: Adeline cut out (a frame of the
# video, hyperframes remove-background → assets/adeline-cutout.png) under a starry night that warms to dawn behind
# her, David's night painting, a handwritten « … n'est pas son absence », a slip for Psaume 13:6, the Enracinée logo.
# Vertical cover (title and face inside the centre 3:4 that profile grids show) and 16:9 (YouTube).
# usage: python3 thumbnail/make.py
import os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)
OUT = os.path.join(PROJ, 'renders/thumbnails')
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
A = 'file://' + PROJ + '/assets'
import re
r_ = [7]
def rnd():
    r_[0] = (r_[0] * 1103515245 + 12345) % 2 ** 31
    return r_[0] / 2 ** 31
STARS = ''.join(f'<circle cx="{rnd() * 1920:.0f}" cy="{rnd() * 1920:.0f}" r="{0.8 + rnd() * rnd() * 2.8:.1f}" opacity="{0.35 + rnd() * 0.65:.2f}"/>' for _ in range(260))
HEART = ('<svg class="heart" viewBox="0 0 220 220" aria-hidden="true"><path d="M110 196 C50 150 18 116 18 78 C18 46 42 24 70 24 '
         'C90 24 104 36 110 52 C116 36 130 24 150 24 C178 24 202 46 202 78 C202 116 170 150 110 196 Z" fill="rgba(194,24,91,.35)" '
         'stroke="#F0B9D0" stroke-width="9" stroke-linejoin="round"/></svg>')


def page(w, h, style, body):
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:"DM Sans";font-weight:700;src:url("{A}/fonts/DMSans-700.woff2")}}
@font-face{{font-family:"Instrument Serif";src:url("{A}/fonts/InstrumentSerif-400.woff2")}}
@font-face{{font-family:"Instrument Serif";font-style:italic;src:url("{A}/fonts/InstrumentSerif-400-Italic.woff2")}}
@font-face{{font-family:"Cormorant";font-weight:600;src:url("{A}/fonts/CG-SemiBold.ttf")}}
@font-face{{font-family:"Cormorant";font-weight:500;font-style:italic;src:url("{A}/fonts/CG-MediumItalic.ttf")}}
@font-face{{font-family:"Caveat";src:url("{A}/fonts/Caveat.ttf")}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{w}px;height:{h}px;overflow:hidden;background:#070B18}}
#c{{position:relative;width:{w}px;height:{h}px;overflow:hidden;background:#070B18;color:#F5EFE6;font-family:"DM Sans",sans-serif}}
.paint{{position:absolute;object-fit:cover;filter:brightness(.55) saturate(1.05)}}
.stars{{position:absolute;left:0;top:0;width:1920px;height:1920px;fill:#EAF0FF}}
.dawn{{position:absolute;border-radius:50%;background:radial-gradient(circle,rgba(255,214,150,.75) 0%,rgba(245,160,95,.38) 30%,rgba(200,110,90,.12) 52%,rgba(200,110,90,0) 70%)}}
.halo{{position:absolute;border-radius:50%;background:radial-gradient(circle,rgba(190,210,255,.42) 0%,rgba(170,190,255,.14) 40%,rgba(170,190,255,0) 70%)}}
.person{{position:absolute;filter:drop-shadow(0 0 2px rgba(17,13,10,.9)) drop-shadow(0 0 30px rgba(190,210,255,.4))}}
.shade{{position:absolute;left:0;right:0}}
.title{{font-family:"Instrument Serif",serif;line-height:.98;letter-spacing:-.01em;text-shadow:0 8px 50px rgba(0,0,0,.8)}}
.title .it{{position:relative;display:inline-block;font-style:italic;color:#C9D6EA}}
.strike{{position:absolute;left:-12px;right:-12px;top:55%;height:12px;border-radius:6px;background:#C2185B;transform:rotate(-3deg)}}
.hand{{font-family:"Caveat",cursive;color:#F0B9D0;text-shadow:0 4px 24px rgba(0,0,0,.85);display:inline-flex;align-items:center;gap:14px}}
.heart{{display:block}}
.slip{{position:absolute;padding:26px 40px 30px;border-radius:8px;color:#2A1A12;box-shadow:0 24px 60px rgba(0,0,0,.6);
  background:radial-gradient(ellipse at 45% 35%,#F6EBD2 0%,#EBDBB8 60%,#D3BA8C 100%)}}
.rubric{{font-family:"Cormorant",serif;font-weight:600;letter-spacing:.3em;color:#A0662A;text-align:center}}
.vq{{font-family:"Cormorant",serif;font-style:italic;font-weight:500;line-height:1.12;text-align:center}}
{style}
</style></head><body><div id="c">{body}</div></body></html>"""


# ── vertical 1080×1920 ───────────────────────────────────────────────────────────────────────────────────────────
V = page(1080, 1920, """
.night{position:absolute;inset:0;background:radial-gradient(ellipse 1100px 1000px at 50% 20%,#1C2850 0%,#0E1530 45%,#070B18 100%)}
.paint{left:0;top:0;width:1080px;height:1920px;object-position:62% 30%;opacity:.55}
.dawn{left:-260px;top:1060px;width:1600px;height:1300px}
.halo{left:90px;top:620px;width:900px;height:900px}
.person{left:-40px;top:610px;width:1160px}
.shade.t{top:0;height:980px;background:linear-gradient(#070B18 0%,rgba(7,11,24,.9) 34%,rgba(7,11,24,.4) 70%,rgba(7,11,24,0))}
.shade.b{top:1330px;height:590px;background:linear-gradient(rgba(7,11,24,0),rgba(20,12,16,.88) 40%,#140C0A)}
.logo{position:absolute;left:50%;top:96px;width:340px;margin-left:-170px}
.top{position:absolute;left:0;right:0;top:240px;text-align:center}
.t1{font-size:150px}
.t2{font-size:150px;margin-top:0}
.hand{font-size:84px;margin-top:14px;transform:rotate(-3deg)}
.slip{left:50%;top:1500px;width:760px;margin-left:-380px;transform:rotate(-1.5deg)}
.rubric{font-size:30px}
.vq{margin-top:12px;font-size:56px}""",
f"""<div class="night"></div><svg class="stars" viewBox="0 0 1920 1920" aria-hidden="true">{STARS}</svg>
<img class="paint" src="{A}/img/david.jpg" alt="">
<div class="dawn"></div>
<div class="halo"></div>
<div class="shade t"></div>
<img class="person" src="file://{HERE}/assets/adeline-cutout.png" alt="">
<div class="shade b"></div>
<img class="logo" src="{A}/brand/enracinee-lockup-a-horizontal-ondark.svg" alt="">
<div class="top"><div class="title t1">Le <span class="it">silence</span></div><div class="title t2">de Dieu</div>
<div class="hand">… n’est pas son absence</div></div>
<div class="slip"><div class="rubric">PSAUME 13 · 6</div><div class="vq">« Moi, j’ai confiance en ta bonté. »</div></div>""")

# ── 16:9 1920×1080: title left, Adeline right ────────────────────────────────────────────────────────────────────
L = page(1920, 1080, """
.night{position:absolute;inset:0;background:radial-gradient(ellipse 1400px 900px at 30% 10%,#1C2850 0%,#0E1530 45%,#070B18 100%)}
.paint{left:760px;top:0;width:1160px;height:1080px;object-position:50% 30%;opacity:.6}
.fadel{position:absolute;left:700px;top:0;width:520px;height:1080px;background:linear-gradient(90deg,#070B18,rgba(7,11,24,0))}
.dawn{left:900px;top:520px;width:1300px;height:1100px}
.halo{left:1060px;top:40px;width:950px;height:950px}
.person{left:1080px;top:110px;width:820px}
.shade.b{top:860px;height:220px;background:linear-gradient(rgba(7,11,24,0),rgba(20,12,16,.85) 60%,#140C0A)}
.logo{position:absolute;left:110px;top:80px;width:330px}
.left{position:absolute;left:110px;top:200px;width:1000px}
.t1{font-size:150px}
.t2{font-size:150px}
.hand{font-size:82px;margin-top:8px;transform:rotate(-2deg)}
.slip{left:110px;top:800px;width:760px;transform:rotate(-1deg)}
.rubric{font-size:26px;text-align:left}
.vq{margin-top:8px;font-size:46px;text-align:left}""",
f"""<div class="night"></div><svg class="stars" viewBox="0 0 1920 1920" aria-hidden="true">{STARS}</svg>
<img class="paint" src="{A}/img/david.jpg" alt="">
<div class="fadel"></div>
<div class="dawn"></div>
<div class="halo"></div>
<img class="person" src="file://{HERE}/assets/adeline-cutout.png" alt="">
<div class="shade b"></div>
<img class="logo" src="{A}/brand/enracinee-lockup-a-horizontal-ondark.svg" alt="">
<div class="left"><div class="title t1">Le <span class="it">silence</span></div><div class="title t2">de Dieu</div>
<div class="hand">… n’est pas son absence</div></div>
<div class="slip"><div class="rubric">PSAUME 13 · 6</div><div class="vq">« Moi, j’ai confiance en ta bonté. »</div></div>""")


def shot(html, name, w, h, scale):
    path = os.path.join(HERE, f'.{name}.html')
    open(path, 'w').write(html)
    out = os.path.join(OUT, name + '.png')
    subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files',
                    f'--window-size={w},{h}', f'--force-device-scale-factor={scale}', '--virtual-time-budget=3000',
                    f'--screenshot={out}', 'file://' + path], capture_output=True, check=True)
    os.remove(path)
    return out


os.makedirs(OUT, exist_ok=True)
v4k = shot(V, 'cover-vertical-4k', 1080, 1920, 2)
l4k = shot(L, 'thumbnail-16x9-4k', 1920, 1080, 2)
subprocess.run(['magick', v4k, '-resize', '1080x1920', '-quality', '92', os.path.join(OUT, 'cover-vertical-1080x1920.jpg')], check=True)
subprocess.run(['magick', l4k, '-resize', '1280x720', '-quality', '92', os.path.join(OUT, 'thumbnail-youtube-1280x720.jpg')], check=True)
print('\n'.join(sorted(os.listdir(OUT))))
