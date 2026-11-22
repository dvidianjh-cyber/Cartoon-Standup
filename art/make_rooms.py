"""Draw the locations for ep02 and ep03 in the faceted low-poly style, portrait
(720x1280, as if filmed on a phone; series.yaml `format: portrait`). Same rules
as art/make_vlog.py: James's eyes sit at about y 520 with his head across
x 225-495 and his shoulders filling the bottom, so the detail is at the sides and top.

Usage: python3 art/make_rooms.py   (from the series repo's top folder)

  show/backdrops/bath/             tiled bathroom, frosted window, candles and a rubber duck (static)
  show/backdrops/corridor/         office corridor, walking towards the camera (depth, zoom-looped)
  show/backdrops/office/           behind James's desk: city window, pinboard, clock at half four (static)
  show/backdrops/kitchen/          green cupboards, metro tiles, the red kettle steaming (static)
  show/backdrops/gaming_den/       night: LED strip, poster, the red gaming chair behind him (static)
  show/backdrops/home_street/      outside James's house, number 27, from the road (static)
  show/backdrops/industrial_road/  the grey road out to the impound lot (depth, zoom-looped)
  show/backdrops/impound_hatch/    the impound lot's portakabin and its payment hatch (static)
  show/sets/bath_tub/              foam and the near rim of the bath (front)
  show/sets/monitor/               James's work screen (writable: `writing:` rows are the email)
  show/sets/game_screen/           the gaming monitor with the factory game on it (back)
  show/sets/desk_edge/             the desk's edge with keyboard and coffee cup (front)
  show/sets/old_estate/            James's old estate car side-on, facing right, bin bag on the
                                   front window and silver fingerprint powder on the doors (back)
  show/sets/broken_glass/          window glass on the road where the car was (back)
  show/sets/hatch_counter/         the sill under the impound hatch with the card machine (front)
"""
import json
import math
from pathlib import Path

from lowpoly import (RECORD_COLORS, faceted, gem, mix, poly, rect, seeded, shade, svg, text)

SHOW = Path(__file__).resolve().parent.parent / "show"
W, H = 720, 1280


def write(kind, name, files):
    d = SHOW / kind / name
    d.mkdir(parents=True, exist_ok=True)
    for fn, content in files.items():
        (d / fn).write_text(content, encoding="utf-8")


def line(x0, y0, x1, y1, col, w, extra=""):
    return f'<path d="M{x0:.1f} {y0:.1f} L{x1:.1f} {y1:.1f}" stroke="{col}" stroke-width="{w}"{extra}/>'


def tiles(x0, y0, x1, y1, tw, th, base, rnd, grout="#c9d3d6", offset=True, spread=0.05):
    """A wall of rectangular tiles, each split into two facets."""
    out = [rect(x0, y0, x1 - x0, y1 - y0, grout)]
    r = 0
    y = y0
    while y < y1:
        x = x0 - (tw / 2 if offset and r % 2 else 0)
        while x < x1:
            c = shade(base, rnd.uniform(-spread, spread))
            a, b = max(x, x0) + 2, min(x + tw, x1) - 2
            yb = min(y + th, y1) - 2
            if b > a and yb > y + 2:
                out.append(poly([(a, y + 2), (b, y + 2), (b, yb), (a, yb)], c))
                out.append(poly([(a, y + 2), (b, y + 2), (a, yb)], shade(c, 0.06)))
            x += tw
        y += th
        r += 1
    return out


# ------------------------------------------------------------------ depth helpers (corridor, road)
VX, VY, S = 360, 470, 0.8


def P(X, Y, z):
    return VX + S * X / z, VY + S * Y / z


def depth_json(zoom, sprites=()):
    return json.dumps({"vanish": [VX, VY], "zoom": round(zoom, 4), "sync": True, "sprites": list(sprites)}, indent=2) + "\n"


