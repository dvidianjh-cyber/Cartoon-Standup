"""Draw the comedy club stage in the faceted low-poly style, in three framings.

Usage: python3 art/make_stage.py   (from the series repo's top folder)

The art is drawn once in a 1280x720 "world" (the wide shot). The medium and
close shots are the same art cropped with a smaller viewBox, so the three
backdrops always match. Writes:

  show/backdrops/stage_wide/backdrop.svg    whole stage, zoom 1
  show/backdrops/stage_mid/backdrop.svg     waist up, zoom 2
  show/backdrops/stage_close/backdrop.svg   head and shoulders, zoom 3
  show/sets/mic/piece.svg                   mic stand (drawn over the comic)
  show/sets/audience/piece.svg              heads of the front row (wide shot only)

Where the comic stands, per framing (world feet at x 640, y 640, scale 0.55),
is in FRAMES below; script.yaml uses the same numbers.
"""
import math
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "show"
W, H = 1280, 720
FLOOR_BACK = 560          # where the back wall meets the stage
STAGE_EDGE = 664          # the front lip of the stage
SPOT = (640, 330)         # centre of the light on the wall

# framing -> viewBox (x, y, w, h); zoom = 1280 / w
FRAMES = {
    "stage_wide": (0, 0, 1280, 720),
    "stage_mid": (320, 60, 640, 360),
    "stage_close": (1280 / 3, 85, 1280 / 3, 240),
}


def hexrgb(c):
    c = c.lstrip("#")
    return [int(c[i:i + 2], 16) for i in (0, 2, 4)]


def rgbhex(rgb):
    return "#" + "".join(f"{max(0, min(255, round(v))):02x}" for v in rgb)


def mix(a, b, t):
    a, b = hexrgb(a), hexrgb(b)
    return rgbhex([x + (y - x) * t for x, y in zip(a, b)])


def shade(c, f):
    return mix(c, "#ffffff", f) if f > 0 else mix(c, "#000000", -f)


def poly(ps, fill, extra=""):
    return f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in ps)}" fill="{fill}"{extra}/>'


def tri_grid(x0, y0, x1, y1, nx, ny, rnd, jitter=0.38):
    """Jittered grid split into triangles: the faceted low-poly look."""
    dx, dy = (x1 - x0) / nx, (y1 - y0) / ny
    pts = {}
    for j in range(ny + 1):
        for i in range(nx + 1):
            x, y = x0 + i * dx, y0 + j * dy
            if 0 < i < nx:
                x += rnd.uniform(-jitter, jitter) * dx
            if 0 < j < ny:
                y += rnd.uniform(-jitter, jitter) * dy
            pts[i, j] = (x, y)
    tris = []
    for j in range(ny):
        for i in range(nx):
            a, b, c, d = pts[i, j], pts[i + 1, j], pts[i + 1, j + 1], pts[i, j + 1]
            if rnd.random() < 0.5:
                tris += [(a, b, c), (a, c, d)]
            else:
                tris += [(a, b, d), (b, c, d)]
    return tris


def centroid(t):
    return sum(p[0] for p in t) / 3, sum(p[1] for p in t) / 3


def wall(rnd):
    """Exposed brick wall, faceted, lit by the spotlight in the middle."""
    out = []
    dark, lit = "#2a1a1d", "#a4553f"
    for t in tri_grid(200, 40, 1080, FLOOR_BACK, 16, 9, rnd):
        cx, cy = centroid(t)
        d = math.hypot((cx - SPOT[0]) / 1.25, cy - SPOT[1]) / 430
        k = max(0.0, 1 - d) ** 1.4
        out.append(poly(t, shade(mix(dark, lit, k), rnd.uniform(-0.07, 0.05))))
    # a few brick courses, faint, so it reads as brick without fighting the facets
    g = []
    for row, y in enumerate(range(70, FLOOR_BACK, 34)):
        g.append(f'<path d="M200 {y} H1080"/>')
        off = 0 if row % 2 else 38
        for x in range(200 + off, 1080, 76):
            g.append(f'<path d="M{x} {y} V{y + 34}"/>')
    out.append(f'<g stroke="#140c0e" stroke-width="2" opacity="0.28">{"".join(g)}</g>')
    return out


