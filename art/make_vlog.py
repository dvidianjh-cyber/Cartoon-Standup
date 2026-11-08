"""Draw the vlog locations in the faceted low-poly style, portrait (720x1280,
as if filmed on a phone; series.yaml `format: portrait`).

Usage: python3 art/make_vlog.py   (from the series repo's top folder)

  show/backdrops/street/      terraced street, walking towards the camera (depth
                              backdrop: zoom-looped base plus synced sprites in backdrop.json)
  show/backdrops/lounge/      sofa in front of the vinyl shelves and a window (static)
  show/backdrops/car/         inside the estate car from the dash mount; the driver's
                              seat (right-hand drive) is on screen-left (static)
  show/backdrops/high_street/ the shops across the road, seen from the near pavement (static)
  show/backdrops/black/       plain black, for the blackout before the end card
  show/sets/<car>_l|_r/       cars side-on driving left / right, for passing traffic

Selfie close-ups put James's eyes at about y 520 with his head across x 225-495
and his shoulders filling the bottom, so the detail is above and at the sides.
"""
import json
import math
from pathlib import Path

from lowpoly import (RECORD_COLORS, faceted, gem, mix, poly, rect, seeded, shade, spines, svg, text)

SHOW = Path(__file__).resolve().parent.parent / "show"
ROOT = SHOW / "backdrops"
W, H = 720, 1280


def write(name, files, root=ROOT):
    d = root / name
    d.mkdir(parents=True, exist_ok=True)
    for fn, content in files.items():
        (d / fn).write_text(content, encoding="utf-8")


# ------------------------------------------------------------------ street (depth)
VX, VY = 360, 470          # vanishing point, at about eye height
S = 0.8                    # street units -> backdrop px at depth 1
GROUND = 420               # ground is this far below the vanishing point at depth 1 (street units)


def P(X, Y, z):
    return VX + S * X / z, VY + S * Y / z


# House fronts are spaced by a constant depth ratio and the colours repeat
# every HOUSE_REPEAT houses, so the base image maps onto itself when scaled by
# STREET_ZOOM about the vanishing point. backdrop.json sets that zoom, so the
# engine zoom-loops the base (the houses go by), and `sync` moves the sprites in
# step with it: everything at the same depth drifts at the same speed.
HOUSE_RATIO = 1.32
HOUSE_REPEAT = 3
STREET_ZOOM = HOUSE_RATIO ** HOUSE_REPEAT