# ------------------------------------------------------------------ bath
def bath():
    rnd = seeded(21)
    b = tiles(0, 0, W, H, 90, 60, "#dfeeee", rnd, grout="#b9cdd0")
    # frosted window, top left
    wx0, wy0, wx1, wy1 = 30, 70, 230, 330
    b.append(rect(wx0 - 12, wy0 - 12, wx1 - wx0 + 24, wy1 - wy0 + 24, "#f4f4f0"))
    b += faceted(wx0, wy0, wx1, wy1, 3, 4, rnd, lambda cx, cy: shade(mix("#cfe3ea", "#f3f1e6", (cy - wy0) / (wy1 - wy0)), rnd.uniform(-0.06, 0.06)))
    b.append(rect(wx0 + (wx1 - wx0) / 2 - 5, wy0, 10, wy1 - wy0, "#f4f4f0"))
    b.append(rect(wx0 - 18, wy1 + 12, wx1 - wx0 + 36, 14, "#e2e2dc"))
    # towel rail with a striped towel, left
    b.append(rect(20, 520, 200, 10, "#b8bec4"))
    for i, c in enumerate(("#3c8de8", "#f4f1de", "#3c8de8", "#f4f1de", "#3c8de8")):
        b.append(poly([(40 + i * 32, 528), (72 + i * 32, 528), (70 + i * 32, 840), (38 + i * 32, 846)], c))
    b.append(poly([(40, 528), (200, 528), (198, 560), (40, 566)], "#2f6fb8"))
    b.append(poly([(38, 846), (198, 838), (198, 860), (38, 868)], "#2f6fb8"))
    # glass shelf, right, with candles, a rubber duck and a shampoo bottle
    b.append(rect(500, 560, 210, 10, "#cfe6ea"))
    b.append(rect(500, 570, 210, 4, "#9fb9be"))
    for cx, h in ((530, 70), (575, 46)):
        b.append(rect(cx - 15, 560 - h, 30, h, "#f6efdc"))
        b.append(poly([(cx - 15, 560 - h), (cx, 560 - h), (cx, 560), (cx - 15, 560)], "#ebe1c8"))
        b.append(poly([(cx, 560 - h - 24), (cx + 7, 560 - h - 8), (cx, 560 - h - 2), (cx - 7, 560 - h - 8)], "#ffb347"))
        b.append(poly([(cx, 560 - h - 16), (cx + 3, 560 - h - 8), (cx, 560 - h - 4), (cx - 3, 560 - h - 8)], "#fff1a8"))
        b.append(f'<circle cx="{cx}" cy="{560 - h - 10}" r="34" fill="#ffd27a" opacity="0.18"/>')
    # duck
    b.append(poly([(610, 560), (680, 560), (690, 530), (672, 512), (630, 516), (608, 534)], "#f7c843"))
    b.append(poly([(610, 560), (650, 560), (630, 516), (608, 534)], "#e9b62e"))
    b += gem(632, 496, 22, ["#f7c843", "#efbd36", "#fbd65a"], n=7)
    b.append(poly([(610, 496), (594, 502), (612, 506)], "#e8743b"))
    b.append(rect(624, 490, 5, 5, "#1b1b1b"))
    # shampoo bottle
    b.append(poly([(684, 560), (708, 560), (706, 490), (686, 490)], "#7d5ba6"))
    b.append(rect(690, 476, 12, 16, "#f4f1de"))
    # the far end of the tub behind him, and a tap
    b.append(poly([(0, 930), (W, 930), (W, H), (0, H)], "#f7f8f6"))
    b.append(poly([(0, 930), (W, 930), (W, 960), (0, 966)], "#ffffff"))
    b.append(poly([(0, 966), (W, 960), (W, 1010), (0, 1020)], "#e3e8e6"))
    b.append(poly([(590, 880), (640, 880), (640, 930), (590, 930)], "#c4cbd1"))
    b.append(poly([(600, 870), (680, 870), (690, 890), (600, 894)], "#dde2e6"))
    b.append(poly([(670, 890), (690, 890), (686, 910), (672, 910)], "#aeb5bb"))
    # bubbles riding high on the water behind him
    for cx, cy, r in ((60, 1000, 60), (150, 990, 48), (560, 1000, 52), (660, 990, 62), (720, 1010, 40)):
        b += gem(cx, cy, r, ["#ffffff", "#eef4f6", "#f7fbfc", "#e4edf0"], n=9, squash=0.6)
    write("backdrops", "bath", {"backdrop.svg": svg(W, H, b, "Bathroom, portrait: tiles, frosted window top left, towel left, shelf with candles and a rubber duck right, the far end of the tub behind him. Made by art/make_rooms.py.")})

    # foam and the near rim across the bottom of the frame
    rnd = seeded(22)
    f = []
    for i in range(16):
        cx = -20 + i * 50 + rnd.uniform(-10, 10)
        r = rnd.uniform(48, 74)
        f += gem(cx, 110 + rnd.uniform(-14, 14), r, ["#ffffff", "#f0f6f8", "#e2ecef", "#f8fbfc"], n=9, squash=0.55, rot=rnd.uniform(0, 1))
    f += faceted(-20, 108, W + 20, 250, 10, 3, rnd, lambda cx, cy: shade("#eef5f7", rnd.uniform(-0.05, 0.04)))
    f.append(poly([(-20, 246), (W + 20, 246), (W + 20, 300), (-20, 300)], "#ffffff"))
    f.append(poly([(-20, 246), (W + 20, 246), (W + 20, 258), (-20, 258)], "#dfe5e3"))
    write("sets", "bath_tub", {"piece.svg": svg(W, 300, f, "Foam and the near rim of the bath, across the bottom of the frame. Anchor: bottom centre. Made by art/make_rooms.py."),
                               "piece.json": json.dumps({"layer": "front"}) + "\n"})


# ------------------------------------------------------------------ office corridor (depth)
COR_RATIO, COR_REPEAT = 1.28, 3
COR_ZOOM = COR_RATIO ** COR_REPEAT


def corridor():
    zs = [0.25 * COR_RATIO ** k for k in range(30)]
    WALL, CEIL, FLOOR = 520, -380, 420
    b = [rect(-10, -10, W + 20, H + 20, "#cfc8b6")]
    # ceiling, walls and carpet as long faces down the corridor
    zn, zf = 0.2, 300
    b.append(poly([P(-WALL, CEIL, zn), P(WALL, CEIL, zn), P(WALL, CEIL, zf), P(-WALL, CEIL, zf)], "#e9e6dc"))
    b.append(poly([P(-WALL, FLOOR, zn), P(WALL, FLOOR, zn), P(WALL, FLOOR, zf), P(-WALL, FLOOR, zf)], "#5b6b80"))
    b.append(poly([P(-170, FLOOR, zn), P(170, FLOOR, zn), P(170, FLOOR, zf), P(-170, FLOOR, zf)], "#647690"))
    for side in (-1, 1):
        X = WALL * side
        b.append(poly([P(X, CEIL, zn), P(X, CEIL, zf), P(X, FLOOR, zf), P(X, FLOOR, zn)], "#e6dcc4" if side < 0 else "#ddd2b9"))
        b.append(poly([P(X, CEIL, zn), P(X, CEIL, zf), P(X, CEIL + 50, zf), P(X, CEIL + 50, zn)], "#f1ece0"))
        b.append(poly([P(X, FLOOR - 40, zn), P(X, FLOOR - 40, zf), P(X, FLOOR, zf), P(X, FLOOR, zn)], "#7a6f63"))
    # repeating bays: a ceiling light, and on the walls doors and noticeboards
    for i in range(len(zs) - 1):
        za, zb = zs[i], zs[i + 1]
        zm = lambda f: za + (zb - za) * f
        k = i % COR_REPEAT
        b.append(poly([P(-120, CEIL, zm(0.3)), P(120, CEIL, zm(0.3)), P(120, CEIL, zm(0.55)), P(-120, CEIL, zm(0.55))], "#fffbe8"))
        b.append(poly([P(-120, CEIL, zm(0.3)), P(0, CEIL, zm(0.3)), P(-120, CEIL, zm(0.55))], "#fff4c8"))
        for side in (-1, 1):
            X = WALL * side
            if (k + (side > 0)) % 3 != 2:   # a door
                col = ["#7a8fa8", "#9c6b4a", "#5f8f7a"][(k + (side > 0)) % 3]
                b.append(poly([P(X, -140, zm(0.25)), P(X, -140, zm(0.6)), P(X, FLOOR, zm(0.6)), P(X, FLOOR, zm(0.25))], "#f4f0e6"))
                b.append(poly([P(X, -120, zm(0.29)), P(X, -120, zm(0.56)), P(X, FLOOR, zm(0.56)), P(X, FLOOR, zm(0.29))], col))
                b.append(poly([P(X, -90, zm(0.33)), P(X, -90, zm(0.52)), P(X, 40, zm(0.52)), P(X, 40, zm(0.33))], "#bcd6e4"))
                b.append(poly([P(X, 140, zm(0.49)), P(X, 140, zm(0.53)), P(X, 160, zm(0.53)), P(X, 160, zm(0.49))], "#d8b45a"))
            else:                            # a noticeboard with posters
                b.append(poly([P(X, -200, zm(0.2)), P(X, -200, zm(0.7)), P(X, 30, zm(0.7)), P(X, 30, zm(0.2))], "#b8895a"))
                for f0, f1, y0, y1, c in ((0.25, 0.42, -180, -40, "#f2b134"), (0.46, 0.66, -170, 10, "#3c8de8"), (0.3, 0.44, -20, 20, "#f4f1de")):
                    b.append(poly([P(X, y0, zm(f0)), P(X, y0, zm(f1)), P(X, y1, zm(f1)), P(X, y1, zm(f0))], c))
    write("backdrops", "corridor", {
        "backdrop.svg": svg(W, H, b, "Office corridor, portrait, vanishing at (360, 470): drawn self-similar so it zoom-loops (backdrop.json zoom). Made by art/make_rooms.py."),
        "backdrop.json": depth_json(COR_ZOOM)})