def neon_sign():
    """LIVE COMEDY, top left of the wall: in the wide and the medium shot."""
    x, y = 455, 168
    glow = '<filter id="glow" x="-30%" y="-60%" width="160%" height="220%"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
    s = [f"<defs>{glow}</defs>"]
    # backing board, faceted
    s.append(poly([(x - 120, y - 70), (x + 118, y - 74), (x + 124, y + 52), (x - 116, y + 56)], "#1b1420"))
    s.append(poly([(x - 120, y - 70), (x + 118, y - 74), (x - 10, y - 10)], "#231a29"))
    s.append(poly([(x + 124, y + 52), (x - 116, y + 56), (x + 10, y + 4)], "#160f1a"))
    s.append(f'<g filter="url(#glow)" font-family="Arial Black, Arial, Helvetica, sans-serif" font-weight="900" text-anchor="middle">'
             f'<text x="{x}" y="{y - 22}" font-size="30" fill="#ffd36b" letter-spacing="8">LIVE</text>'
             f'<text x="{x}" y="{y + 30}" font-size="46" fill="#ff5c8a" letter-spacing="3">COMEDY</text></g>')
    # little star
    sx, sy = x + 98, y - 40
    star = [(sx + 12 * math.cos(a) * (1 if k % 2 == 0 else 0.45), sy + 12 * math.sin(a) * (1 if k % 2 == 0 else 0.45))
            for k, a in enumerate([i * math.pi / 5 - math.pi / 2 for i in range(10)])]
    s.append(poly(star, "#7fe3ff", ' filter="url(#glow)"'))
    return s


def curtains(rnd):
    """Deep red curtains framing the stage, vertical folds, and a valance."""
    out = []
    base = ["#6d1520", "#8e2230", "#561019", "#a1303a", "#7a1a26"]
    for side in (0, 1):
        x0, x1 = (0, 220) if side == 0 else (1060, 1280)
        n = 7
        w = (x1 - x0) / n
        for i in range(n):
            xa, xb = x0 + i * w, x0 + (i + 1) * w
            top, bot = 40, FLOOR_BACK + 26
            mid = (xa + xb) / 2 + rnd.uniform(-6, 6)
            c = base[(i + side * 2) % len(base)]
            out.append(poly([(xa, top), (xb, top), (xb + rnd.uniform(-4, 4), bot), (xa, bot)], c))
            out.append(poly([(xa, top), (mid, top), (mid + rnd.uniform(-8, 8), bot), (xa, bot)], shade(c, -0.18)))
            out.append(poly([(mid, top + 60), (xb, top), (xb, bot - 120)], shade(c, 0.1)))
        # inner edge catches the light
        ex = 220 if side == 0 else 1060
        out.append(poly([(ex - 10, 40), (ex + 10, 40), (ex + 6 if side == 0 else ex - 6, FLOOR_BACK + 26), (ex - 6 if side == 0 else ex + 6, FLOOR_BACK + 26)], "#b33a43"))
    # valance across the top
    vx = 0
    k = 0
    while vx < W:
        w = 80 + (k % 3) * 10
        c = base[k % len(base)]
        out.append(poly([(vx, 0), (vx + w, 0), (vx + w, 54), (vx + w / 2, 70), (vx, 54)], c))
        out.append(poly([(vx, 0), (vx + w / 2, 0), (vx + w / 2, 70), (vx, 54)], shade(c, -0.15)))
        vx += w
        k += 1
    out.append(poly([(0, 0), (W, 0), (W, 12), (0, 12)], "#3d0b12"))
    return out


