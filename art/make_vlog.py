"""Draw the vlog locations in the faceted low-poly style.

Usage: python3 art/make_vlog.py   (from the series repo's top folder)

  show/backdrops/street/      terraced street, walking towards the camera (depth
                              backdrop: static base plus sprites in backdrop.json)
  show/backdrops/lounge/      sofa in front of shelves of vinyl, a window (static)
  show/backdrops/car/         inside the estate car from the dash mount (static)
  show/backdrops/high_street/ shop fronts incl. the solicitor's, side-on, tiles for scroll

Close-ups put James's head across x 480-800 and his shoulders across the bottom,
so the detail is at the sides and the top.
"""
import math
from pathlib import Path

from lowpoly import (RECORD_COLORS, faceted, gem, mix, poly, rect, seeded, shade, spines, svg, text)

ROOT = Path(__file__).resolve().parent.parent / "show" / "backdrops"
W, H = 1280, 720


def write(name, files):
    d = ROOT / name
    d.mkdir(parents=True, exist_ok=True)
    for fn, content in files.items():
        (d / fn).write_text(content, encoding="utf-8")


def sky(rnd, y1, top="#8fbad6", bottom="#f2e3c4", x0=0, x1=W, n=(14, 4)):
    def col(cx, cy):
        return shade(mix(top, bottom, min(1, max(0, cy / y1))), rnd.uniform(-0.03, 0.04))
    return faceted(x0, 0, x1, y1, n[0], n[1], rnd, col)


def cloud(cx, cy, s, c="#ffffff"):
    pts = [(-60, 10), (-48, -14), (-20, -26), (8, -34), (36, -22), (58, -6), (66, 12)]
    out = [poly([(cx + x * s, cy + y * s) for x, y in pts], c, ' opacity="0.9"')]
    out.append(poly([(cx - 60 * s, cy + 10 * s), (cx + 66 * s, cy + 12 * s), (cx + 10 * s, cy - 4 * s)], shade(c, -0.08), ' opacity="0.9"'))
    return out


# ------------------------------------------------------------------ street (depth)
VX, VY = 640, 300          # vanishing point
GROUND = 420               # ground is this far below the vanishing point at depth 1


def P(X, Y, z):
    return VX + X / z, VY + Y / z


# House fronts are spaced by a constant depth ratio and the colours repeat
# every HOUSE_REPEAT houses, so the base image maps onto itself when scaled by
# STREET_ZOOM about the vanishing point. backdrop.json sets that zoom, so the
# engine zoom-loops the base (the houses go by) under the moving sprites,
# and the loop's cross-fade has nothing to ghost.
HOUSE_RATIO = 1.32
HOUSE_REPEAT = 3
STREET_ZOOM = HOUSE_RATIO ** HOUSE_REPEAT