def street():
    b = ['<defs><linearGradient id="sky" gradientUnits="userSpaceOnUse" x1="0" y1="-300" x2="0" y2="470">'
         '<stop offset="0" stop-color="#86b4d3"/><stop offset="1" stop-color="#f2e3c4"/></linearGradient></defs>',
         rect(-3000, -3000, 6720, 3470, "url(#sky)")]
    zs = [0.2 * HOUSE_RATIO ** k for k in range(26)]
    EAVES = -380                 # two storeys
    for side in (-1, 1):
        X = 760 * side
        for i in range(len(zs) - 1):
            za, zb = zs[i], zs[i + 1]
            zm = lambda f: za + (zb - za) * f
            k = i % HOUSE_REPEAT
            c = ["#a65a43", "#93503c", "#b0654b"][k] if side < 0 else ["#c9b394", "#b89f80", "#d4bf9f"][k]
            roof = "#4c5560"
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
            b.append(poly([P(X, GROUND - 130, za), P(X, GROUND - 130, zb), P(X, GROUND, zb), P(X, GROUND, za)], "#3f6b3a"))
            b.append(poly([P(X, GROUND - 130, za), P(X, GROUND - 60, zb), P(X, GROUND, za)], "#355c31"))
        for Y, col, w in ((EAVES, "#3a3a40", 3), (-60, "#e9dccb", 2)):
            a2, c2 = P(X, Y, zs[0]), P(X, Y, zs[-1])
            b.append(f'<path d="M{a2[0]:.1f} {a2[1]:.1f} L{c2[0]:.1f} {c2[1]:.1f}" stroke="{col}" stroke-width="{w}" opacity="0.7"/>')
    # pavements and road: only lines along the street, so they look the same while it zooms
    zn, zf = 0.2, 150
    for side in (-1, 1):
        b.append(poly([P(760 * side, GROUND, zn), P(760 * side, GROUND, zf), P(420 * side, GROUND, zf), P(420 * side, GROUND, zn)], "#aca79f"))
        b.append(poly([P(420 * side, GROUND, zn), P(420 * side, GROUND, zf), P(400 * side, GROUND + 14, zf), P(400 * side, GROUND + 14, zn)], "#d9d4ca"))
    b.append(poly([P(-400, GROUND + 14, zn), P(-400, GROUND + 14, zf), P(400, GROUND + 14, zf), P(400, GROUND + 14, zn)], "#55565e"))
    b.append(poly([P(-400, GROUND + 14, zn), P(-400, GROUND + 14, zf), P(-130, GROUND + 14, zn)], "#5d5f67"))
    base = svg(W, H, b, "Terraced street, portrait, vanishing at (360, 470). The base zoom-loops (backdrop.json zoom); lampposts, trees, cars and bins are synced sprites. Made by art/make_vlog.py.")

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
    car2 = car.replace("#c0392b", "#2f6fa8").replace("#a93226", "#285f91")
    bin_ = svg(120, 200, [
        poly([(10, 20), (110, 20), (100, 190), (20, 190)], "#2e6b3a"), poly([(10, 20), (60, 20), (56, 190), (20, 190)], "#28603a"),
        poly([(4, 0), (116, 0), (116, 22), (4, 22)], "#24552e"), rect(14, 180, 22, 20, "#151515"), rect(84, 180, 22, 20, "#151515"),
    ], "Wheelie bin.")
    dash = svg(24, 160, [rect(0, 0, 24, 160, "#e8e2c8")], "Road centre dash, flat.")

    def s(v):
        return round(v * S, 1)
    # Sprite depths: `near`..`far` with copies spaced evenly in log depth (sync). Keep far/near a whole
    # power of the zoom so the spacing matches the houses' repeat.
    zr = STREET_ZOOM
    sprites = {
        "vanish": [VX, VY],
        "zoom": round(zr, 4),
        "sync": True,
        "sprites": [
            {"src": "lamp.svg", "side": "both", "offset": s(450), "y": s(GROUND), "height": s(1000), "count": 3, "near": 0.35, "far": round(0.35 * zr ** 3, 2)},
            {"src": "tree.svg", "side": "both", "offset": s(600), "y": s(GROUND), "height": s(900), "count": 3, "phase": 0.5, "near": 0.35, "far": round(0.35 * zr ** 3, 2)},
            {"src": "bin.svg", "side": "left", "offset": s(720), "y": s(GROUND), "height": s(200), "count": 3, "phase": 0.2, "near": 0.35, "far": round(0.35 * zr ** 3, 2)},
            {"src": "car.svg", "side": "right", "offset": s(300), "y": s(GROUND + 14), "width": s(420), "count": 2, "phase": 0.7, "near": 0.45, "far": round(0.45 * zr ** 2, 2)},
            {"src": "car2.svg", "side": "left", "offset": s(300), "y": s(GROUND + 14), "width": s(420), "count": 1, "phase": 0.35, "near": 0.45, "far": round(0.45 * zr, 2)},
            {"src": "dash.svg", "side": "centre", "y": s(GROUND + 14), "width": s(18), "height": s(220), "anchor": "top", "flat": True, "count": 12, "near": 0.6, "far": round(0.6 * zr ** 3, 2)},
        ],
    }
    write("street", {"backdrop.svg": base, "lamp.svg": lamp, "tree.svg": tree, "car.svg": car, "car2.svg": car2, "bin.svg": bin_,
                     "dash.svg": dash, "backdrop.json": json.dumps(sprites, indent=2) + "\n"})