def truss():
    """Lighting bar with three cans, just under the valance."""
    out = [poly([(250, 76), (1030, 76), (1030, 86), (250, 86)], "#1d1a22")]
    for cx in (360, 920):   # no can in the middle: it would sit behind the comic's head
        out.append(poly([(cx - 22, 80), (cx + 22, 80), (cx + 30, 116), (cx - 30, 116)], "#26222c"))
        out.append(poly([(cx - 22, 80), (cx, 80), (cx - 4, 116), (cx - 30, 116)], "#1a171f"))
        out.append(poly([(cx - 26, 112), (cx + 26, 112), (cx + 18, 122), (cx - 18, 122)], "#ffb36b"))
    return out


def stage_floor(rnd):
    out = []
    # planks running towards the audience, faceted
    planks = 14
    for i in range(planks):
        xa_b, xb_b = 180 + i * (920 / planks), 180 + (i + 1) * (920 / planks)
        xa_f, xb_f = -40 + i * (1360 / planks), -40 + (i + 1) * (1360 / planks)
        cx = (xa_f + xb_f) / 2
        k = max(0.0, 1 - abs(cx - 640) / 560)
        c = mix("#3b2a22", "#8a6146", k ** 1.2)
        c = shade(c, rnd.uniform(-0.06, 0.05))
        out.append(poly([(xa_b, FLOOR_BACK), (xb_b, FLOOR_BACK), (xb_f, STAGE_EDGE), (xa_f, STAGE_EDGE)], c))
        midb, midf = (xa_b + xb_b) / 2, (xa_f + xb_f) / 2
        out.append(poly([(xa_b, FLOOR_BACK), (midb, FLOOR_BACK), (midf, STAGE_EDGE), (xa_f, STAGE_EDGE)], shade(c, -0.08)))
    # front of the stage
    out.append(poly([(-40, STAGE_EDGE), (1320, STAGE_EDGE), (1320, STAGE_EDGE + 8), (-40, STAGE_EDGE + 8)], "#a07858"))
    for t in tri_grid(0, STAGE_EDGE + 8, W, H, 10, 2, rnd):
        out.append(poly(t, shade("#1f1513", rnd.uniform(-0.15, 0.12))))
    # side floor beyond the curtains: dark
    out.append(poly([(0, FLOOR_BACK + 26), (200, FLOOR_BACK), (-40, STAGE_EDGE)], "#241915"))
    out.append(poly([(W, FLOOR_BACK + 26), (1080, FLOOR_BACK), (1320, STAGE_EDGE)], "#241915"))
    return out


def stool():
    """Bar stool with a pint of water, stage right of the comic."""
    x, y = 905, 628
    out = []
    leg = "#2b2a30"
    out.append(poly([(x - 44, y), (x - 36, y), (x - 14, y - 150), (x - 22, y - 150)], leg))
    out.append(poly([(x + 44, y), (x + 36, y), (x + 14, y - 150), (x + 22, y - 150)], "#232228"))
    out.append(poly([(x - 4, y - 6), (x + 4, y - 6), (x + 3, y - 150), (x - 3, y - 150)], "#1c1b20"))
    out.append(poly([(x - 34, y - 70), (x + 34, y - 70), (x + 32, y - 64), (x - 32, y - 64)], "#3a3940"))
    out.append(poly([(x - 46, y - 160), (x + 46, y - 160), (x + 40, y - 146), (x - 40, y - 146)], "#5b3a2a"))
    out.append(poly([(x - 46, y - 160), (x + 46, y - 160), (x + 30, y - 170), (x - 30, y - 170)], "#7d543b"))
    out.append(poly([(x - 30, y - 170), (x, y - 170), (x - 46, y - 160)], "#946649"))
    # pint glass
    gx, gy = x + 12, y - 166
    out.append(poly([(gx - 12, gy), (gx + 12, gy), (gx + 15, gy - 46), (gx - 15, gy - 46)], "#bfe3ee", ' opacity="0.75"'))
    out.append(poly([(gx - 12, gy), (gx, gy), (gx - 2, gy - 46), (gx - 15, gy - 46)], "#e8f7fb", ' opacity="0.6"'))
    out.append(poly([(gx - 15, gy - 46), (gx + 15, gy - 46), (gx + 15, gy - 49), (gx - 15, gy - 49)], "#ffffff", ' opacity="0.8"'))
    return out