def street():
    rnd = seeded(21)
    b = ['<defs><linearGradient id="sky" gradientUnits="userSpaceOnUse" x1="0" y1="-150" x2="0" y2="300">'
         '<stop offset="0" stop-color="#86b4d3"/><stop offset="1" stop-color="#f2e3c4"/></linearGradient></defs>',
         rect(-2000, -2000, 5280, 2300, "url(#sky)")]
    zs = [0.25 * HOUSE_RATIO ** k for k in range(24)]          # 0.25 .. ~150
    EAVES = -380                 # two storeys
    for side in (-1, 1):
        X = 760 * side
        for i in range(len(zs) - 1):
            za, zb = zs[i], zs[i + 1]
            zm = lambda f: za + (zb - za) * f
            k = i % HOUSE_REPEAT
            c = ["#a65a43", "#93503c", "#b0654b"][k] if side < 0 else ["#c9b394", "#b89f80", "#d4bf9f"][k]
            roof = "#4c5560"
            # pitched slate roof, then the facade
            b.append(poly([P(X, EAVES, za), P(X, EAVES, zb), P(X * 1.3, EAVES - 170, zb), P(X * 1.3, EAVES - 170, za)], roof))
            b.append(poly([P(X, EAVES, za), P(X * 1.3, EAVES - 170, zm(0.5)), P(X * 1.3, EAVES - 170, za)], "#5a6470"))
            if k == 0:   # chimney stack on the party wall
                b.append(poly([P(X * 1.12, EAVES - 60, za), P(X * 1.12, EAVES - 60, zm(0.12)), P(X * 1.12, EAVES - 230, zm(0.12)), P(X * 1.12, EAVES - 230, za)], shade(c, -0.15)))
            b.append(poly([P(X, EAVES, za), P(X, EAVES, zb), P(X, GROUND - 130, zb), P(X, GROUND - 130, za)], c))
            b.append(poly([P(X, EAVES, za), P(X, EAVES, zb), P(X, -150, za)], shade(c, 0.07)))
            b.append(poly([P(X, -60, za), P(X, -60, zb), P(X, GROUND - 130, zb), P(X, GROUND - 130, za)], shade(c, -0.06)))
            frame, glass = "#efe8da", "#34495a"
            for (f0, f1, y0, y1) in ((0.15, 0.5, -320, -170), (0.1, 0.55, -40, 140)):
                b.append(poly([P(X, y0, zm(f0)), P(X, y0, zm(f1)), P(X, y1, zm(f1)), P(X, y1, zm(f0))], frame))
                b.append(poly([P(X, y0 + 14, zm(f0 + 0.04)), P(X, y0 + 14, zm(f1 - 0.04)), P(X, y1 - 14, zm(f1 - 0.04)), P(X, y1 - 14, zm(f0 + 0.04))], glass))
            door = ["#1f4d3a", "#7b2d26", "#1f5fa8"][k]
            b.append(poly([P(X, -20, zm(0.68)), P(X, -20, zm(0.86)), P(X, GROUND - 130, zm(0.86)), P(X, GROUND - 130, zm(0.68))], door))
            b.append(poly([P(X, -360, zm(0.98)), P(X, -360, zb), P(X, GROUND - 130, zb), P(X, GROUND - 130, zm(0.98))], shade(c, -0.25)))
            # low front wall and hedge along the pavement
            b.append(poly([P(X, GROUND - 130, za), P(X, GROUND - 130, zb), P(X, GROUND, zb), P(X, GROUND, za)], "#3f6b3a"))
            b.append(poly([P(X, GROUND - 130, za), P(X, GROUND - 60, zb), P(X, GROUND, za)], "#355c31"))
        for Y, col, w in ((EAVES, "#3a3a40", 4), (-60, "#e9dccb", 3)):
            a2, c2 = P(X, Y, zs[0]), P(X, Y, zs[-1])
            b.append(f'<path d="M{a2[0]:.1f} {a2[1]:.1f} L{c2[0]:.1f} {c2[1]:.1f}" stroke="{col}" stroke-width="{w}" opacity="0.7"/>')
    # pavements and road
    # pavements and road: only lines along the street, so they look the same while it zooms
    zn, zf = 0.25, 150
    for side in (-1, 1):
        b.append(poly([P(760 * side, GROUND, zn), P(760 * side, GROUND, zf), P(420 * side, GROUND, zf), P(420 * side, GROUND, zn)], "#aca79f"))
        b.append(poly([P(420 * side, GROUND, zn), P(420 * side, GROUND, zf), P(400 * side, GROUND + 14, zf), P(400 * side, GROUND + 14, zn)], "#d9d4ca"))
    b.append(poly([P(-400, GROUND + 14, zn), P(-400, GROUND + 14, zf), P(400, GROUND + 14, zf), P(400, GROUND + 14, zn)], "#55565e"))
    b.append(poly([P(-400, GROUND + 14, zn), P(-400, GROUND + 14, zf), P(-130, GROUND + 14, zn)], "#5d5f67"))
    base = svg(W, H, b, "Terraced street, vanishing at (640, 300). The base zoom-loops (backdrop.json zoom); lampposts, trees, cars and bins are sprites. Made by art/make_vlog.py.")

    lamp = svg(200, 1000, [
        rect(92, 60, 16, 940, "#3b4048"), rect(100, 60, 8, 940, "#4c525b"),
        poly([(70, 30), (130, 30), (122, 64), (78, 64)], "#2f3339"),
        poly([(80, 60), (120, 60), (114, 80), (86, 80)], "#fff1b8"),
        poly([(84, 975), (116, 975), (124, 1000), (76, 1000)], "#2f3339"),
    ], "Lamppost, base at the bottom centre.")
    tree = svg(400, 900, [
        poly([(188, 900), (212, 900), (206, 420), (194, 420)], "#5b3f2c"),
        poly([(200, 900), (212, 900), (206, 420), (200, 420)], "#6e4c35"),
        poly([(200, 560), (204, 520), (290, 430), (284, 424)], "#5b3f2c"),
        poly([(200, 0), (330, 90), (380, 260), (330, 430), (200, 480), (70, 430), (20, 260), (70, 90)], "#4f7a3f"),
        poly([(200, 0), (330, 90), (200, 200)], "#6a9a50"), poly([(330, 90), (380, 260), (200, 200)], "#5d8a47"),
        poly([(380, 260), (330, 430), (200, 200)], "#44693a"), poly([(330, 430), (200, 480), (200, 200)], "#3c5e33"),
        poly([(200, 480), (70, 430), (200, 200)], "#466e3b"), poly([(70, 430), (20, 260), (200, 200)], "#55833f"),
        poly([(20, 260), (70, 90), (200, 200)], "#6f9f52"), poly([(70, 90), (200, 0), (200, 200)], "#7aab5a"),
    ], "Street tree, trunk at the bottom centre.")
    car = svg(420, 300, [
        poly([(30, 270), (390, 270), (400, 170), (360, 140), (320, 60), (100, 60), (60, 140), (20, 170)], "#c0392b"),
        poly([(30, 270), (210, 270), (210, 60), (100, 60), (60, 140), (20, 170)], "#a93226"),
        poly([(110, 74), (310, 74), (340, 140), (80, 140)], "#7fa6bd"), poly([(110, 74), (210, 74), (200, 140), (80, 140)], "#9cc0d4"),
        rect(40, 170, 60, 22, "#f6c453"), rect(320, 170, 60, 22, "#f6c453"),
        rect(150, 200, 120, 30, "#f2f2ea"), rect(20, 240, 380, 26, "#2b2b30"),
        rect(40, 260, 60, 40, "#17171b"), rect(320, 260, 60, 40, "#17171b"),
    ], "Parked hatchback from behind, wheels at the bottom.")
    bin_ = svg(120, 200, [
        poly([(10, 20), (110, 20), (100, 190), (20, 190)], "#2e6b3a"), poly([(10, 20), (60, 20), (56, 190), (20, 190)], "#28603a"),
        poly([(4, 0), (116, 0), (116, 22), (4, 22)], "#24552e"), rect(14, 180, 22, 20, "#151515"), rect(84, 180, 22, 20, "#151515"),
    ], "Wheelie bin.")
    dash = svg(24, 160, [rect(0, 0, 24, 160, "#e8e2c8")], "Road centre dash, flat.")
    sprites = {
        "vanish": [VX, VY],
        "zoom": round(STREET_ZOOM, 4),
        "sprites": [
            {"src": "lamp.svg", "side": "both", "offset": 450, "y": GROUND, "height": 1000, "count": 3, "near": 0.5, "far": 12},
            {"src": "tree.svg", "side": "both", "offset": 600, "y": GROUND, "height": 900, "count": 3, "phase": 0.5, "near": 0.5, "far": 12},
            {"src": "bin.svg", "side": "left", "offset": 720, "y": GROUND, "height": 200, "count": 2, "phase": 0.25, "near": 0.5, "far": 12},
            {"src": "car.svg", "side": "right", "offset": 300, "y": GROUND + 14, "width": 420, "count": 2, "phase": 0.7, "near": 0.6, "far": 12},
            {"src": "dash.svg", "side": "centre", "y": GROUND + 14, "width": 18, "height": 220, "anchor": "top", "flat": True, "count": 16, "near": 0.9, "far": 25},
        ],
    }
    import json
    write("street", {"backdrop.svg": base, "lamp.svg": lamp, "tree.svg": tree, "car.svg": car, "bin.svg": bin_,
                     "dash.svg": dash, "backdrop.json": json.dumps(sprites, indent=2) + "\n"})


