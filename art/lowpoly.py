"""Shared helpers for the series' faceted low-poly art (art/make_*.py)."""
import math
import random


def hexrgb(c):
    c = c.lstrip("#")
    return [int(c[i:i + 2], 16) for i in (0, 2, 4)]


def rgbhex(rgb):
    return "#" + "".join(f"{max(0, min(255, round(v))):02x}" for v in rgb)


def mix(a, b, t):
    a, b = hexrgb(a), hexrgb(b)
    return rgbhex([x + (y - x) * t for x, y in zip(a, b)])


def shade(c, f):
    """f > 0 lightens towards white, f < 0 darkens towards black."""
    return mix(c, "#ffffff", f) if f > 0 else mix(c, "#000000", -f)


def poly(ps, fill, extra=""):
    return f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in ps)}" fill="{fill}"{extra}/>'


def rect(x, y, w, h, fill, extra=""):
    return poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], fill, extra)


def text(x, y, s, size, fill, weight="900", family="Arial Black, Arial, Helvetica, sans-serif", extra=""):
    s = s.replace("&", "&amp;")
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{family}" font-weight="{weight}" font-size="{size}" '
            f'fill="{fill}" text-anchor="middle"{extra}>{s}</text>')


def tri_grid(x0, y0, x1, y1, nx, ny, rnd, jitter=0.38):
    """A jittered grid cut into triangles: the faceted look."""
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
            tris += [(a, b, c), (a, c, d)] if rnd.random() < 0.5 else [(a, b, d), (b, c, d)]
    return tris


def centroid(t):
    return sum(p[0] for p in t) / len(t), sum(p[1] for p in t) / len(t)


def faceted(x0, y0, x1, y1, nx, ny, rnd, color_at, jitter=0.38):
    """Fill a box with facets; color_at(cx, cy) picks each triangle's colour."""
    return [poly(t, color_at(*centroid(t))) for t in tri_grid(x0, y0, x1, y1, nx, ny, rnd, jitter)]


def svg(w, h, body, comment="", view=None):
    vb = view or f"0 0 {w} {h}"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="{w}" height="{h}">\n'
            + (f"  <!-- {comment} -->\n" if comment else "") + "  " + "\n  ".join(body) + "\n</svg>\n")


def gem(cx, cy, r, colors, n=8, squash=1.0, rot=0.3):
    """A faceted disc (lamp shade, wheel, grille): n wedges in the given colours."""
    ring = [(cx + r * math.cos(a), cy + r * squash * math.sin(a)) for a in [i * 2 * math.pi / n + rot for i in range(n)]]
    return [poly([(cx, cy), ring[i], ring[(i + 1) % n]], colors[i % len(colors)]) for i in range(n)]


def spines(x0, y0, x1, y1, rnd, palette, lean=True):
    """Record sleeves on a shelf seen edge-on: thin upright strips, a few leaning."""
    out = []
    x = x0 + 2
    while x < x1 - 4:
        w = rnd.uniform(5, 11)
        c = shade(rnd.choice(palette), rnd.uniform(-0.15, 0.1))
        top = y0 + rnd.uniform(0, 8)
        if lean and rnd.random() < 0.08 and x + w + 18 < x1:
            out.append(poly([(x, y1), (x + w, y1), (x + w + 16, top + 6), (x + 16, top + 6)], c))
            x += w + 18
            continue
        out.append(poly([(x, top), (x + w, top), (x + w, y1), (x, y1)], c))
        out.append(poly([(x, top), (x + w * 0.35, top), (x + w * 0.35, y1), (x, y1)], shade(c, -0.2)))
        x += w + rnd.uniform(0.5, 1.5)
    return out


RECORD_COLORS = ["#d94f3d", "#f2b134", "#3c8de8", "#2a9d8f", "#f4f1de", "#222222", "#e76f51", "#8e44ad",
                 "#264653", "#e9c46a", "#b5838d", "#6d6875", "#118ab2", "#ef476f", "#06d6a0"]


def seeded(n):
    return random.Random(n)