def spotlight(rnd):
    """The cone from a lamp above the valance and the pool of light on the stage."""
    out = []
    top_l, top_r = (600, 0), (680, 0)
    bot_l, bot_r = (430, 650), (850, 650)
    n = 6
    for i in range(n):
        ta = top_l[0] + (top_r[0] - top_l[0]) * i / n
        tb = top_l[0] + (top_r[0] - top_l[0]) * (i + 1) / n
        ba = bot_l[0] + (bot_r[0] - bot_l[0]) * i / n
        bb = bot_l[0] + (bot_r[0] - bot_l[0]) * (i + 1) / n
        op = 0.05 + 0.05 * (1 - abs(i - (n - 1) / 2) / (n / 2)) + rnd.uniform(-0.01, 0.015)
        out.append(poly([(ta, 0), (tb, 0), (bb, 650), (ba, 650)], "#fff3cf", f' opacity="{op:.3f}"'))
    # pool: faceted ellipse, brighter in the middle
    cx, cy, rx, ry = 640, 640, 230, 30
    ring = [(cx + rx * math.cos(a), cy + ry * math.sin(a)) for a in [i * math.pi / 8 for i in range(16)]]
    for i in range(16):
        a, b = ring[i], ring[(i + 1) % 16]
        out.append(poly([(cx, cy), a, b], "#ffe9b0", f' opacity="{0.22 + 0.06 * ((i * 7) % 3) / 2:.3f}"'))
    inner = [(cx + rx * 0.55 * math.cos(a), cy + ry * 0.55 * math.sin(a)) for a in [i * math.pi / 6 for i in range(12)]]
    out.append(poly(inner, "#fff6d8", ' opacity="0.25"'))
    return out


def vignette():
    """Darken the edges a touch so the eye goes to the comic (in every crop)."""
    return ['<defs><radialGradient id="vig" cx="0.5" cy="0.45" r="0.75">'
            '<stop offset="0.55" stop-color="#000" stop-opacity="0"/>'
            '<stop offset="1" stop-color="#000" stop-opacity="0.45"/></radialGradient></defs>',
            f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#vig)"/>']


def backdrop():
    rnd = random.Random(7)
    parts = [f'<rect x="0" y="0" width="{W}" height="{H}" fill="#140e14"/>']
    parts += wall(rnd)
    parts += neon_sign()
    parts += stage_floor(rnd)
    parts += stool()
    parts += spotlight(rnd)
    parts += curtains(rnd)
    parts += truss()
    parts += vignette()
    return "\n  ".join(parts)


def mic_piece():
    """Mic stand in puppet units of the comic's rig (318 x 970, feet at 970).

    viewBox 0 0 318 990: place it at the comic's x, y + 20 * scale, same scale.
    The mic sits just off the right of the chin, clear of the mouth.
    """
    cx = 159
    s = []
    # tripod base on the floor
    s.append(poly([(cx + 8, 940), (cx + 12, 940), (cx - 60, 988), (cx - 70, 988)], "#16161b"))
    s.append(poly([(cx + 8, 940), (cx + 12, 940), (cx + 92, 986), (cx + 82, 986)], "#1d1d23"))
    s.append(poly([(cx + 7, 936), (cx + 13, 936), (cx + 16, 978), (cx + 4, 978)], "#121216"))
    # pole
    s.append(poly([(cx + 6, 322), (cx + 14, 322), (cx + 14, 944), (cx + 6, 944)], "#26262d"))
    s.append(poly([(cx + 10, 322), (cx + 14, 322), (cx + 14, 944), (cx + 10, 944)], "#3d3d47"))
    s.append(poly([(cx + 3, 600), (cx + 17, 600), (cx + 17, 616), (cx + 3, 616)], "#33333b"))
    # clip and mic body, angled up towards the right of the chin
    s.append(poly([(cx + 2, 300), (cx + 18, 300), (cx + 18, 326), (cx + 2, 326)], "#1a1a20"))
    s.append(poly([(cx + 4, 304), (cx + 15, 300), (cx + 34, 252), (cx + 22, 248)], "#2c2c34"))
    s.append(poly([(cx + 4, 304), (cx + 9, 302), (cx + 27, 250), (cx + 22, 248)], "#3f3f49"))
    # grille: faceted ball
    gx, gy, r = cx + 31, 238, 15
    ring = [(gx + r * math.cos(a), gy + r * 1.1 * math.sin(a)) for a in [i * math.pi / 4 + 0.3 for i in range(8)]]
    greys = ["#8d939c", "#6b7079", "#a9aeb6", "#5a5e66", "#7c818a", "#b9bec5", "#646871", "#9aa0a8"]
    for i in range(8):
        s.append(poly([(gx, gy), ring[i], ring[(i + 1) % 8]], greys[i]))
    s.append(poly([(gx - 12, gy + 10), (gx + 12, gy + 10), (gx + 9, gy + 15), (gx - 9, gy + 15)], "#2a2a31"))
    # cable down the pole
    s.append('<path d="M%d 310 C%d 360 %d 420 %d 520 S%d 800 %d 980" stroke="#0d0d10" stroke-width="3" fill="none"/>'
             % (cx + 12, cx + 26, cx + 24, cx + 22, cx + 20, cx + 40))
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 318 990" width="318" height="990">\n'
            "  <!-- Mic on a stand, faceted. Anchor: bottom centre = the comic's feet + 20 units. -->\n  "
            + "\n  ".join(s) + "\n</svg>\n")