# ------------------------------------------------------------------ lounge
def lounge():
    rnd = seeded(5)
    b = []
    light = (1060, 200)

    def wall(cx, cy):
        k = max(0.0, 1 - math.hypot(cx - light[0], cy - light[1]) / 1100)
        return shade(mix("#3f5d5a", "#9cbcae", k ** 1.3), rnd.uniform(-0.04, 0.04))
    b += faceted(0, 0, W, H, 16, 9, rnd, wall)
    # skirting / floor glimpse at the very bottom corners is under the sofa
    # window on the right
    wx0, wy0, wx1, wy1 = 900, 70, 1220, 430
    b.append(rect(wx0 - 14, wy0 - 14, wx1 - wx0 + 28, wy1 - wy0 + 28, "#e9e4d8"))
    b += sky(rnd, wy1, "#7fb2d6", "#f6e7c5", wx0, wx1, (5, 4))[:0]
    def winsky(cx, cy):
        return shade(mix("#7fb2d6", "#f6e7c5", (cy - wy0) / (wy1 - wy0)), rnd.uniform(-0.03, 0.04))
    b += faceted(wx0, wy0, wx1, wy1, 5, 4, rnd, winsky)
    # rooftops across the road
    b.append(poly([(wx0, 330), (960, 300), (1010, 330), (1060, 290), (1120, 330), (1170, 300), (wx1, 320), (wx1, wy1), (wx0, wy1)], "#8a5442"))
    b.append(poly([(wx0, 360), (wx1, 350), (wx1, wy1), (wx0, wy1)], "#a2634d"))
    for x in (930, 1010, 1090, 1170):
        b.append(rect(x, 375, 24, 30, "#f3d98b"))
    b.append(rect(1056, wy0, 10, wy1 - wy0, "#e9e4d8"))
    b.append(rect(wx0, 246, wx1 - wx0, 10, "#e9e4d8"))
    # curtains
    for x0, x1 in ((860, 930), (1190, 1260)):
        for i in range(4):
            xa, xb = x0 + (x1 - x0) * i / 4, x0 + (x1 - x0) * (i + 1) / 4
            c = ["#b5452f", "#9b3a28", "#c45436", "#a33f2b"][i]
            b.append(poly([(xa, 50), (xb, 50), (xb + 4, 470), (xa - 2, 470)], c))
    b.append(rect(840, 40, 440, 12, "#3b2a22"))
    # standard lamp beside the sofa
    b.append(rect(1196, 330, 8, 400, "#2c2a2e"))
    b.append(poly([(1150, 260), (1250, 260), (1270, 340), (1130, 340)], "#f1d9a6"))
    b.append(poly([(1150, 260), (1200, 260), (1196, 340), (1130, 340)], "#e3c58c"))
    b.append(poly([(1130, 340), (1270, 340), (1330, 520), (1070, 520)], "#fff3cf", ' opacity="0.18"'))
    # vinyl shelving on the left: 3 x 4 cubes, a turntable on top
    sx0, sy0, cw, ch = 20, 150, 132, 132
    b.append(rect(sx0 - 10, sy0 - 12, cw * 3 + 20, ch * 5, "#c9a06e"))
    for r in range(5):
        for c in range(3):
            x, y = sx0 + c * cw, sy0 + r * ch
            b.append(rect(x + 6, y + 6, cw - 12, ch - 12, "#3a2a20"))
            b.append(poly([(x + 6, y + 6), (x + cw - 6, y + 6), (x + 6, y + ch - 6)], "#30221a"))
            b += spines(x + 8, y + 14, x + cw - 8, y + ch - 6, rnd, RECORD_COLORS)
    b.append(poly([(sx0 - 10, sy0 - 12), (sx0 + cw * 3 + 10, sy0 - 12), (sx0 + cw * 3 + 10, sy0 - 2), (sx0 - 10, sy0 - 2)], "#ddb886"))
    tx, ty = 110, sy0 - 12
    b.append(poly([(tx, ty), (tx + 190, ty), (tx + 186, ty - 30), (tx + 4, ty - 30)], "#2a2a2e"))
    b.append(poly([(tx + 4, ty - 30), (tx + 186, ty - 30), (tx + 180, ty - 36), (tx + 10, ty - 36)], "#3c3c42"))
    b += gem(tx + 80, ty - 38, 62, ["#111114", "#1d1d22", "#16161a", "#24242a"], n=10, squash=0.18)
    b.append(poly([(tx + 74, ty - 41), (tx + 86, ty - 41), (tx + 86, ty - 35), (tx + 74, ty - 35)], "#e76f51"))
    b.append(poly([(tx + 160, ty - 36), (tx + 166, ty - 36), (tx + 120, ty - 52), (tx + 116, ty - 48)], "#b9bec5"))
    # framed LP cover and a photo on the wall above the shelves' right edge
    b.append(rect(440, 90, 110, 110, "#1f1f24"))
    b.append(rect(448, 98, 94, 94, "#f2b134"))
    b.append(poly([(448, 98), (542, 98), (448, 192)], "#e8473c"))
    b += gem(495, 145, 26, ["#1b1b1b", "#2a2a2a"], n=8)
    b.append(rect(456, 230, 76, 96, "#6b4a33"))
    b.append(rect(462, 236, 64, 84, "#e9dcc3"))
    b.append(poly([(494, 250), (510, 262), (512, 286), (494, 296), (476, 286), (478, 262)], "#c79a7b"))
    b.append(poly([(470, 320), (480, 298), (508, 298), (518, 320)], "#4a5a6a"))
    # houseplant on the shelf top, right corner
    b.append(poly([(360, 138), (396, 138), (390, 104), (366, 104)], "#c96a3c"))
    for a, l, c in ((-1.9, 70, "#3f7a46"), (-1.3, 80, "#58985a"), (-0.8, 60, "#4b8a50"), (-2.5, 55, "#6aa865")):
        x2, y2 = 378 + math.cos(a) * l, 104 + math.sin(a) * l
        b.append(poly([(378, 104), (x2 - 10, y2 + 8), (x2, y2), (x2 + 10, y2 + 4)], c))
    # sofa back across the bottom (James sits in front of it)
    b.append(poly([(150, 520), (1130, 520), (1180, 720), (100, 720)], "#b5652f"))
    b.append(poly([(150, 520), (640, 520), (600, 720), (100, 720)], "#a65a2a"))
    b.append(poly([(150, 520), (1130, 520), (1124, 536), (156, 536)], "#c97a42"))
    for x0 in (170, 920):
        b.append(poly([(x0, 560), (x0 + 190, 548), (x0 + 200, 720), (x0 - 10, 720)], "#e9c46a"))
        b.append(poly([(x0, 560), (x0 + 190, 548), (x0 + 90, 640)], "#f2d07e"))
    b.append(poly([(60, 470), (170, 470), (170, 720), (50, 720)], "#9b4f25"))
    b.append(poly([(1110, 470), (1230, 470), (1240, 720), (1110, 720)], "#9b4f25"))
    write("lounge", {"backdrop.svg": svg(W, H, b, "Lounge: sofa in front of the vinyl shelves, window on the right. Made by art/make_vlog.py.")})