# ------------------------------------------------------------------ office
def office():
    rnd = seeded(31)
    b = faceted(0, 0, W, H, 8, 14, rnd, lambda cx, cy: shade("#c7cfd6", rnd.uniform(-0.05, 0.05) - cy / 9000))
    # city window, top, behind his head
    wx0, wy0, wx1, wy1 = 150, 60, 570, 420
    b.append(rect(wx0 - 14, wy0 - 14, wx1 - wx0 + 28, wy1 - wy0 + 28, "#8e98a3"))
    b += faceted(wx0, wy0, wx1, wy1, 5, 4, rnd, lambda cx, cy: shade(mix("#8fbad6", "#e7eef0", (cy - wy0) / (wy1 - wy0)), rnd.uniform(-0.03, 0.04)))
    x = wx0
    while x < wx1:   # city skyline
        w = rnd.uniform(36, 70)
        top = wy1 - rnd.uniform(90, 250)
        c = rnd.choice(["#6d7f92", "#7d8fa1", "#5d6f82", "#8c9aa8"])
        b.append(rect(x, top, min(w, wx1 - x), wy1 - top, c))
        b.append(rect(x, top, min(w, wx1 - x) * 0.35, wy1 - top, shade(c, -0.1)))
        for wy in range(int(top) + 12, wy1 - 10, 22):
            for wx in range(int(x) + 8, int(min(x + w, wx1)) - 8, 14):
                if rnd.random() < 0.55:
                    b.append(rect(wx, wy, 6, 9, "#dfe9f1"))
        x += w + 4
    for mx in (wx0 + (wx1 - wx0) / 3, wx0 + 2 * (wx1 - wx0) / 3):
        b.append(rect(mx - 5, wy0, 10, wy1 - wy0, "#8e98a3"))
    # blind pulled half way
    b.append(rect(wx0, wy0, wx1 - wx0, 70, "#e8e3d6"))
    for y in range(wy0 + 8, wy0 + 70, 10):
        b.append(line(wx0, y, wx1, y, "#cfc8b8", 2))
    # clock, top right: half past four
    cx, cy = 640, 150
    b += gem(cx, cy, 52, ["#2b2d33"], n=12)
    b += gem(cx, cy, 44, ["#fbfaf5", "#f1efe6"], n=12)
    for i in range(12):
        a = i * math.pi / 6
        b.append(line(cx + 36 * math.sin(a), cy - 36 * math.cos(a), cx + 41 * math.sin(a), cy - 41 * math.cos(a), "#2b2d33", 3))
    hr = math.radians(4.5 * 30)
    b.append(line(cx, cy, cx + 22 * math.sin(hr), cy - 22 * math.cos(hr), "#1b1b1b", 6, ' stroke-linecap="round"'))
    b.append(line(cx, cy, cx, cy + 34, "#1b1b1b", 4, ' stroke-linecap="round"'))
    b.append(f'<circle cx="{cx}" cy="{cy}" r="4" fill="#c0392b"/>')
    # pinboard, left
    b.append(rect(10, 470, 190, 230, "#a8764d"))
    b.append(rect(18, 478, 174, 214, "#c79a6a"))
    for (x0, y0, w, h, c) in ((30, 492, 70, 84, "#f7e27a"), (112, 498, 66, 60, "#f4f1de"), (36, 596, 62, 80, "#8fd3c1"), (110, 574, 72, 104, "#f4f1de")):
        b.append(poly([(x0, y0), (x0 + w, y0 + 3), (x0 + w - 2, y0 + h), (x0 - 2, y0 + h - 3)], c))
        b.append(f'<circle cx="{x0 + w / 2:.0f}" cy="{y0 + 8:.0f}" r="4" fill="#c0392b"/>')
        for k in range(3):
            b.append(line(x0 + 8, y0 + 24 + k * 14, x0 + w - 12, y0 + 24 + k * 14, "#8a8a8a", 2))
    # plant, bottom left
    b.append(poly([(40, 860), (120, 860), (110, 940), (50, 940)], "#c96f45"))
    for a, c in ((-0.9, "#3f7a3a"), (-0.4, "#4f8f45"), (0.1, "#5ea050"), (0.6, "#4a8a42"), (1.0, "#3a7035")):
        tip = (80 + 120 * math.sin(a), 860 - 150 * math.cos(a))
        b.append(poly([(80, 860), (tip[0] - 18, (860 + tip[1]) / 2), tip, (tip[0] + 14, (860 + tip[1]) / 2 + 10)], c))
    # the back of the office: a partition along the bottom
    b.append(rect(0, 940, W, H - 940, "#5d6b7a"))
    b.append(rect(0, 940, W, 12, "#7d8b9a"))
    write("backdrops", "office", {"backdrop.svg": svg(W, H, b, "Office behind James's desk, portrait: city window, clock at half past four top right, pinboard and plant left. Made by art/make_rooms.py.")})

    # monitor: writable screen
    m = [rect(0, 0, 300, 210, "#1f2126"), rect(10, 10, 280, 172, "#f7f9fc"), rect(10, 10, 280, 22, "#2e6fd8"),
         f'<circle cx="24" cy="21" r="5" fill="#ffffff" opacity="0.8"/>', rect(36, 17, 70, 8, "#ffffff", ' opacity="0.7"'),
         poly([(0, 0), (300, 0), (300, 8), (0, 8)], "#2b2e35"), poly([(10, 182), (290, 182), (290, 196), (10, 196)], "#16171b"),
         poly([(130, 210), (170, 210), (176, 262), (124, 262)], "#2b2e35"), poly([(130, 210), (150, 210), (150, 262), (124, 262)], "#24262c"),
         poly([(84, 262), (216, 262), (226, 280), (74, 280)], "#1f2126")]
    write("sets", "monitor", {"piece.svg": svg(300, 280, m, "James's work monitor. The screen is writable: `writing:` rows are lines of the email. Anchor: bottom centre. Made by art/make_rooms.py."),
                              "piece.json": json.dumps({"writeArea": [18, 40, 282, 180], "lineHeight": 32, "inkSize": 19, "ink": "#1b1b1b"}) + "\n"})
    # desk edge with keyboard and coffee cup
    rnd = seeded(32)
    d = [rect(0, 60, W, 160, "#b48a5e"), rect(0, 60, W, 14, "#c99e70"), rect(0, 74, W, 8, "#9a7650"),
         poly([(0, 82), (W, 82), (W, 220), (0, 220)], "#a37b52")]
    d.append(poly([(70, 52), (330, 52), (340, 74), (60, 74)], "#2b2e35"))
    for r in range(3):
        for k in range(12):
            d.append(rect(78 + k * 21 + r * 3, 55 + r * 6, 17, 4, "#5a5e68"))
    d.append(poly([(560, -10), (620, -10), (614, 70), (566, 70)], "#f4f1de"))
    d.append(poly([(560, -10), (590, -10), (588, 70), (566, 70)], "#e6e1cc"))
    d.append(poly([(620, 8), (642, 14), (640, 44), (616, 48)], "none", ' stroke="#f4f1de" stroke-width="7"'))
    d.append(rect(562, -10, 56, 8, "#5a3a22"))
    write("sets", "desk_edge", {"piece.svg": svg(W, 240, ['<g transform="translate(0 20)">'] + d + ["</g>"], "The desk's edge across the bottom of the frame, keyboard and a coffee cup. Anchor: bottom centre. Made by art/make_rooms.py."),
                                "piece.json": json.dumps({"layer": "front"}) + "\n"})


