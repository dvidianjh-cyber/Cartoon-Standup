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


def street():
    rnd = seeded(21)
    b = []
    b += sky(rnd, 320)
    b += cloud(250, 90, 1.2) + cloud(1010, 60, 0.9) + cloud(760, 150, 0.6)
    # far end of the street: a hazy terrace across the vanishing point
    b.append(poly([(540, 250), (600, 236), (680, 236), (740, 250), (740, 312), (540, 312)], "#b98d7a"))
    b.append(poly([(540, 250), (600, 236), (640, 236), (640, 312), (540, 312)], "#c79b86"))
    zs = [0.5, 0.75, 1.05, 1.45, 2.0, 2.7, 3.6, 4.8, 6.5, 9, 13, 20]
    EAVES = -380                 # two storeys
    for side in (-1, 1):
        X = 760 * side
        for i in range(len(zs) - 1):
            za, zb = zs[i], zs[i + 1]
            zm = lambda f: za + (zb - za) * f
            base = ["#a65a43", "#93503c", "#b0654b"][i % 3] if side < 0 else ["#c9b394", "#b89f80", "#d4bf9f"][i % 3]
            fog = min(0.5, i * 0.05)
            c = mix(base, "#d9c4b0", fog)
            # pitched slate roof, then the facade
            b.append(poly([P(X, EAVES, za), P(X, EAVES, zb), P(X * 1.3, EAVES - 170, zb), P(X * 1.3, EAVES - 170, za)], mix("#4c5560", "#9aa0a8", fog)))
            b.append(poly([P(X, EAVES, za), P(X * 1.3, EAVES - 170, zm(0.5)), P(X * 1.3, EAVES - 170, za)], mix("#5a6470", "#9aa0a8", fog)))
            if i % 2 == 0:   # chimney stack on the party wall
                b.append(poly([P(X * 1.12, EAVES - 60, za), P(X * 1.12, EAVES - 60, zm(0.12)), P(X * 1.12, EAVES - 230, zm(0.12)), P(X * 1.12, EAVES - 230, za)], shade(c, -0.15)))
            b.append(poly([P(X, EAVES, za), P(X, EAVES, zb), P(X, GROUND - 130, zb), P(X, GROUND - 130, za)], c))
            b.append(poly([P(X, EAVES, za), P(X, EAVES, zb), P(X, -150, za)], shade(c, 0.07)))
            b.append(poly([P(X, -60, za), P(X, -60, zb), P(X, GROUND - 130, zb), P(X, GROUND - 130, za)], shade(c, -0.06)))
            frame, glass = mix("#efe8da", "#d9c4b0", fog), mix("#34495a", "#9fb2bf", fog)
            # upstairs sash window, downstairs bay and the front door
            for (f0, f1, y0, y1) in ((0.15, 0.5, -320, -170), (0.1, 0.55, -40, 140)):
                b.append(poly([P(X, y0, zm(f0)), P(X, y0, zm(f1)), P(X, y1, zm(f1)), P(X, y1, zm(f0))], frame))
                b.append(poly([P(X, y0 + 14, zm(f0 + 0.04)), P(X, y0 + 14, zm(f1 - 0.04)), P(X, y1 - 14, zm(f1 - 0.04)), P(X, y1 - 14, zm(f0 + 0.04))], glass))
            door = ["#1f4d3a", "#7b2d26", "#1f5fa8", "#2b2b30", "#d8b45a"][i % 5]
            b.append(poly([P(X, -20, zm(0.68)), P(X, -20, zm(0.86)), P(X, GROUND - 130, zm(0.86)), P(X, GROUND - 130, zm(0.68))], mix(door, "#d9c4b0", fog)))
            b.append(poly([P(X, -360, zm(0.98)), P(X, -360, zb), P(X, GROUND - 130, zb), P(X, GROUND - 130, zm(0.98))], shade(c, -0.25)))
            # low front wall and hedge along the pavement
            b.append(poly([P(X, GROUND - 130, za), P(X, GROUND - 130, zb), P(X, GROUND, zb), P(X, GROUND, za)], mix("#3f6b3a", "#9fb08f", fog)))
            b.append(poly([P(X, GROUND - 130, za), P(X, GROUND - 60, zb), P(X, GROUND, za)], mix("#355c31", "#9fb08f", fog)))
        for Y, col, w in ((EAVES, "#3a3a40", 4), (-60, "#e9dccb", 3)):
            a2, c2 = P(X, Y, 0.5), P(X, Y, 20)
            b.append(f'<path d="M{a2[0]:.1f} {a2[1]:.1f} L{c2[0]:.1f} {c2[1]:.1f}" stroke="{col}" stroke-width="{w}" opacity="0.7"/>')
    # pavements and road
    for side in (-1, 1):
        b.append(poly([P(760 * side, GROUND, 0.5), P(760 * side, GROUND, 20), P(420 * side, GROUND, 20), P(420 * side, GROUND, 0.55)], "#a9a49c"))
        b.append(poly([P(760 * side, GROUND, 0.55), P(600 * side, GROUND, 20), P(420 * side, GROUND, 0.55)], "#b8b3aa"))
        b.append(poly([P(420 * side, GROUND, 0.55), P(420 * side, GROUND, 20), P(400 * side, GROUND + 14, 20), P(400 * side, GROUND + 14, 0.55)], "#d9d4ca"))
    b.append(poly([P(-400, GROUND + 14, 0.55), P(-400, GROUND + 14, 20), P(400, GROUND + 14, 20), P(400, GROUND + 14, 0.55)], "#55565e"))
    b.append(poly([P(-400, GROUND + 14, 0.55), P(0, GROUND + 14, 20), P(-120, GROUND + 14, 0.55)], "#5e6068"))
    base = svg(W, H, b, "Terraced street, vanishing at (640, 300). Lampposts, trees, cars and bins are sprites (backdrop.json). Made by art/make_vlog.py.")

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
def car():
    rnd = seeded(9)
    b = [rect(0, 0, W, H, "#2b2d33")]
    # rear window behind the seats: street outside
    rx0, ry0, rx1, ry1 = 300, 110, 1000, 330
    def out(cx, cy):
        return shade(mix("#8fbad6", "#e8dcc0", (cy - ry0) / (ry1 - ry0)), rnd.uniform(-0.03, 0.04))
    b += faceted(rx0, ry0, rx1, ry1, 7, 3, rnd, out)
    b.append(poly([(rx0, 270), (420, 240), (520, 262), (640, 236), (760, 258), (880, 240), (rx1, 262), (rx1, ry1), (rx0, ry1)], "#8a6150"))
    b.append(poly([(rx0, 300), (rx1, 296), (rx1, ry1), (rx0, ry1)], "#5f7d4f"))
    for i in range(8):
        b.append(f'<path d="M{rx0 + 20} {ry0 + 30 + i * 22} H{rx1 - 20}" stroke="#c74a3a" stroke-width="1.5" opacity="0.35"/>')
    # roof lining
    def roof(cx, cy):
        return shade(mix("#b9b6ae", "#8e8b84", cy / 120), rnd.uniform(-0.04, 0.04))
    b += faceted(0, 0, W, 112, 12, 2, rnd, roof)
    b.append(poly([(590, 20), (690, 20), (680, 44), (600, 44)], "#d9d6cf"))
    b.append(poly([(606, 26), (674, 26), (668, 40), (612, 40)], "#fff5d6"))
    b.append(poly([(rx0 - 20, 100), (rx1 + 20, 100), (rx1, ry0), (rx0, ry0)], "#5c5a57"))
    # boot full of record crates, seen through the rear window either side of the headrest
    for cx, cy in ((390, 262), (470, 276), (820, 270), (920, 258)):
        b.append(poly([(cx - 48, cy), (cx + 48, cy), (cx + 48, cy + 70), (cx - 48, cy + 70)], "#8b6a45"))
        b.append(poly([(cx - 48, cy), (cx, cy), (cx - 48, cy + 70)], "#7a5b3a"))
        b += spines(cx - 44, cy - 30, cx + 44, cy + 2, rnd, RECORD_COLORS, lean=False)
        b.append(rect(cx - 18, cy + 18, 36, 10, "#5b4329"))
    b.append(rect(rx0, 326, rx1 - rx0, 10, "#3f4148"))
    # rear seat back
    b.append(poly([(0, 470), (1280, 470), (1280, 720), (0, 720)], "#3a3c44"))
    b += faceted(0, 470, W, H, 12, 2, rnd, lambda cx, cy: shade("#3a3c44", rnd.uniform(-0.1, 0.08)))
    # left: driver's door with its window (UK car, camera on the dash looking back)
    def side(cx, cy):
        return shade(mix("#9cc3d9", "#dfe8d0", cy / 420), rnd.uniform(-0.03, 0.04))
    b.append(poly([(0, 60), (260, 112), (300, 430), (0, 460)], "#1e1f24"))
    b += [p for p in faceted(0, 80, 270, 420, 3, 4, rnd, side)]
    b.append(poly([(0, 300), (60, 280), (120, 300), (190, 270), (270, 300), (270, 420), (0, 420)], "#4f7a3f"))
    b.append(poly([(0, 330), (270, 330), (270, 420), (0, 420)], "#3f6b3a"))
    b.append(poly([(255, 90), (300, 100), (330, 470), (285, 470)], "#2a2b31"))
    b.append(poly([(0, 420), (300, 430), (310, 720), (0, 720)], "#474a53"))
    b.append(poly([(0, 520), (290, 500), (296, 540), (0, 560)], "#363840"))
    b.append(poly([(200, 470), (260, 466), (262, 486), (202, 490)], "#9aa0a8"))
    # driver's seat behind James: headrest and the seat's wings
    b.append(poly([(520, 150), (760, 150), (780, 300), (500, 300)], "#24262c"))
    b.append(poly([(520, 150), (640, 150), (640, 300), (500, 300)], "#1d1f24"))
    b.append(poly([(600, 300), (620, 300), (620, 330), (600, 330)], "#9aa0a8"))
    b.append(poly([(660, 300), (680, 300), (680, 330), (660, 330)], "#9aa0a8"))
    b.append(poly([(420, 330), (860, 330), (900, 720), (380, 720)], "#2a2c33"))
    b.append(poly([(420, 330), (480, 330), (440, 720), (380, 720)], "#353841"))
    b.append(poly([(800, 330), (860, 330), (900, 720), (840, 720)], "#353841"))
    # right: the empty passenger seat
    b.append(poly([(1000, 170), (1180, 170), (1196, 290), (986, 290)], "#24262c"))
    b.append(poly([(1000, 170), (1090, 170), (1090, 290), (986, 290)], "#1d1f24"))
    b.append(poly([(940, 320), (1260, 320), (1290, 720), (910, 720)], "#2a2c33"))
    b.append(poly([(940, 320), (1100, 320), (1080, 720), (910, 720)], "#30323a"))
    # seat belt hanging on the B-pillar
    b.append(poly([(286, 130), (300, 130), (360, 720), (342, 720)], "#15161a"))
    write("car", {"backdrop.svg": svg(W, H, b, "Estate car from the dash mount: driver's seat, crates of vinyl in the boot. Made by art/make_vlog.py.")})


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