# ------------------------------------------------------------------ lounge
def lounge():
    rnd = seeded(5)
    b = []
    light = (620, 160)

    def wall(cx, cy):
        k = max(0.0, 1 - math.hypot(cx - light[0], cy - light[1]) / 1000)
        return shade(mix("#3f5d5a", "#9cbcae", k ** 1.3), rnd.uniform(-0.04, 0.04))
    b += faceted(0, 0, W, H, 9, 16, rnd, wall)
    # window, top right
    wx0, wy0, wx1, wy1 = 490, 120, 700, 560
    b.append(rect(wx0 - 14, wy0 - 14, wx1 - wx0 + 28, wy1 - wy0 + 28, "#e9e4d8"))

    def winsky(cx, cy):
        return shade(mix("#7fb2d6", "#f6e7c5", (cy - wy0) / (wy1 - wy0)), rnd.uniform(-0.03, 0.04))
    b += faceted(wx0, wy0, wx1, wy1, 3, 5, rnd, winsky)
    b.append(poly([(wx0, 430), (530, 400), (570, 430), (610, 390), (650, 430), (690, 400), (wx1, 420), (wx1, wy1), (wx0, wy1)], "#8a5442"))
    b.append(poly([(wx0, 460), (wx1, 450), (wx1, wy1), (wx0, wy1)], "#a2634d"))
    for x in (510, 570, 630, 680):
        b.append(rect(x, 478, 18, 26, "#f3d98b"))
    b.append(rect(592, wy0, 10, wy1 - wy0, "#e9e4d8"))
    b.append(rect(wx0, 330, wx1 - wx0, 10, "#e9e4d8"))
    # curtains
    for x0, x1 in ((452, 510), (690, 740)):
        for i in range(4):
            xa, xb = x0 + (x1 - x0) * i / 4, x0 + (x1 - x0) * (i + 1) / 4
            c = ["#b5452f", "#9b3a28", "#c45436", "#a33f2b"][i]
            b.append(poly([(xa, 100), (xb, 100), (xb + 4, 600), (xa - 2, 600)], c))
    b.append(rect(440, 90, 300, 12, "#3b2a22"))
    # standard lamp beside the sofa, right
    b.append(rect(656, 760, 8, 400, "#2c2a2e"))
    b.append(poly([(610, 680), (710, 680), (730, 760), (590, 760)], "#f1d9a6"))
    b.append(poly([(610, 680), (660, 680), (656, 760), (590, 760)], "#e3c58c"))
    b.append(poly([(590, 760), (730, 760), (790, 960), (530, 960)], "#fff3cf", ' opacity="0.18"'))
    # vinyl shelving on the left: 2 wide x 6 high, a turntable on top
    sx0, sy0, cw, ch = 14, 200, 128, 128
    b.append(rect(sx0 - 10, sy0 - 12, cw * 2 + 20, ch * 7, "#c9a06e"))
    for r in range(7):
        for c in range(2):
            x, y = sx0 + c * cw, sy0 + r * ch
            b.append(rect(x + 6, y + 6, cw - 12, ch - 12, "#3a2a20"))
            b.append(poly([(x + 6, y + 6), (x + cw - 6, y + 6), (x + 6, y + ch - 6)], "#30221a"))
            b += spines(x + 8, y + 14, x + cw - 8, y + ch - 6, rnd, RECORD_COLORS)
    b.append(poly([(sx0 - 10, sy0 - 12), (sx0 + cw * 2 + 10, sy0 - 12), (sx0 + cw * 2 + 10, sy0 - 2), (sx0 - 10, sy0 - 2)], "#ddb886"))
    tx, ty = 40, sy0 - 12
    b.append(poly([(tx, ty), (tx + 180, ty), (tx + 176, ty - 30), (tx + 4, ty - 30)], "#2a2a2e"))
    b.append(poly([(tx + 4, ty - 30), (tx + 176, ty - 30), (tx + 170, ty - 36), (tx + 10, ty - 36)], "#3c3c42"))
    b += gem(tx + 76, ty - 38, 58, ["#111114", "#1d1d22", "#16161a", "#24242a"], n=10, squash=0.18)
    b.append(poly([(tx + 70, ty - 41), (tx + 82, ty - 41), (tx + 82, ty - 35), (tx + 70, ty - 35)], "#e76f51"))
    b.append(poly([(tx + 150, ty - 36), (tx + 156, ty - 36), (tx + 112, ty - 52), (tx + 108, ty - 48)], "#b9bec5"))
    # framed LP cover above James's head
    b.append(rect(300, 110, 120, 120, "#1f1f24"))
    b.append(rect(308, 118, 104, 104, "#f2b134"))
    b.append(poly([(308, 118), (412, 118), (308, 222)], "#e8473c"))
    b += gem(360, 170, 28, ["#1b1b1b", "#2a2a2a"], n=8)
    # sofa back across the bottom (James sits in front of it)
    b.append(poly([(20, 960), (700, 960), (740, 1280), (-20, 1280)], "#b5652f"))
    b.append(poly([(20, 960), (360, 960), (330, 1280), (-20, 1280)], "#a65a2a"))
    b.append(poly([(20, 960), (700, 960), (696, 978), (24, 978)], "#c97a42"))
    for x0 in (40, 520):
        b.append(poly([(x0, 1010), (x0 + 160, 998), (x0 + 170, 1280), (x0 - 10, 1280)], "#e9c46a"))
        b.append(poly([(x0, 1010), (x0 + 160, 998), (x0 + 80, 1110)], "#f2d07e"))
    b.append(poly([(-10, 900), (40, 900), (40, 1280), (-10, 1280)], "#9b4f25"))
    b.append(poly([(680, 900), (730, 900), (730, 1280), (680, 1280)], "#9b4f25"))
    write("lounge", {"backdrop.svg": svg(W, H, b, "Lounge, portrait: vinyl shelves on the left, window on the right, sofa back across the bottom. Made by art/make_vlog.py.")})