# ------------------------------------------------------------------ kitchen
def kitchen():
    rnd = seeded(41)
    b = tiles(0, 0, W, H, 70, 36, "#f3f1ea", rnd, grout="#d8d3c6", spread=0.03)
    # wall cupboards across the top
    for x0 in range(0, W, 180):
        b.append(rect(x0 + 4, 0, 172, 300, "#4f7f68"))
        b.append(rect(x0 + 16, 12, 148, 276, "#5b8f75"))
        b.append(poly([(x0 + 16, 12), (x0 + 164, 12), (x0 + 16, 200)], "#66997e"))
        b.append(rect(x0 + 140, 230, 10, 40, "#d8b45a"))
    b.append(rect(0, 300, W, 12, "#3f6b56"))
    # window over the sink, left
    wx0, wy0, wx1, wy1 = 20, 380, 220, 640
    b.append(rect(wx0 - 12, wy0 - 12, wx1 - wx0 + 24, wy1 - wy0 + 24, "#f4f4f0"))
    b += faceted(wx0, wy0, wx1, wy1, 3, 4, rnd, lambda cx, cy: shade(mix("#8fbad6", "#f3e7c8", (cy - wy0) / (wy1 - wy0)), rnd.uniform(-0.03, 0.04)))
    b.append(poly([(wx0, 560), (60, 540), (110, 556), (160, 530), (wx1, 548), (wx1, wy1), (wx0, wy1)], "#4f7a3f"))
    b.append(rect(wx0 + (wx1 - wx0) / 2 - 4, wy0, 8, wy1 - wy0, "#f4f4f0"))
    b.append(rect(wx0 - 20, wy1 + 12, wx1 - wx0 + 40, 14, "#e2e2dc"))
    # utensil rail with spoons, right
    b.append(rect(520, 420, 190, 8, "#9aa0a8"))
    for k, c in enumerate(("#9aa0a8", "#c0392b", "#9aa0a8", "#3c8de8")):
        x = 545 + k * 42
        b.append(rect(x - 3, 428, 6, 90, c))
        b += gem(x, 528, 13, [c, shade(c, -0.15)], n=6, squash=1.3)
    # worktop across, at shoulder height
    b.append(rect(0, 820, W, 26, "#c7a77a"))
    b.append(rect(0, 846, W, 10, "#a8875c"))
    b.append(rect(0, 856, W, H - 856, "#4f7f68"))
    for x0 in range(0, W, 180):
        b.append(rect(x0 + 10, 870, 160, 400, "#5b8f75"))
        b.append(rect(x0 + 140, 890, 10, 40, "#d8b45a"))
    # the red kettle on the worktop, right, steaming
    kx = 640
    b.append(poly([(kx - 58, 820), (kx + 58, 820), (kx + 48, 720), (kx + 30, 700), (kx - 30, 700), (kx - 48, 720)], "#c0392b"))
    b.append(poly([(kx - 58, 820), (kx, 820), (kx, 700), (kx - 30, 700), (kx - 48, 720)], "#a93226"))
    b.append(poly([(kx - 34, 700), (kx + 34, 700), (kx + 20, 686), (kx - 20, 686)], "#2b2d33"))
    b.append(poly([(kx + 48, 730), (kx + 78, 716), (kx + 72, 780), (kx + 52, 790)], "none", ' stroke="#2b2d33" stroke-width="9"'))
    b.append(poly([(kx - 50, 740), (kx - 86, 714), (kx - 92, 706), (kx - 56, 726)], "#a93226"))
    b.append(rect(kx - 64, 816, 128, 8, "#2b2d33"))
    for k, (dx, dy, r) in enumerate(((-96, 690, 18), (-112, 660, 24), (-98, 622, 28), (-120, 584, 32), (-104, 540, 30))):
        b += [g.replace("/>", f' opacity="{0.75 - k * 0.12:.2f}"/>') for g in gem(kx + dx, dy, r, ["#ffffff", "#eef2f3", "#f7f9fa"], n=7)]
    # a mug and a tea caddy, left of him
    b.append(poly([(90, 820), (140, 820), (136, 770), (94, 770)], "#f2b134"))
    b.append(rect(150, 740, 54, 80, "#2a9d8f"))
    b.append(text(177, 786, "TEA", 14, "#f4f1de"))
    write("backdrops", "kitchen", {"backdrop.svg": svg(W, H, b, "Kitchen, portrait: green cupboards, metro tiles, window left, the red kettle steaming on the worktop right. Made by art/make_rooms.py.")})