# ------------------------------------------------------------------ car
# One-point perspective from the dash mount looking back down the cabin.
# Cabin coordinates: X across (-1 .. 1 = the side walls), Y down (-0.62 roof,
# 0.05 the waistline), z away from the camera (3.2 = the tailgate).
CVX, CVY, CF = 640, 250, 700


def C(X, Y, z):
    return CVX + CF * X / z, CVY + CF * Y / z


def quad(X0, X1, Y0, Y1, z):
    """A face across the cabin at depth z."""
    return [C(X0, Y0, z), C(X1, Y0, z), C(X1, Y1, z), C(X0, Y1, z)]


def wall(side, Y0, Y1, z0, z1):
    """A patch of the side wall (X = +-1) between depths z0 and z1."""
    return [C(side, Y0, z0), C(side, Y0, z1), C(side, Y1, z1), C(side, Y1, z0)]


ROOF, WAIST, FLOOR, TAIL = -0.62, 0.05, 0.9, 2.7


def outside(clip_id, pts, rnd, ground_y):
    """Sky, a hedge and rooftops seen through a window, clipped to its glass."""
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    body = [f'<clipPath id="{clip_id}">{poly(pts, "#000")}</clipPath>', f'<g clip-path="url(#{clip_id})">']
    body += faceted(x0, y0, x1, y1, max(2, int((x1 - x0) / 120)), 2, rnd,
                    lambda cx, cy: shade(mix("#8fbad6", "#eadfc4", (cy - y0) / max(1, y1 - y0)), rnd.uniform(-0.03, 0.04)))
    hx = x0
    while hx < x1:   # rooftops
        w = rnd.uniform(40, 80)
        b2 = ground_y - rnd.uniform(18, 40)
        body.append(poly([(hx, ground_y + 40), (hx, b2), (hx + w / 2, b2 - 18), (hx + w, b2), (hx + w, ground_y + 40)], rnd.choice(["#9b5a44", "#b0654b", "#c9b394"])))
        hx += w
    body.append(rect(x0, ground_y, x1 - x0, y1 - ground_y + 40, "#4f7a3f"))
    body.append(poly([(x0, ground_y), (x1, ground_y + 6), (x1, ground_y + 14), (x0, ground_y + 10)], "#5f8a4a"))
    body.append("</g>")
    return body