# ------------------------------------------------------------------ car
# One-point perspective from the phone on the dash mount, looking back down the cabin.
# Cabin coordinates: X across (-1 .. 1 = the side walls; -1 is the car's right, the
# driver's side in a right-hand-drive car, which the camera sees on screen-left),
# Y down (-0.62 roof, 0.05 the waistline), z away from the camera (2.7 = the tailgate).
# The mount sits a little towards the driver (CAM_X), so the driver's seat is at x ~230
# and the empty passenger seat fills the right of the frame.
CVY, CF, CAM_X = 470, 560, -0.22


def C(X, Y, z):
    return W / 2 + CF * (X - CAM_X) / z, CVY + CF * Y / z


def quad(X0, X1, Y0, Y1, z):
    """A face across the cabin at depth z."""
    return [C(X0, Y0, z), C(X1, Y0, z), C(X1, Y1, z), C(X0, Y1, z)]


def wallp(side, Y0, Y1, z0, z1):
    """A patch of the side wall (X = +-1) between depths z0 and z1."""
    return [C(side, Y0, z0), C(side, Y0, z1), C(side, Y1, z1), C(side, Y1, z0)]


ROOF, WAIST, FLOOR, TAIL = -0.62, 0.05, 0.9, 2.7
DRIVER_X, PASSENGER_X = -0.5, 0.5


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
        w = rnd.uniform(30, 60)
        b2 = ground_y - rnd.uniform(14, 30)
        body.append(poly([(hx, ground_y + 40), (hx, b2), (hx + w / 2, b2 - 14), (hx + w, b2), (hx + w, ground_y + 40)], rnd.choice(["#9b5a44", "#b0654b", "#c9b394"])))
        hx += w
    body.append(rect(x0, ground_y, x1 - x0, y1 - ground_y + 40, "#4f7a3f"))
    body.append(poly([(x0, ground_y), (x1, ground_y + 6), (x1, ground_y + 14), (x0, ground_y + 10)], "#5f8a4a"))
    body.append("</g>")
    return body