# ------------------------------------------------------------------ gaming den
def gaming_den():
    rnd = seeded(51)
    b = faceted(0, 0, W, H, 8, 14, rnd, lambda cx, cy: shade(mix("#262a46", "#3a2f5a", cx / W), rnd.uniform(-0.05, 0.05)))
    # LED strip along the top, its glow on the wall
    b.append(f'<defs><linearGradient id="led" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d14bff" stop-opacity="0.45"/><stop offset="1" stop-color="#d14bff" stop-opacity="0"/></linearGradient></defs>')
    b.append(rect(0, 40, W, 200, "url(#led)"))
    b.append(rect(0, 34, W, 8, "#f1a6ff"))
    # poster, top left: a rocket
    b.append(rect(30, 110, 170, 240, "#14162a"))
    b.append(rect(40, 120, 150, 220, "#1f6e9e"))
    b += faceted(40, 120, 190, 340, 3, 4, rnd, lambda cx, cy: shade("#1d5f8a", rnd.uniform(-0.1, 0.1)))
    b.append(poly([(115, 150), (135, 200), (135, 270), (95, 270), (95, 200)], "#e8e2c8"))
    b.append(poly([(95, 240), (80, 280), (95, 270)], "#e8473c"))
    b.append(poly([(135, 240), (150, 280), (135, 270)], "#e8473c"))
    b.append(poly([(100, 272), (130, 272), (115, 316)], "#f2b134"))
    b.append(text(115, 330, "LAUNCH", 13, "#f4f1de"))
    # shelf with a figurine and boxes, top right
    b.append(rect(510, 250, 200, 10, "#14162a"))
    for x0, w, h, c in ((520, 30, 70, "#e8473c"), (552, 26, 80, "#3c8de8"), (580, 34, 60, "#5fbf4a")):
        b.append(rect(x0, 250 - h, w, h, c))
        b.append(rect(x0, 250 - h, w * 0.3, h, shade(c, -0.2)))
    b += gem(660, 214, 20, ["#f2b134", "#e09a1c"], n=6)
    b.append(rect(650, 230, 20, 20, "#f2b134"))
    # desk top along the bottom
    b.append(rect(0, 1000, W, H - 1000, "#1b1d2c"))
    b.append(rect(0, 1000, W, 14, "#2c2f44"))
    b.append(rect(0, 1014, W, 4, "#d14bff", ' opacity="0.6"'))
    # the red gaming chair behind him: winged back, headrest cushion
    ch = [(150, 1280), (150, 560), (190, 380), (240, 330), (480, 330), (530, 380), (570, 560), (570, 1280)]
    b.append(poly(ch, "#b3262f"))
    b.append(poly([(150, 1280), (150, 560), (190, 380), (240, 330), (360, 330), (360, 1280)], "#9c1f28"))
    b.append(poly([(190, 380), (240, 330), (280, 330), (232, 400), (200, 560), (170, 560)], "#1b1b1f"))
    b.append(poly([(530, 380), (480, 330), (440, 330), (488, 400), (520, 560), (550, 560)], "#1b1b1f"))
    b.append(poly([(270, 360), (450, 360), (440, 420), (280, 420)], "#1b1b1f"))
    b.append(poly([(150, 560), (200, 560), (200, 1280), (150, 1280)], "#1b1b1f"))
    b.append(poly([(520, 560), (570, 560), (570, 1280), (520, 1280)], "#1b1b1f"))
    write("backdrops", "gaming_den", {"backdrop.svg": svg(W, H, b, "Gaming den at night, portrait: purple LED strip, rocket poster, shelf, the red gaming chair behind him. Made by art/make_rooms.py.")})

    # the gaming monitor with a factory-building game: conveyors, machines, crates
    rnd = seeded(52)
    g = [rect(0, 0, 340, 230, "#0f1016"), rect(10, 10, 320, 196, "#2f3b2a")]
    g += faceted(10, 10, 330, 206, 6, 4, rnd, lambda cx, cy: shade("#3f5233", rnd.uniform(-0.08, 0.06)))
    for y in (60, 130):
        g.append(rect(10, y, 320, 16, "#6d6a60"))
        for x in range(14, 326, 16):
            g.append(rect(x, y + 3, 8, 10, "#8c887c"))
    g.append(rect(150, 60, 16, 86, "#6d6a60"))
    for x0, y0, c in ((40, 30, "#d8b45a"), (230, 92, "#c0392b"), (90, 150, "#3c8de8"), (260, 156, "#d8b45a")):
        g.append(rect(x0, y0, 50, 40, shade(c, -0.25)))
        g.append(rect(x0 + 6, y0 + 6, 38, 28, c))
        g.append(poly([(x0 + 6, y0 + 6), (x0 + 44, y0 + 6), (x0 + 6, y0 + 34)], shade(c, 0.2)))
    for x in (60, 110, 200, 290):
        g.append(rect(x, 63, 10, 10, "#e9c46a"))
        g.append(rect(x + 20, 133, 10, 10, "#b9bec5"))
    g.append(rect(250, 16, 74, 20, "#0f1016", ' opacity="0.75"'))
    g.append(text(287, 31, "IRON 0", 12, "#e8473c"))
    g.append(f'<rect x="10" y="10" width="320" height="196" fill="#7fe0ff" opacity="0.08"/>')
    g += [poly([(150, 230), (190, 230), (196, 280), (144, 280)], "#14151c"), poly([(100, 280), (240, 280), (250, 296), (90, 296)], "#0f1016")]
    g.append(f'<ellipse cx="170" cy="118" rx="210" ry="160" fill="#7fe0ff" opacity="0.08"/>')
    write("sets", "game_screen", {"piece.svg": svg(340, 296, g, "The gaming monitor with a factory-building game on it. Anchor: bottom centre. Made by art/make_rooms.py."),
                                  "piece.json": json.dumps({"layer": "back"}) + "\n"})