def audience_piece():
    """Front row heads and shoulders in silhouette, 1280 x 120, rim-lit from the stage."""
    rnd = random.Random(11)
    s = []
    xs = [40, 150, 265, 380, 900, 1010, 1125, 1240, 520, 760]
    for i, x in enumerate(xs):
        x += rnd.uniform(-15, 15)
        centre = 470 < x < 810
        top = 52 if centre else rnd.uniform(4, 22)
        hw = rnd.uniform(30, 36)
        sh = rnd.uniform(70, 86)
        body = "#0e0b12"
        # shoulders
        s.append(poly([(x - sh, 120), (x - sh * 0.8, top + 74), (x - hw * 0.6, top + 60), (x + hw * 0.6, top + 60),
                       (x + sh * 0.8, top + 74), (x + sh, 120)], body))
        # head: faceted octagon
        hy = top + 30
        ring = [(x + hw * math.cos(a), hy + hw * 1.15 * math.sin(a)) for a in [k * math.pi / 4 + 0.39 for k in range(8)]]
        s.append(poly(ring, "#110d15"))
        # rim light on the top edge
        s.append(poly([ring[4], ring[5], ring[6], (x, hy - hw * 0.6)], "#2c2533"))
        s.append(poly([ring[6], ring[7], (x, hy - hw * 0.6)], "#3a3043"))
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 120" width="1280" height="120">\n'
            "  <!-- Front row of the audience, silhouettes. Anchor: bottom centre at (640, 720) in the wide shot. -->\n  "
            + "\n  ".join(s) + "\n</svg>\n")


def main():
    art = backdrop()
    for name, (x, y, w, h) in FRAMES.items():
        d = ROOT / "backdrops" / name
        d.mkdir(parents=True, exist_ok=True)
        (d / "backdrop.svg").write_text(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x:g} {y:g} {w:g} {h:g}" width="1280" height="720">\n'
            f"  <!-- Comedy club stage, faceted low-poly. Made by art/make_stage.py ({name}); don't edit by hand. -->\n  "
            + art + "\n</svg>\n", encoding="utf-8")
    for piece, svg, meta in (("mic", mic_piece(), '{ "layer": "front" }\n'),
                             ("audience", audience_piece(), '{ "layer": "front" }\n')):
        d = ROOT / "sets" / piece
        d.mkdir(parents=True, exist_ok=True)
        (d / "piece.svg").write_text(svg, encoding="utf-8")
        (d / "piece.json").write_text(meta, encoding="utf-8")
    print("wrote stage_wide, stage_mid, stage_close, sets/mic, sets/audience")


if __name__ == "__main__":
    main()