def seat(Xc, z, c, b):
    """A front seat: tapered backrest with bolsters, a headrest on two posts."""
    tl, tr = C(Xc - 0.3, 0.08, z), C(Xc + 0.3, 0.08, z)
    bl, br = C(Xc - 0.4, 1.25, z), C(Xc + 0.4, 1.25, z)
    b.append(poly([tl, tr, br, bl], c))
    ml, mr = C(Xc - 0.18, 0.12, z), C(Xc + 0.18, 0.12, z)
    b.append(poly([tl, ml, C(Xc - 0.24, 1.25, z), bl], shade(c, 0.12)))
    b.append(poly([mr, tr, br, C(Xc + 0.24, 1.25, z)], shade(c, 0.06)))
    b.append(poly([ml, C(Xc, 0.1, z), C(Xc, 1.25, z), C(Xc - 0.24, 1.25, z)], shade(c, 0.03)))
    b.append(poly([tl, tr, C(Xc + 0.27, 0.16, z), C(Xc - 0.27, 0.16, z)], shade(c, 0.18)))
    for dx in (-0.1, 0.07):
        b.append(poly(quad(Xc + dx, Xc + dx + 0.03, 0.0, 0.1, z), "#8e949c"))
    hr = [C(Xc - 0.15, -0.24, z), C(Xc + 0.15, -0.24, z), C(Xc + 0.19, -0.15, z), C(Xc + 0.17, 0.02, z),
          C(Xc - 0.17, 0.02, z), C(Xc - 0.19, -0.15, z)]
    b.append(poly(hr, shade(c, -0.02)))
    b.append(poly([hr[0], hr[1], hr[2], hr[5]], shade(c, 0.14)))
    b.append(poly([hr[5], C(Xc, -0.15, z), hr[4]], shade(c, 0.05)))