def car():
    rnd = seeded(9)
    trim, trim_d, trim_l = "#3b3e46", "#30333a", "#4a4e57"
    b = [rect(0, 0, W, H, "#26282e")]
    # tailgate at the back: the rear window, the trim round it
    b.append(poly(quad(-1, 1, ROOF, FLOOR, TAIL), trim_d))
    rear_glass = quad(-0.82, 0.82, -0.52, WAIST - 0.02, TAIL)
    b += outside("rearwin", rear_glass, rnd, C(0, -0.12, TAIL)[1])
    for i in range(5):   # demister lines
        y = C(0, -0.44 + i * 0.09, TAIL)[1]
        b.append(f'<path d="M{C(-0.74, 0, TAIL)[0]:.0f} {y:.0f} H{C(0.74, 0, TAIL)[0]:.0f}" stroke="#b5574a" stroke-width="1.2" opacity="0.45"/>')
    # side walls: two windows a side (rear door glass, then the estate's quarter glass)
    for side in (-1, 1):
        b.append(poly(wall(side, ROOF, FLOOR, 0.4, TAIL), trim))
        b.append(poly(wall(side, WAIST, FLOOR, 0.4, TAIL), trim_d))
        for k, (z0, z1) in enumerate(((0.95, 1.65), (1.8, 2.55))):
            g = wall(side, ROOF + 0.07, WAIST, z0, z1)
            b += outside(f"side{side}{k}", g, rnd, C(side, -0.15, (z0 + z1) / 2)[1])
            b.append(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in g)}" fill="none" stroke="#1b1c20" stroke-width="5"/>')
        # pillars between the windows
        for z0, z1 in ((0.4, 0.95), (1.65, 1.8), (2.55, TAIL)):
            b.append(poly(wall(side, ROOF, WAIST, z0, z1), trim_l))
        b.append(poly(wall(side, WAIST, WAIST + 0.06, 0.4, TAIL), "#1f2126"))   # window sill
        b.append(poly(wall(side, 0.18, 0.24, 1.15, 1.35), "#8e949c"))   # door handle
    # roof lining with a courtesy light
    b.append(poly([C(-1, ROOF, 0.4), C(1, ROOF, 0.4), C(1, ROOF, TAIL), C(-1, ROOF, TAIL)], "#a9a69f"))
    rz = [0.4, 0.8, 1.3, 1.9, TAIL]
    for i in range(len(rz) - 1):
        for j, (xa, xb) in enumerate(((-1, -0.3), (-0.3, 0.3), (0.3, 1))):
            c = shade("#a9a69f", rnd.uniform(-0.08, 0.06) + (0.04 if j == 1 else -0.03))
            b.append(poly([C(xa, ROOF, rz[i]), C(xb, ROOF, rz[i]), C(xb, ROOF, rz[i + 1])], c))
            b.append(poly([C(xa, ROOF, rz[i]), C(xb, ROOF, rz[i + 1]), C(xa, ROOF, rz[i + 1])], shade(c, -0.04)))
    b.append(poly([C(-0.12, ROOF, 1.3), C(0.12, ROOF, 1.3), C(0.12, ROOF, 1.55), C(-0.12, ROOF, 1.55)], "#e8e4da"))
    b.append(poly([C(-0.08, ROOF, 1.34), C(0.08, ROOF, 1.34), C(0.08, ROOF, 1.51), C(-0.08, ROOF, 1.51)], "#fff5d6"))
    # the boot, inside the car: crates of records stacked against the tailgate,
    # drawn over the bottom of the rear glass
    for X0, z in ((-0.8, 2.55), (-0.36, 2.6), (0.04, 2.6), (0.44, 2.55), (-0.62, 2.35), (0.3, 2.38)):
        top = -0.26 if z > 2.45 else -0.17
        f = quad(X0, X0 + 0.38, top, 0.3, z)
        b.append(poly(f, "#8b6a45"))
        b.append(poly([f[0], f[1], f[3]], "#7d5e3c"))
        b.append(poly(quad(X0, X0 + 0.38, top, top + 0.025, z), "#a3825a"))
        (x0, y0), (x1, _) = f[0], f[1]
        b += spines(x0 + 3, y0 - 22, x1 - 3, y0 + 1, rnd, RECORD_COLORS, lean=False)
        hx, hy = C(X0 + 0.19, top + 0.12, z)
        b.append(rect(hx - 12, hy - 4, 24, 8, "#5b4329"))
    # rear seats: backs and headrests, across the cabin
    RZ = 2.05
    b.append(poly(quad(-1, 1, 0.0, FLOOR, RZ), "#34363e"))
    for X0, X1 in ((-1, -0.34), (-0.34, 0.34), (0.34, 1)):
        c = shade("#3a3c44", rnd.uniform(-0.04, 0.04))
        b.append(poly(quad(X0 + 0.03, X1 - 0.03, 0.02, 0.6, RZ), c))
        b.append(poly(quad(X0 + 0.03, X1 - 0.03, 0.02, 0.07, RZ), shade(c, 0.15)))
        b.append(poly([C(X0 + 0.03, 0.07, RZ), C(X0 + 0.15, 0.07, RZ), C(X0 + 0.15, 0.6, RZ), C(X0 + 0.03, 0.6, RZ)], shade(c, 0.07)))
    # the empty passenger seat (screen right) and James's seat behind him
    for Xc, z, c in ((0.72, 1.55, "#2a2c33"), (0.0, 1.4, "#26282e")):
        # backrest: tapered, with side bolsters and a lit facet
        tl, tr = C(Xc - 0.3, 0.08, z), C(Xc + 0.3, 0.08, z)
        bl, br = C(Xc - 0.4, 1.25, z), C(Xc + 0.4, 1.25, z)
        b.append(poly([tl, tr, br, bl], c))
        ml, mr = C(Xc - 0.18, 0.12, z), C(Xc + 0.18, 0.12, z)
        b.append(poly([tl, ml, C(Xc - 0.24, 1.25, z), bl], shade(c, 0.12)))
        b.append(poly([mr, tr, br, C(Xc + 0.24, 1.25, z)], shade(c, 0.06)))
        b.append(poly([ml, C(Xc, 0.1, z), C(Xc, 1.25, z), C(Xc - 0.24, 1.25, z)], shade(c, 0.03)))
        b.append(poly([tl, tr, C(Xc + 0.27, 0.16, z), C(Xc - 0.27, 0.16, z)], shade(c, 0.18)))
        # headrest: a faceted cushion on two posts
        for dx in (-0.1, 0.07):
            b.append(poly(quad(Xc + dx, Xc + dx + 0.03, 0.0, 0.1, z), "#8e949c"))
        hr = [C(Xc - 0.15, -0.24, z), C(Xc + 0.15, -0.24, z), C(Xc + 0.19, -0.15, z), C(Xc + 0.17, 0.02, z),
              C(Xc - 0.17, 0.02, z), C(Xc - 0.19, -0.15, z)]
        b.append(poly(hr, shade(c, -0.02)))
        b.append(poly([hr[0], hr[1], hr[2], hr[5]], shade(c, 0.14)))
        b.append(poly([hr[5], C(Xc, -0.15, z), hr[4]], shade(c, 0.05)))
    write("car", {"backdrop.svg": svg(W, H, b, "Estate car from the dash mount, one-point perspective; crates of vinyl in the boot. Made by art/make_vlog.py.")})