# ------------------------------------------------------------------ home street
# From the road, looking at James's terraced house. He stands in the road by the kerb; his car
# parks behind him on the right (the old_estate set piece, bottom at about y 1010).
def home_street():
    rnd = seeded(61)
    b = faceted(0, 0, W, 60, 6, 1, rnd, lambda cx, cy: shade("#9cc3dc", rnd.uniform(-0.03, 0.03)))
    b += faceted(0, 40, W, 760, 9, 10, rnd, lambda cx, cy: shade("#a65a43", rnd.uniform(-0.07, 0.06)), jitter=0.3)
    for y in range(70, 760, 26):   # brick courses
        b.append(line(0, y, W, y, "#8e4b37", 1.5, ' opacity="0.45"'))
    b.append(rect(0, 30, W, 18, "#4c5560"))
    # bay window, left: three facets
    bx0, by0, bx1, by1 = 0, 330, 250, 620
    b.append(poly([(bx0, by0 - 30), (bx1, by0 - 30), (bx1 + 10, by0 - 10), (bx0, by0 - 10)], "#efe8da"))
    for (x0, x1, c) in ((0, 60, "#2f4556"), (66, 184, "#34495a"), (190, 250, "#2f4556")):
        b.append(rect(x0, by0, x1 - x0, by1 - by0, "#efe8da"))
        b.append(rect(x0 + 8, by0 + 8, x1 - x0 - 16, by1 - by0 - 16, c))
        b.append(poly([(x0 + 8, by0 + 8), (x0 + (x1 - x0) * 0.6, by0 + 8), (x0 + 8, by0 + 120)], shade(c, 0.15)))
        b.append(rect(x0, by0 + 120, x1 - x0, 8, "#efe8da"))
    b.append(rect(-10, by1, 270, 20, "#d9d0bf"))
    # upstairs sash window, top right
    for wx in (420, 570):
        b.append(rect(wx, 90, 110, 160, "#efe8da"))
        b.append(rect(wx + 8, 98, 94, 66, "#34495a"))
        b.append(rect(wx + 8, 172, 94, 70, "#3a5163"))
        b.append(poly([(wx + 8, 98), (wx + 60, 98), (wx + 8, 150)], "#4d6577"))
        b.append(rect(wx - 6, 250, 122, 10, "#d9d0bf"))
    # the blue front door, number 27, behind his head on the right
    dx0, dx1, dy0 = 470, 620, 380
    b.append(rect(dx0 - 16, dy0 - 60, dx1 - dx0 + 32, 760 - dy0 + 60, "#efe8da"))
    b.append(rect(dx0, dy0 - 46, dx1 - dx0, 36, "#bcd6e4"))
    b.append(rect(dx0, dy0, dx1 - dx0, 760 - dy0, "#1f5fa8"))
    b.append(poly([(dx0, dy0), (dx0 + 60, dy0), (dx0 + 60, 760), (dx0, 760)], "#1b5393"))
    for py in (dy0 + 20, dy0 + 200):
        b.append(rect(dx0 + 16, py, dx1 - dx0 - 32, 150, "#2a6cb8"))
    b.append(rect(dx0 + 40, dy0 + 180, 70, 12, "#d8b45a"))
    b.append(text((dx0 + dx1) / 2, dy0 + 150, "27", 36, "#d8b45a", family="Georgia, 'Times New Roman', serif"))
    b.append(f'<circle cx="{dx0 + 126}" cy="{dy0 + 200}" r="7" fill="#d8b45a"/>')
    # low wall and hedge in front of the house, then the pavement and the kerb
    b.append(rect(0, 700, W, 80, "#9b4f3a"))
    b.append(rect(0, 690, W, 14, "#c9b394"))
    b.append(rect(dx0 - 20, 690, dx1 - dx0 + 40, 90, "#b5a58a"))   # the gap for the path
    hx = 0
    while hx < dx0 - 40:
        b += gem(hx + 30, 680, 40, ["#3f6b3a", "#4f7a3f", "#355c31", "#5f8a4a"], n=7, squash=0.8, rot=rnd.uniform(0, 1))
        hx += 46
    # wheelie bin by the gate
    b.append(poly([(640, 700), (712, 700), (706, 812), (646, 812)], "#2e6b3a"))
    b.append(poly([(634, 686), (718, 686), (718, 704), (634, 704)], "#24552e"))
    b.append(text(676, 760, "27", 18, "#f4f1de"))
    b.append(rect(0, 780, W, 110, "#aca79f"))
    for x in range(0, W, 120):
        b.append(line(x, 780, x - 30, 890, "#958f86", 2))
    b.append(rect(0, 890, W, 16, "#d9d4ca"))
    b.append(rect(0, 906, W, H - 906, "#55565e"))
    b.append(poly([(0, 906), (W, 906), (W, 940), (0, 960)], "#5d5f67"))
    b.append(rect(0, 1180, W, 10, "#e8d36a"))   # a single yellow line
    write("backdrops", "home_street", {"backdrop.svg": svg(W, H, b, "Outside James's house from the road, portrait: red-brick terrace, bay window left, blue door number 27 right, low wall and hedge, wheelie bin, pavement and kerb. Made by art/make_rooms.py.")})

    # glass on the road where the car was
    rnd = seeded(62)
    gl = []
    for _ in range(40):
        cx, cy = rnd.uniform(10, 410), rnd.uniform(20, 70)
        r = rnd.uniform(4, 12)
        a = rnd.uniform(0, 6.28)
        gl.append(poly([(cx + r * math.cos(a), cy + r * 0.4 * math.sin(a)), (cx + r * math.cos(a + 2.2), cy + r * 0.4 * math.sin(a + 2.2)),
                        (cx + r * math.cos(a + 4.1), cy + r * 0.4 * math.sin(a + 4.1))], rnd.choice(["#d6f0f6", "#bfe3ee", "#ffffff", "#a9d6e4"])))
    write("sets", "broken_glass", {"piece.svg": svg(420, 80, gl, "Window glass glittering on the road where the car was. Anchor: bottom centre. Made by art/make_rooms.py."),
                                   "piece.json": json.dumps({"layer": "back"}) + "\n"})