def car():
    rnd = seeded(9)
    trim, trim_d, trim_l = "#3b3e46", "#30333a", "#4a4e57"
    b = [rect(0, 0, W, H, "#26282e")]
    # tailgate: the rear window, the trim round it
    b.append(poly(quad(-1, 1, ROOF, FLOOR, TAIL), trim_d))
    rear_glass = quad(-0.82, 0.82, -0.52, WAIST - 0.02, TAIL)
    b += outside("rearwin", rear_glass, rnd, C(0, -0.12, TAIL)[1])
    for i in range(5):   # demister lines
        y = C(0, -0.44 + i * 0.09, TAIL)[1]
        b.append(f'<path d="M{C(-0.74, 0, TAIL)[0]:.0f} {y:.0f} H{C(0.74, 0, TAIL)[0]:.0f}" stroke="#b5574a" stroke-width="1" opacity="0.45"/>')
    # side walls: two windows a side (rear door glass, then the estate's quarter glass)
    for side in (-1, 1):
        b.append(poly(wallp(side, ROOF, FLOOR, 0.3, TAIL), trim))
        b.append(poly(wallp(side, WAIST, FLOOR, 0.3, TAIL), trim_d))
        for k, (z0, z1) in enumerate(((0.95, 1.65), (1.8, 2.55))):
            g = wallp(side, ROOF + 0.07, WAIST, z0, z1)
            b += outside(f"side{side}{k}", g, rnd, C(side, -0.15, (z0 + z1) / 2)[1])
            b.append(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in g)}" fill="none" stroke="#1b1c20" stroke-width="4"/>')
        for z0, z1 in ((0.3, 0.95), (1.65, 1.8), (2.55, TAIL)):
            b.append(poly(wallp(side, ROOF, WAIST, z0, z1), trim_l))
        b.append(poly(wallp(side, WAIST, WAIST + 0.06, 0.3, TAIL), "#1f2126"))   # window sill
        b.append(poly(wallp(side, 0.18, 0.24, 1.15, 1.35), "#8e949c"))   # door handle
    # roof lining with a courtesy light
    rz = [0.3, 0.55, 0.85, 1.3, 1.9, TAIL]
    for i in range(len(rz) - 1):
        for j, (xa, xb) in enumerate(((-1, -0.3), (-0.3, 0.3), (0.3, 1))):
            c = shade("#a9a69f", rnd.uniform(-0.08, 0.06) + (0.04 if j == 1 else -0.03))
            b.append(poly([C(xa, ROOF, rz[i]), C(xb, ROOF, rz[i]), C(xb, ROOF, rz[i + 1])], c))
            b.append(poly([C(xa, ROOF, rz[i]), C(xb, ROOF, rz[i + 1]), C(xa, ROOF, rz[i + 1])], shade(c, -0.04)))
    b.append(poly([C(-0.12, ROOF, 1.3), C(0.12, ROOF, 1.3), C(0.12, ROOF, 1.55), C(-0.12, ROOF, 1.55)], "#e8e4da"))
    b.append(poly([C(-0.08, ROOF, 1.34), C(0.08, ROOF, 1.34), C(0.08, ROOF, 1.51), C(-0.08, ROOF, 1.51)], "#fff5d6"))
    # the boot: crates of records stacked against the tailgate, over the bottom of the rear glass
    for X0, z in ((-0.8, 2.55), (-0.36, 2.6), (0.04, 2.6), (0.44, 2.55), (-0.62, 2.35), (0.3, 2.38)):
        top = -0.26 if z > 2.45 else -0.17
        f = quad(X0, X0 + 0.38, top, 0.3, z)
        b.append(poly(f, "#8b6a45"))
        b.append(poly([f[0], f[1], f[3]], "#7d5e3c"))
        b.append(poly(quad(X0, X0 + 0.38, top, top + 0.025, z), "#a3825a"))
        (x0, y0), (x1, _) = f[0], f[1]
        b += spines(x0 + 2, y0 - 18, x1 - 2, y0 + 1, rnd, RECORD_COLORS, lean=False)
        hx, hy = C(X0 + 0.19, top + 0.12, z)
        b.append(rect(hx - 9, hy - 3, 18, 6, "#5b4329"))
    # rear seat backs, headrests folded
    RZ = 2.05
    b.append(poly(quad(-1, 1, 0.0, FLOOR, RZ), "#34363e"))
    for X0, X1 in ((-1, -0.34), (-0.34, 0.34), (0.34, 1)):
        c = shade("#3a3c44", rnd.uniform(-0.04, 0.04))
        b.append(poly(quad(X0 + 0.03, X1 - 0.03, 0.02, 0.6, RZ), c))
        b.append(poly(quad(X0 + 0.03, X1 - 0.03, 0.02, 0.07, RZ), shade(c, 0.15)))
        b.append(poly([C(X0 + 0.03, 0.07, RZ), C(X0 + 0.15, 0.07, RZ), C(X0 + 0.15, 0.6, RZ), C(X0 + 0.03, 0.6, RZ)], shade(c, 0.07)))
    # centre console and handbrake between the front seats
    b.append(poly([C(-0.12, 0.55, 1.6), C(0.12, 0.55, 1.6), C(0.12, 0.55, 0.7), C(-0.12, 0.55, 0.7)], "#2b2d33"))
    b.append(poly([C(-0.12, 0.55, 0.7), C(0.12, 0.55, 0.7), C(0.12, FLOOR, 0.7), C(-0.12, FLOOR, 0.7)], "#202227"))
    b.append(poly([C(-0.03, 0.55, 1.1), C(0.03, 0.55, 1.1), C(0.03, 0.42, 0.95), C(-0.03, 0.42, 0.95)], "#15161a"))
    # the empty passenger seat (screen right), then James's driver's seat behind him (screen left)
    seat(PASSENGER_X, 1.5, "#2a2c33", b)
    seat(DRIVER_X, 1.3, "#26282e", b)
    # B-pillar seat belt on the driver's side, hanging from the pillar
    a, c2 = C(-0.97, -0.4, 1.5), C(-0.97, 0.6, 1.5)
    b.append(f'<path d="M{a[0]:.0f} {a[1]:.0f} L{c2[0]:.0f} {c2[1]:.0f}" stroke="#1a1b1f" stroke-width="12"/>')
    write("car", {"backdrop.svg": svg(W, H, b, "Estate car from the dash mount, portrait, right-hand drive: the driver's seat on screen-left, the empty passenger seat on screen-right, crates of vinyl in the boot. Made by art/make_vlog.py.")})


# ------------------------------------------------------------------ high street (static)
# Seen from the near pavement: the road, the far pavement, and the shops across the road.
# James stands in front of it; passers-by walk the far pavement (feet at FAR_KERB) and cars
# pass on the road (far lane bottom FAR_LANE driving right, near lane NEAR_LANE driving left).
FASCIA, SHOP_BASE, FAR_KERB, NEAR_KERB = 400, 690, 712, 900
FAR_LANE, NEAR_LANE = 790, 872


