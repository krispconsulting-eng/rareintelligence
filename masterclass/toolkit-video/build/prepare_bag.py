"""Key the baked-in transparency checkerboard out of the supplied bag PNG.

The bag was exported as RGB with the checker pattern flattened into the pixels, so
alpha has to be recovered: mark grey, bright pixels, keep only the region connected to
the border, then unpremultiply the halo the checker left on antialiased edges.
"""

import sys
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

HERE = Path(__file__).resolve().parent
SRC = HERE.parent.parent / "Codex Image 14 Sept 2026, 15_44_19.png"
OUT = HERE.parent / "assets" / "bag" / "kris-pierce-toolkit-bag.png"


def main() -> int:
    if not SRC.exists():
        print(f"missing source: {SRC}", file=sys.stderr)
        return 1

    img = Image.open(SRC).convert("RGB")
    rgb = np.asarray(img).astype(np.int16)
    h, w = rgb.shape[:2]

    spread = rgb.max(axis=2) - rgb.min(axis=2)
    value = rgb.max(axis=2)
    checker = (spread < 14) & (value > 168)

    # Checker pixels form the background where they reach the border, or where they sit
    # in a large enclosed gap such as the space between the handles. Small enclosed
    # patches are the bag's own white stitching and highlights, which must stay opaque.
    background = np.zeros((h, w), dtype=bool)
    visited = np.zeros((h, w), dtype=bool)
    for sy in range(h):
        for sx in range(w):
            if not checker[sy, sx] or visited[sy, sx]:
                continue
            component = []
            touches_border = False
            queue = deque([(sy, sx)])
            visited[sy, sx] = True
            while queue:
                y, x = queue.popleft()
                component.append((y, x))
                if y in (0, h - 1) or x in (0, w - 1):
                    touches_border = True
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < h and 0 <= nx < w and checker[ny, nx] and not visited[ny, nx]:
                        visited[ny, nx] = True
                        queue.append((ny, nx))
            if touches_border or len(component) > 5000:
                for y, x in component:
                    background[y, x] = True

    alpha = np.where(background, 0, 255).astype(np.uint8)
    alpha_img = Image.fromarray(alpha, "L")
    # Pull the matte in by a pixel and soften it: the checker bled into every
    # antialiased edge, and a hard matte keeps that light fringe.
    alpha_img = alpha_img.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.6))

    out = Image.merge("RGBA", (*img.split(), alpha_img))
    bbox = out.getbbox()
    if bbox:
        out = out.crop(bbox)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    out.save(OUT)
    print(f"wrote {OUT} {out.size}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