def old_estate():
    """James's old estate, side-on, facing right (580 x 230): faded blue, a bin bag taped over the
    front window, silver fingerprint powder smeared on the doors."""
    body, dark = "#5f7f9a", "#4d6a83"
    o = [poly([(14, 190), (16, 110), (40, 100), (90, 44), (420, 40), (470, 100), (560, 116), (570, 190)], body),
         poly([(14, 146), (570, 146), (570, 190), (14, 190)], dark),
         poly([(40, 100), (94, 52), (220, 50), (220, 100)], "#7fa6bd"), poly([(232, 50), (330, 50), (330, 100), (232, 100)], "#9cc0d4"),
         rect(220, 48, 12, 54, dark), rect(330, 48, 12, 54, dark)]
    # the front window: a black bin bag and parcel tape
    o.append(poly([(342, 50), (412, 50), (458, 100), (342, 100)], "#1b1c20"))
    o.append(poly([(352, 58), (400, 56), (380, 84), (350, 92)], "#2c2e34"))
    o.append(poly([(410, 54), (446, 92), (420, 96)], "#25272c"))
    for x0, y0, x1, y1 in ((336, 64, 420, 58), (336, 94, 462, 90), (380, 46, 372, 104)):
        o.append(line(x0, y0, x1, y1, "#c9a86a", 7, ' opacity="0.9"'))
    # dents, rust and the silver fingerprint powder on the doors
    o.append(poly([(480, 120), (520, 118), (510, 136), (486, 134)], "#4d6a83"))
    o.append(poly([(30, 150), (62, 148), (58, 166), (34, 168)], "#8b5a3c"))
    rnd = seeded(63)
    for _ in range(60):
        cx, cy = rnd.uniform(110, 470), rnd.uniform(104, 150)
        r = rnd.uniform(3, 9)
        o.append(f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{r:.1f}" ry="{r * 0.7:.1f}" fill="#d7dbe0" opacity="{rnd.uniform(0.35, 0.8):.2f}"/>')
    for x0, y0 in ((160, 112), (300, 118), (400, 126)):
        o.append(poly([(x0, y0), (x0 + 50, y0 - 4), (x0 + 58, y0 + 20), (x0 + 4, y0 + 26)], "#c4c9cf", ' opacity="0.55"'))
    o += [line(220, 104, 220, 186, "#3d556b", 3), line(340, 104, 344, 186, "#3d556b", 3), rect(258, 112, 28, 6, "#c4c9cf"), rect(380, 112, 28, 6, "#c4c9cf")]
    o += [rect(552, 120, 20, 14, "#f6c453"), rect(10, 118, 14, 14, "#c0392b")]
    for cx in (120, 460):
        o += gem(cx, 190, 36, ["#17171b", "#222227"], n=8)
        o += gem(cx, 190, 15, ["#9aa0a8", "#7d838b"], n=6)
    write("sets", "old_estate", {"piece.svg": svg(580, 230, o, "James's old estate side-on, facing right: bin bag taped over the front window, silver fingerprint powder on the doors. Wheels on the bottom edge. Made by art/make_rooms.py."),
                                 "piece.json": json.dumps({"layer": "back"}) + "\n"})


# ------------------------------------------------------------------ industrial road (depth)
IND_RATIO, IND_REPEAT = 1.3, 3
IND_ZOOM = IND_RATIO ** IND_REPEAT


def industrial_road():
    zs = [0.2 * IND_RATIO ** k for k in range(28)]
    GROUND, FENCE, SHED = 420, -720, 760
    b = ['<defs><linearGradient id="grey" gradientUnits="userSpaceOnUse" x1="0" y1="-200" x2="0" y2="470">'
         '<stop offset="0" stop-color="#a9b2ba"/><stop offset="1" stop-color="#d9dcd8"/></linearGradient></defs>',
         rect(-10, -10, W + 20, VY + 20, "url(#grey)"), rect(-10, VY, W + 20, H - VY + 10, "#7c7f84")]
    zn, zf = 0.2, 200
    # verges, pavements and the road, as long faces
    b.append(poly([P(-1400, GROUND, zn), P(-1400, GROUND, zf), P(-420, GROUND, zf), P(-420, GROUND, zn)], "#8a9a6a"))
    b.append(poly([P(1400, GROUND, zn), P(1400, GROUND, zf), P(420, GROUND, zf), P(420, GROUND, zn)], "#9a958c"))
    b.append(poly([P(-420, GROUND + 10, zn), P(-420, GROUND + 10, zf), P(420, GROUND + 10, zf), P(420, GROUND + 10, zn)], "#5d5f64"))
    b.append(poly([P(-420, GROUND + 10, zn), P(-420, GROUND + 10, zf), P(-160, GROUND + 10, zn)], "#64666b"))
    for X in (-420, 420):
        b.append(poly([P(X - 14, GROUND, zn), P(X - 14, GROUND, zf), P(X + 14, GROUND + 10, zf), P(X + 14, GROUND + 10, zn)], "#c9c6be"))
    # right: warehouses with loading bays; left: chain-link fence on posts, grey sheds behind
    for i in range(len(zs) - 1):
        za, zb = zs[i], zs[i + 1]
        zm = lambda f: za + (zb - za) * f
        k = i % IND_REPEAT
        c = ["#b9bcbf", "#a7abb0", "#c3c0b5"][k]
        b.append(poly([P(SHED, -420, za), P(SHED, -420, zb), P(SHED, GROUND, zb), P(SHED, GROUND, za)], c))
        b.append(poly([P(SHED, -420, za), P(SHED, -420, zb), P(SHED * 1.15, -520, zb), P(SHED * 1.15, -520, za)], shade(c, -0.25)))
        for f in (0.0, 0.25, 0.5, 0.75):   # corrugation
            b.append(poly([P(SHED, -420, zm(f)), P(SHED, -420, zm(f + 0.04)), P(SHED, GROUND, zm(f + 0.04)), P(SHED, GROUND, zm(f))], shade(c, -0.08)))
        b.append(poly([P(SHED, -150, zm(0.3)), P(SHED, -150, zm(0.75)), P(SHED, GROUND, zm(0.75)), P(SHED, GROUND, zm(0.3))], ["#d9a43a", "#5a6470", "#3c6e9e"][k]))
        for y in range(-120, GROUND, 60):
            b.append(poly([P(SHED, y, zm(0.3)), P(SHED, y, zm(0.75)), P(SHED, y + 6, zm(0.75)), P(SHED, y + 6, zm(0.3))], "#000000", ' opacity="0.25"'))
        # sheds behind the fence
        sc = ["#8f979e", "#9fa59a", "#868c94"][k]
        b.append(poly([P(-1100, -300, za), P(-1100, -300, zb), P(-1100, GROUND, zb), P(-1100, GROUND, za)], sc))
        b.append(poly([P(-1100, -300, za), P(-1100, -300, zb), P(-1250, -380, zb), P(-1250, -380, za)], shade(sc, -0.2)))
        # fence posts and a lamp post per bay
        for f in (0.0, 0.5):
            b.append(poly([P(FENCE - 6, -150, zm(f)), P(FENCE + 6, -150, zm(f)), P(FENCE + 6, GROUND, zm(f)), P(FENCE - 6, GROUND, zm(f))], "#4c5058"))
        if k == 0:
            for X in (-520, 520):
                b.append(poly([P(X - 8, -560, za), P(X + 8, -560, za), P(X + 8, GROUND, za), P(X - 8, GROUND, za)], "#3b4048"))
                b.append(poly([P(X, -560, za), P(X * 0.8, -580, za), P(X * 0.8, -560, za)], "#3b4048"))
                b.append(poly([P(X * 0.8 - 20, -560, za), P(X * 0.8 + 20, -560, za), P(X * 0.8 + 14, -548, za), P(X * 0.8 - 14, -548, za)], "#fff1b8"))
        # centre dashes
        b.append(poly([P(-8, GROUND + 10, zm(0.1)), P(8, GROUND + 10, zm(0.1)), P(8, GROUND + 10, zm(0.45)), P(-8, GROUND + 10, zm(0.45))], "#e8e2c8"))
    # the chain-link mesh: lines along the fence, top wire
    for Y in range(-150, GROUND, 30):
        a, c2 = P(FENCE, Y, zs[0]), P(FENCE, Y, zs[-1])
        b.append(line(a[0], a[1], c2[0], c2[1], "#6f747c", 1.2, ' opacity="0.7"'))
    a, c2 = P(FENCE, -150, zs[0]), P(FENCE, -150, zs[-1])
    b.append(line(a[0], a[1], c2[0], c2[1], "#4c5058", 3))
    write("backdrops", "industrial_road", {
        "backdrop.svg": svg(W, H, b, "Grey industrial road, portrait, vanishing at (360, 470): chain-link fence left, warehouses right; self-similar so it zoom-loops (backdrop.json zoom). Made by art/make_rooms.py."),
        "backdrop.json": depth_json(IND_ZOOM)})


# ------------------------------------------------------------------ impound hatch
# The portakabin wall fills the frame; the hatch is on the right (x 380-700, y 360-760), with the
# attendant behind it (cast at about x 540, y 1080, scale 0.62, depth -1) and the hatch_counter
# set piece over his lower half. James stands left, in front.
def impound_hatch():
    rnd = seeded(71)
    b = faceted(0, 0, W, 140, 6, 2, rnd, lambda cx, cy: shade(mix("#a9b2ba", "#d4d8d6", cy / 140), rnd.uniform(-0.03, 0.03)))
    # impounded cars behind a fence, glimpsed above the cabin
    for x0, c in ((10, "#c0392b"), (170, "#ecebe6"), (330, "#2f6fa8"), (500, "#2d2f36")):
        b.append(poly([(x0, 140), (x0 + 20, 100), (x0 + 120, 96), (x0 + 150, 140)], c))
    for x in range(0, W, 24):
        b.append(line(x, 60, x + 30, 150, "#6f747c", 1.5, ' opacity="0.6"'))
        b.append(line(x + 30, 60, x, 150, "#6f747c", 1.5, ' opacity="0.6"'))
    b.append(rect(0, 56, W, 5, "#4c5058"))
    # portakabin wall: ribbed cladding
    b.append(rect(0, 150, W, H - 150, "#d6d2c4"))
    for x in range(0, W, 36):
        b.append(rect(x, 150, 14, H - 150, "#c7c2b2"))
    b.append(rect(0, 150, W, 16, "#9c978a"))
    # sign
    b.append(rect(40, 200, 330, 110, "#f2c230"))
    b.append(rect(48, 208, 314, 94, "#1b1b1b"))
    b.append(rect(52, 212, 306, 86, "#f2c230"))
    b.append(text(205, 248, "VEHICLE RELEASE", 28, "#1b1b1b"))
    b.append(text(205, 282, "PAYMENT HERE · NO CASH", 15, "#1b1b1b", weight="700", family="Arial, Helvetica, sans-serif"))
    # opening hours notice
    b.append(rect(40, 360, 150, 170, "#ffffff"))
    b.append(text(115, 388, "OPEN", 18, "#c0392b"))
    for k, s in enumerate(("MON-FRI", "8 - 5", "SAT-SUN", "CLOSED", "£125/NIGHT")):
        b.append(text(115, 416 + k * 24, s, 15, "#1b1b1b", weight="700", family="Arial, Helvetica, sans-serif"))
    # the hatch: a window into the cabin, with the inside behind
    hx0, hy0, hx1, hy1 = 380, 360, 700, 760
    b.append(rect(hx0 - 16, hy0 - 16, hx1 - hx0 + 32, hy1 - hy0 + 32, "#8e98a3"))
    b += faceted(hx0, hy0, hx1, hy1, 4, 5, rnd, lambda cx, cy: shade("#b8c4b4", rnd.uniform(-0.05, 0.05)))
    b.append(rect(hx0 + 20, hy0 + 30, 110, 140, "#e9e4d8"))   # a calendar inside
    b.append(rect(hx0 + 20, hy0 + 30, 110, 30, "#c0392b"))
    for r in range(4):
        for c in range(4):
            b.append(rect(hx0 + 28 + c * 25, hy0 + 70 + r * 24, 18, 16, "#cfc8b8"))
    b.append(rect(hx1 - 110, hy0 + 40, 80, 160, "#7a8591"))   # filing cabinet
    for r in range(3):
        b.append(rect(hx1 - 104, hy0 + 48 + r * 50, 68, 42, "#8e99a5"))
        b.append(rect(hx1 - 80, hy0 + 64 + r * 50, 20, 6, "#c4c9cf"))
    # the sliding glass, pushed open on the left
    b.append(rect(hx0, hy0, 70, hy1 - hy0, "#cfe6ea", ' opacity="0.55"'))
    b.append(rect(hx0 + 66, hy0, 6, hy1 - hy0, "#8e98a3"))
    # ground: tarmac below the cabin
    b.append(rect(0, 1120, W, H - 1120, "#5d5f64"))
    b.append(rect(0, 1120, W, 10, "#4c4e53"))
    write("backdrops", "impound_hatch", {"backdrop.svg": svg(W, H, b, "Impound lot portakabin, portrait: VEHICLE RELEASE sign, opening hours, the payment hatch right with the attendant behind it. Made by art/make_rooms.py.")})

    # sill and wall under the hatch, with the card machine showing £500
    c = [rect(0, 0, 360, 30, "#8e98a3"), rect(0, 30, 360, 6, "#6d7680"), rect(0, 36, 360, 380, "#d6d2c4")]
    for x in range(0, 360, 36):
        c.append(rect(x, 36, 14, 380, "#c7c2b2"))
    c.append(poly([(200, 0), (270, 0), (276, -84), (206, -84)], "#2b2d33"))
    c.append(rect(212, -76, 56, 30, "#9fd39a"))
    c.append(text(240, -54, "£500", 17, "#1b1b1b"))
    for r in range(3):
        for k in range(3):
            c.append(rect(214 + k * 18, -38 + r * 11, 13, 7, "#5a5e68"))
    write("sets", "hatch_counter", {"piece.svg": svg(360, 506, ['<g transform="translate(0 90)">'] + c + ["</g>"], "Sill and cabin wall under the impound hatch, with the card machine showing £500. Anchor: bottom centre. Made by art/make_rooms.py."),
                                    "piece.json": json.dumps({"layer": "front"}) + "\n"})


def main():
    bath()
    corridor()
    office()
    kitchen()
    gaming_den()
    home_street()
    old_estate()
    industrial_road()
    impound_hatch()
    print("wrote bath, corridor, office, kitchen, gaming_den, home_street, industrial_road, impound_hatch and their set pieces")


if __name__ == "__main__":
    main()