def high_street():
    rnd = seeded(13)
    b = []
    b += faceted(0, 0, W, 90, 6, 2, rnd, lambda cx, cy: shade(mix("#86b4d3", "#d7e4e6", cy / 90), rnd.uniform(-0.03, 0.04)))
    b += faceted(0, 80, W, FASCIA, 8, 4, rnd, lambda cx, cy: shade("#9b5a44", rnd.uniform(-0.07, 0.06)), jitter=0.3)
    b.append(rect(0, 74, W, 12, "#4c4f57"))
    shops = [
        ("PEMBERTON & GALL", "SOLICITORS · EST. 1962", "#1f4d3a", "#d8b45a", "#f3ead2"),
        ("FONE DOCTOR", "UNLOCKING · REPAIRS", "#1f5fa8", "#ffffff", "#d6ecff"),
        ("SPIN CYCLE", "RECORDS · BOUGHT & SOLD", "#e07a2f", "#1d2b36", "#fff2dc"),
    ]
    sw = 240
    for i, (name, sub, main, ink, glass) in enumerate(shops):
        x0 = i * sw + 4
        x1 = x0 + sw - 8
        for wx in (x0 + 26, x0 + 136):   # sash windows upstairs
            for wy in (120, 260):
                b.append(rect(wx, wy, 70, 100, "#efe8da"))
                b.append(rect(wx + 5, wy + 5, 60, 42, "#7ea6c0"))
                b.append(rect(wx + 5, wy + 53, 60, 42, "#8fb5cc"))
                b.append(poly([(wx + 5, wy + 5), (wx + 40, wy + 5), (wx + 5, wy + 38)], "#a5c6d9"))
                b.append(rect(wx - 5, wy + 100, 80, 8, "#d9d0bf"))
        b.append(rect(x0, FASCIA, x1 - x0, 56, main))
        b.append(rect(x0, FASCIA, x1 - x0, 5, shade(main, -0.3)))
        b.append(text((x0 + x1) / 2, FASCIA + 32, name, 19 if len(name) > 12 else 24, ink,
                      family="Georgia, 'Times New Roman', serif" if i == 0 else "Arial Black, Arial, sans-serif"))
        b.append(text((x0 + x1) / 2, FASCIA + 49, sub, 10, ink, weight="700", family="Arial, Helvetica, sans-serif"))
        top = FASCIA + 56
        b.append(rect(x0, top, x1 - x0, SHOP_BASE - top, shade(main, -0.15)))
        b.append(rect(x0 + 12, top + 14, 150, SHOP_BASE - top - 34, shade(glass, -0.15)))
        b.append(poly([(x0 + 12, top + 14), (x0 + 90, top + 14), (x0 + 12, top + 120)], shade(glass, 0.15), ' opacity="0.8"'))
        b.append(rect(x0 + 176, top + 14, 46, SHOP_BASE - top - 14, shade(main, -0.35)))
        b.append(rect(x0 + 212, top + 100, 5, 14, "#d8b45a"))
        gx, gy = x0 + 12, top + 14
        if i == 0:   # files and a brass plaque
            for k in range(5):
                b.append(rect(gx + 14 + k * 20, gy + 120 - k * 5, 16, 50 + k * 5, ["#c7b48a", "#a8936a", "#d9c9a0"][k % 3]))
            b.append(rect(x0 + 178, top + 30, 42, 30, "#d8b45a"))
            b.append(text(x0 + 199, top + 50, "P&G", 11, "#1f4d3a", family="Georgia, serif"))
        elif i == 1:  # phones and a card
            for k in range(4):
                b.append(rect(gx + 14 + k * 32, gy + 40, 22, 42, "#1b1b1f"))
                b.append(rect(gx + 17 + k * 32, gy + 43, 16, 34, "#4aa3ff"))
            b.append(rect(gx + 10, gy + 110, 130, 32, "#ffffff"))
            b.append(text(gx + 75, gy + 131, "WE UNLOCK ANY PHONE*", 10, "#c0392b", family="Arial Black, Arial, sans-serif"))
        else:         # records in the window
            for k in range(3):
                b += gem(gx + 30 + k * 46, gy + 50 + (k % 2) * 34, 20, ["#141418", "#26262c"], n=8)
                b.append(rect(gx + 24 + k * 46, gy + 44 + (k % 2) * 34, 12, 12, RECORD_COLORS[k * 3]))
            b += spines(gx + 8, gy + 128, gx + 142, gy + 176, rnd, RECORD_COLORS, lean=False)
        b.append(rect(x0 - 4, FASCIA, 4, SHOP_BASE - FASCIA, "#d9d0bf"))
    # far pavement, kerb, road, near kerb, near pavement
    b.append(rect(0, SHOP_BASE, W, FAR_KERB - SHOP_BASE, "#a9a49c"))
    b.append(rect(0, FAR_KERB, W, 8, "#d9d4ca"))
    b.append(rect(0, FAR_KERB + 8, W, NEAR_KERB - FAR_KERB - 8, "#55565e"))
    b.append(poly([(0, FAR_KERB + 8), (W, FAR_KERB + 8), (W, FAR_KERB + 40), (0, FAR_KERB + 60)], "#5d5f67"))
    for k in range(0, W, 120):   # centre line dashes
        b.append(rect(k + 20, 828, 70, 7, "#e8e2c8"))
    b.append(rect(0, NEAR_KERB, W, 12, "#d9d4ca"))
    b.append(rect(0, NEAR_KERB + 12, W, H - NEAR_KERB - 12, "#aca79f"))
    for k in range(0, W, 180):
        b.append(f'<path d="M{k} {NEAR_KERB + 12} L{k - 90} {H}" stroke="#958f86" stroke-width="2"/>')
    for y in (1000, 1130):
        b.append(f'<path d="M0 {y} H{W}" stroke="#958f86" stroke-width="2"/>')
    write("high_street", {"backdrop.svg": svg(W, H, b, "High street, portrait: the shops across the road from the near pavement. Made by art/make_vlog.py.")})