# ------------------------------------------------------------------ high street (scroll)
def high_street():
    rnd = seeded(13)
    b = []
    b += sky(rnd, 120, "#86b4d3", "#d7e4e6")
    # upper floors: brick with sash windows, across the whole width (tiles)
    def brick(cx, cy):
        return shade("#9b5a44", rnd.uniform(-0.07, 0.06))
    b += faceted(0, 60, W, 300, 16, 3, rnd, brick, jitter=0.3)
    b.append(rect(0, 50, W, 14, "#4c4f57"))
    shops = [
        ("PEMBERTON & GALL", "SOLICITORS · EST. 1962", "#1f4d3a", "#d8b45a", "#f3ead2"),
        ("SPIN CYCLE", "RECORDS · BOUGHT & SOLD", "#e07a2f", "#1d2b36", "#fff2dc"),
        ("THE DAILY GRIND", "COFFEE · TEA · CAKE", "#7b2d26", "#f4e1c1", "#f4e1c1"),
        ("FONE DOCTOR", "UNLOCKING · REPAIRS", "#1f5fa8", "#ffffff", "#d6ecff"),
    ]
    for i, (name, sub, main, ink, glass) in enumerate(shops):
        x0 = i * 320 + 6
        x1 = x0 + 308
        for wx in (x0 + 40, x0 + 180):   # sash windows upstairs
            b.append(rect(wx, 110, 90, 130, "#efe8da"))
            b.append(rect(wx + 6, 116, 78, 56, "#7ea6c0"))
            b.append(rect(wx + 6, 178, 78, 56, "#8fb5cc"))
            b.append(poly([(wx + 6, 116), (wx + 50, 116), (wx + 6, 160)], "#a5c6d9"))
            b.append(rect(wx - 6, 240, 102, 10, "#d9d0bf"))
        b.append(rect(x0, 300, 308, 60, main))
        b.append(rect(x0, 300, 308, 6, shade(main, -0.3)))
        b.append(text((x0 + x1) / 2, 336, name, 26 if len(name) < 14 else 22, ink, family="Georgia, 'Times New Roman', serif" if i == 0 else "Arial Black, Arial, sans-serif"))
        b.append(text((x0 + x1) / 2, 354, sub, 11, ink, weight="700", family="Arial, Helvetica, sans-serif"))
        b.append(rect(x0, 360, 308, 300, shade(main, -0.15)))
        b.append(rect(x0 + 16, 380, 190, 240, shade(glass, -0.15)))
        b.append(poly([(x0 + 16, 380), (x0 + 120, 380), (x0 + 16, 520)], shade(glass, 0.15), ' opacity="0.8"'))
        b.append(rect(x0 + 226, 380, 66, 270, shade(main, -0.35)))
        b.append(rect(x0 + 276, 510, 6, 18, "#d8b45a"))
        # window displays
        if i == 0:   # files, a plaque, a dusty plant
            for k in range(5):
                b.append(rect(x0 + 30 + k * 24, 560 - k * 6, 20, 60 + k * 6, ["#c7b48a", "#a8936a", "#d9c9a0"][k % 3]))
            b.append(rect(x0 + 230, 420, 58, 40, "#d8b45a"))
            b.append(text(x0 + 259, 446, "P&G", 14, "#1f4d3a", family="Georgia, serif"))
        elif i == 1:  # records in the window
            for k in range(3):
                b += gem(x0 + 60 + k * 60, 470 + (k % 2) * 40, 26, ["#141418", "#26262c"], n=8)
                b.append(rect(x0 + 52 + k * 60, 462 + (k % 2) * 40, 16, 16, RECORD_COLORS[k * 3]))
            b += spines(x0 + 24, 560, x0 + 200, 618, rnd, RECORD_COLORS, lean=False)
        elif i == 2:  # awning stripes and a cake stand
            for k in range(8):
                b.append(poly([(x0 + k * 38.5, 362), (x0 + (k + 1) * 38.5, 362), (x0 + (k + 1) * 38.5 + 6, 392), (x0 + k * 38.5 + 6, 392)],
                              "#f4e1c1" if k % 2 else "#7b2d26"))
            b.append(poly([(x0 + 70, 560), (x0 + 150, 560), (x0 + 140, 530), (x0 + 80, 530)], "#e9c46a"))
            b.append(rect(x0 + 106, 560, 8, 50, "#cfcfcf"))
        else:         # phones and a "WE UNLOCK ANY PHONE" card
            for k in range(4):
                b.append(rect(x0 + 34 + k * 42, 480, 28, 54, "#1b1b1f"))
                b.append(rect(x0 + 37 + k * 42, 484, 22, 44, "#4aa3ff"))
            b.append(rect(x0 + 30, 560, 160, 40, "#ffffff"))
            b.append(text(x0 + 110, 585, "WE UNLOCK ANY PHONE*", 12, "#c0392b", family="Arial Black, Arial, sans-serif"))
        b.append(rect(x0 - 6, 300, 6, 360, "#d9d0bf"))
    # pavement
    b.append(rect(0, 660, W, 60, "#a9a49c"))
    for k in range(0, W, 160):
        b.append(f'<path d="M{k} 660 V720" stroke="#8f8a82" stroke-width="2"/>')
    b.append(rect(0, 656, W, 6, "#7c776f"))
    write("high_street", {"backdrop.svg": svg(W, H, b, "High street shop fronts, side-on; tiles left to right for scroll. Made by art/make_vlog.py.")})


def main():
    street()
    lounge()
    car()
    high_street()
    print("wrote street, lounge, car, high_street")


if __name__ == "__main__":
    main()