def black():
    write("black", {"backdrop.svg": svg(W, H, [rect(0, 0, W, H, "#000000")], "Black, for the blackout before the end card.")})


# ------------------------------------------------------------------ passing cars (set pieces)
def side_car(body, dark, kind):
    """A car side-on, facing right, wheels on the bottom edge (520 x 200)."""
    if kind == "van":
        out = [poly([(10, 170), (10, 30), (330, 20), (360, 30), (440, 90), (505, 110), (512, 170)], body),
               poly([(10, 120), (512, 120), (512, 170), (10, 170)], dark),
               poly([(350, 36), (430, 94), (350, 94)], "#7fa6bd"), poly([(350, 36), (380, 58), (350, 94)], "#9cc0d4")]
    else:
        roof = 150 if kind == "estate" else 210
        out = [poly([(12, 170), (14, 100), (60, 92), (120, 40), (330, 36), (400, 92), (500, 108), (510, 170)], body),
               poly([(12, 130), (510, 130), (510, 170), (12, 170)], dark),
               poly([(70, 92), (126, 48), (roof + 70, 46), (roof + 70, 92)], "#7fa6bd"),
               poly([(roof + 82, 46), (322, 46), (386, 92), (roof + 82, 92)], "#9cc0d4"),
               rect(roof + 70, 44, 12, 50, dark)]
    out += [rect(490, 112, 20, 12, "#f6c453"), rect(10, 112, 14, 12, "#c0392b")]
    for cx in (110, 410):
        out += gem(cx, 168, 32, ["#17171b", "#222227"], n=8)
        out += gem(cx, 168, 13, ["#9aa0a8", "#7d838b"], n=6)
    return out


def cars():
    sets = SHOW / "sets"
    for name, body, dark, kind in (("hatch_red", "#c0392b", "#a93226", "hatch"), ("estate_blue", "#2f6fa8", "#285f91", "estate"),
                                   ("van_white", "#ecebe6", "#c9c7c0", "van")):
        art = side_car(body, dark, kind)
        right = svg(520, 200, art, f"{name}, side-on, driving right. Made by art/make_vlog.py.")
        left = svg(520, 200, ['<g transform="translate(520 0) scale(-1 1)">'] + art + ["</g>"],
                   f"{name}, side-on, driving left. Made by art/make_vlog.py.")
        write(f"{name}_r", {"piece.svg": right, "piece.json": "{}\n"}, sets)
        write(f"{name}_l", {"piece.svg": left, "piece.json": "{}\n"}, sets)


def main():
    street()
    lounge()
    car()
    high_street()
    black()
    cars()
    print("wrote street, lounge, car, high_street, black and the passing cars")


if __name__ == "__main__":
    main()
