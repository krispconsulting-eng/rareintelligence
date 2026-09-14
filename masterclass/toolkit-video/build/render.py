"""Render the Kris Pierce Toolkit video.

Composites the supplied bag and the twelve official lab-button artworks over a
generated dark-studio background: each button pops in, holds long enough to be read,
then drops into the bag on the beat. Frames are piped straight to ffmpeg, so nothing
large is written to disk.

    python3 render.py                 # full cut
    python3 render.py --stills 2.4 9  # write single frames at those times instead
"""

from __future__ import annotations

import argparse
import colorsys
import math
import os
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, ImageOps

HERE = Path(__file__).resolve().parent
ASSETS = HERE.parent.parent
OUT = HERE / "out"
BAG = HERE.parent / "assets" / "bag" / "kris-pierce-toolkit-bag.png"

# Inter if it is available, otherwise whatever grotesque the machine has. Set
# TOOLKIT_FONT_DIR to a directory of Inter*.ttf to match the delivered cut exactly.
FONT_FALLBACK = {
    "InterDisplay-Medium.ttf": "LiberationSans-Regular.ttf",
    "InterDisplay-SemiBold.ttf": "LiberationSans-Bold.ttf",
    "InterDisplay-Bold.ttf": "LiberationSans-Bold.ttf",
}
FONT_DIRS = [
    Path(os.environ["TOOLKIT_FONT_DIR"]) if os.environ.get("TOOLKIT_FONT_DIR") else None,
    HERE / "fonts",
    Path("/usr/share/fonts/truetype/inter"),
]

W, H = 1080, 1920
FPS = 30
BPM = 120.0
BEAT = 60.0 / BPM

INTRO = 4 * BEAT * 2          # 4.0s, two bars
PER_BUTTON = 3 * BEAT         # 1.5s between buttons: the next pops in as the last lands
SETTLE = 0.5                  # how long a landing's flare and bag squash run into the next button
OUTRO = 4 * BEAT * 3          # 6.0s, three bars: the pull-back needs room

# The closing pull-back: where the horizon sits, where the bag ends up standing, how
# small it gets, and how much of its reflection shows on the floor.
STAGE_HORIZON = 1000
STAGE_BASE = 1250
STAGE_SCALE = 0.32
REFL_H = 260

# Each button's own timeline. It lands at 1.50, which is also when the next one pops
# in, so the settle after a landing plays under the next button's hold.
POP_END = 0.18
DROP_START = 1.10             # a 0.40s fall: quick, still easing into the bag
IMPACT = 1.50                 # on the beat
TITLE_FADE = (1.02, 1.20)     # clears before the falling button reaches the caption

# Measured on the supplied bag artwork (1210x1218 after keying).
BAG_FRONT_Y = 500             # top edge of the front panel: the line a button drops behind
BAG_MOUTH = (250, 970)        # x span of the open mouth
BAG_STRAPS = ((268, 300, 432, 500), (778, 300, 942, 500))  # handle straps, kept in front

INK = (5, 7, 12)
GOLD = (233, 185, 73)
WHITE = (245, 247, 250)
MUTED = (138, 147, 166)

# Official lab titles, in the order the artwork was supplied. US spellings are the
# product names as printed by MasterClass and are kept verbatim.
LABS = [
    ("ai-lab-01-data-analysis-with-ai.png", "Data Analysis with AI"),
    ("ai-lab-02-build-full-marketing-campaigns-with-ai.png", "Build Full Marketing Campaigns with AI"),
    ("ai-lab-03-training-ai-agents-from-domain-expertise-to-working-agent.png", "Training AI Agents"),
    ("ai-lab-04-financial-analysis-and-modeling-with-ai.png", "Financial Analysis and Modeling with AI"),
    ("ai-lab-05-answer-engine-optimization-ai-search-beyond-seo.png", "Answer Engine Optimization"),
    ("ai-lab-06-build-prototypes-with-ai.png", "Build Prototypes with AI"),
    ("ai-lab-07-how-ai-teams-build-and-govern-agents.png", "How AI Teams Build and Govern Agents"),
    ("ai-lab-08-turn-your-workflow-into-an-ai-superpower.png", "Turn Your Workflow into an AI Superpower"),
    ("ai-lab-09-customer-research-with-synthetic-users.png", "Customer Research with Synthetic Users"),
    ("ai-lab-10-build-ai-agents-for-sales-and-gtm.png", "Build AI Agents for Sales and GTM"),
    ("ai-lab-11-storytelling-and-slide-decks-with-ai.png", "Storytelling and Slide Decks with AI"),
    ("ai-lab-12-ai-for-customer-support.png", "AI for Customer Support"),
]

TOTAL = INTRO + PER_BUTTON * len(LABS) + OUTRO

BAG_W = 780
# Reels and TikTok put their own controls over roughly the bottom 260px, so the bag
# and every caption stay above that.
BAG_BOTTOM_MARGIN = 265
CARD_CENTRE = (540, 450)
CARD_SIZE = 264
TITLE_TOP = 690
PEEK_SIZE = 116
EYEBROW_Y = 104
DOTS_Y = 170


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    for directory in FONT_DIRS:
        if directory and (directory / name).exists():
            return ImageFont.truetype(str(directory / name), size)
    return ImageFont.truetype(
        f"/usr/share/fonts/truetype/liberation/{FONT_FALLBACK.get(name, 'LiberationSans-Regular.ttf')}", size
    )


def serif_font(size: int) -> ImageFont.FreeTypeFont:
    """A high-contrast serif for the closing line, in the MasterClass wordmark idiom."""
    for directory in FONT_DIRS:
        if not directory:
            continue
        for name, weight in (("PlayfairDisplay[wght].ttf", 600), ("CormorantGaramond-SemiBold.ttf", None)):
            path = directory / name
            if path.exists() and path.stat().st_size > 10_000:
                loaded = ImageFont.truetype(str(path), size)
                if weight:
                    try:
                        loaded.set_variation_by_axes([weight])
                    except Exception:
                        pass
                return loaded
    return ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf", size)


def clamp(t: float) -> float:
    return min(1.0, max(0.0, t))


def ease_out_back(t: float) -> float:
    c = 1.70158
    t -= 1.0
    return 1.0 + t * t * ((c + 1) * t + c)


def ease_in(t: float) -> float:
    return t * t


def drop_curve(t: float) -> float:
    """Gathers speed, then eases off into the bag: a pillow landing, not a hard hit."""
    return t * t * (3.0 - 2.0 * t)


def ease_out(t: float) -> float:
    return 1.0 - (1.0 - t) ** 3


def dominant_colour(img: Image.Image) -> tuple[int, int, int]:
    """The button's most saturated, reasonably bright colour, pushed vivid."""
    small = img.convert("RGBA").resize((40, 40), Image.LANCZOS)
    best, best_score = (120, 150, 220), -1.0
    for r, g, b, a in small.getdata():
        if a < 200:
            continue
        mx, mn = max(r, g, b), min(r, g, b)
        if mx < 60:
            continue
        sat = (mx - mn) / mx
        score = sat * (mx / 255.0) ** 0.4
        if score > best_score:
            best_score, best = score, (r, g, b)
    # Normalise to a vivid, consistently lit version of that hue, so a pale artwork
    # still throws a readable colour into the lighting and the progress dots.
    h, l, s = colorsys.rgb_to_hls(*(c / 255 for c in best))
    r, g, b = colorsys.hls_to_rgb(h, min(max(l, 0.46), 0.62), max(s, 0.66))
    return tuple(int(c * 255) for c in (r, g, b))


def upscale(art: Image.Image, size: int) -> Image.Image:
    """The artwork arrived at 80x80. Lanczos in two steps with an unsharp mask keeps
    edges crisp; it cannot add detail that is not there, so full-size originals
    dropped into masterclass/ will always beat this."""
    mid = art.resize((size * 2, size * 2), Image.LANCZOS)
    mid = mid.filter(ImageFilter.UnsharpMask(radius=3, percent=90, threshold=1))
    out = mid.resize((size, size), Image.LANCZOS)
    return out.filter(ImageFilter.UnsharpMask(radius=1.2, percent=70, threshold=2))


_glow_cache: dict[int, Image.Image] = {}


def glow_mask(size: int) -> Image.Image:
    size = max(8, (size // 16) * 16)
    if size not in _glow_cache:
        m = Image.new("L", (size, size), 0)
        d = ImageDraw.Draw(m)
        steps = 28
        for i in range(steps, 0, -1):
            f = i / steps
            r = size / 2 * f
            v = int(255 * (1 - f) ** 2.2)
            d.ellipse([size / 2 - r, size / 2 - r, size / 2 + r, size / 2 + r], fill=v)
        _glow_cache[size] = m.filter(ImageFilter.GaussianBlur(size / 22))
    return _glow_cache[size]


def add_glow(layer: Image.Image, centre, size: int, colour, strength: float) -> None:
    if strength <= 0.004:
        return
    mask = glow_mask(size).resize((size, size), Image.BILINEAR)
    if strength < 1.0:
        mask = mask.point(lambda v: int(v * strength))
    patch = Image.new("RGBA", (size, size), (*colour, 0))
    patch.putalpha(mask)
    layer.alpha_composite(patch, (int(centre[0] - size / 2), int(centre[1] - size / 2)))


def tracked_text(draw: ImageDraw.ImageDraw, xy, text, fnt, fill, tracking: float, anchor_centre=True):
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = xy[0] - total / 2 if anchor_centre else xy[0]
    for ch, wch in zip(text, widths):
        draw.text((x, xy[1]), ch, font=fnt, fill=fill)
        x += wch + tracking


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt, max_w: int) -> list[str]:
    if draw.textlength(text, font=fnt) <= max_w:
        return [text]
    words = text.split()
    # Prefer an even two-line break: a greedy wrap leaves titles hanging on one word.
    best = None
    for i in range(1, len(words)):
        a = " ".join(words[:i])
        b = " ".join(words[i:])
        wa, wb = draw.textlength(a, font=fnt), draw.textlength(b, font=fnt)
        if wa <= max_w and wb <= max_w and (best is None or max(wa, wb) < best[0]):
            best = (max(wa, wb), [a, b])
    if best:
        return best[1]
    lines, cur = [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


class Scene:
    def __init__(self) -> None:
        bag = Image.open(BAG).convert("RGBA")
        self.bag = bag.resize((BAG_W, round(BAG_W * bag.height / bag.width)), Image.LANCZOS)
        self.bag_x = (W - BAG_W) // 2
        self.bag_y = H - self.bag.height - BAG_BOTTOM_MARGIN
        scale = self.bag.height / 1218
        self.scale = scale
        self.rim_y = self.bag_y + int(BAG_FRONT_Y * scale)
        # Everything from the front rim down is re-composited over the buttons, so a
        # falling button disappears into the bag instead of sliding over its face. The
        # two handle straps rise above that line, so they are re-composited too.
        self.front = self.bag.crop((0, int(BAG_FRONT_Y * scale), BAG_W, self.bag.height))
        self.front_y = self.bag_y + int(BAG_FRONT_Y * scale)
        self.straps = []
        for x0, y0, x1, y1 in BAG_STRAPS:
            box = tuple(int(v * scale) for v in (x0, y0, x1, y1))
            self.straps.append((self.bag.crop(box), (self.bag_x + box[0], self.bag_y + box[1])))

        self.buttons, self.titles, self.colours, self.cards = [], [], [], []
        for filename, title in LABS:
            art = Image.open(ASSETS / filename).convert("RGBA")
            self.buttons.append(art)
            self.titles.append(title)
            self.colours.append(dominant_colour(art))
            self.cards.append(self.make_card(art, CARD_SIZE))
        self.peeks = [self.make_peek(art, i) for i, art in enumerate(self.buttons)]

        self.f_eyebrow = font("InterDisplay-Medium.ttf", 26)
        self.f_title = font("InterDisplay-SemiBold.ttf", 54)
        self.f_big = font("InterDisplay-Bold.ttf", 82)
        self.f_sub = font("InterDisplay-Medium.ttf", 38)
        self.f_kicker = font("InterDisplay-Medium.ttf", 30)
        self.f_serif = serif_font(96)

        self.base = self.make_base()
        self.stage = self.make_stage()
        mouth_l = self.bag_x + int(BAG_MOUTH[0] * scale)
        mouth_r = self.bag_x + int(BAG_MOUTH[1] * scale)
        step = (mouth_r - mouth_l) / (len(LABS) - 1)
        # Settled buttons fan across the mouth, but every button falls through the deep
        # centre of the opening: a drop aimed at the far edges reads as passing in front
        # of the bag rather than going into it.
        self.landing_x = [int(mouth_l + i * step) for i in range(len(LABS))]
        self.drop_x = [540 + ((i % 5) - 2) * 32 for i in range(len(LABS))]

    def make_card(self, art: Image.Image, size: int = 320) -> Image.Image:
        """One button as a rounded card: upscaled artwork, hairline edge, soft shadow."""
        pad = 26
        canvas = Image.new("RGBA", (size + pad * 2, size + pad * 2), (0, 0, 0, 0))
        face = upscale(art, size)
        mask = Image.new("L", (size, size), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, size - 1, size - 1], radius=size // 7, fill=255)

        shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        ImageDraw.Draw(shadow).rounded_rectangle(
            [pad, pad + 8, pad + size, pad + size + 8], radius=size // 7, fill=(0, 0, 0, 170)
        )
        canvas.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(16)))

        face.putalpha(mask)
        canvas.alpha_composite(face, (pad, pad))
        edge = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        ImageDraw.Draw(edge).rounded_rectangle(
            [pad, pad, pad + size - 1, pad + size - 1], radius=size // 7, outline=(255, 255, 255, 48), width=2
        )
        canvas.alpha_composite(edge)
        return canvas

    def make_peek(self, art: Image.Image, index: int) -> Image.Image:
        """A button as it sits in the bag: smaller, rounded, angled, shaded by the bag."""
        size = PEEK_SIZE
        face = upscale(art, size)
        mask = Image.new("L", (size, size), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, size - 1, size - 1], radius=size // 7, fill=255)
        face.putalpha(mask)
        shade = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        d = ImageDraw.Draw(shade)
        for y in range(size):
            d.line([(0, y), (size, y)], fill=(2, 4, 9, int(150 * (y / size) ** 1.6)))
        shade.putalpha(Image.composite(shade.getchannel("A"), Image.new("L", (size, size), 0), mask))
        face.alpha_composite(shade)
        edge = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        ImageDraw.Draw(edge).rounded_rectangle(
            [0, 0, size - 1, size - 1], radius=size // 7, outline=(255, 255, 255, 40), width=2
        )
        face.alpha_composite(edge)
        return face.rotate(-7 + (index * 37) % 15, Image.BICUBIC, expand=True)

    def make_base(self) -> Image.Image:
        base = Image.new("RGBA", (W, H), (*INK, 255))
        grid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(grid)
        for x in range(0, W + 1, 72):
            d.line([(x, 0), (x, H)], fill=(120, 140, 180, 16), width=1)
        for y in range(0, H + 1, 72):
            d.line([(0, y), (W, y)], fill=(120, 140, 180, 16), width=1)
        base.alpha_composite(grid)
        add_glow(base, (540, 640), 1400, (40, 70, 130), 0.55)
        return base

    def make_stage(self) -> Image.Image:
        """The pulled-back view: a floor grid running off to a horizon, hazed near the
        vanishing point, and one spotlight on the spot where the bag will stand."""
        stage = Image.new("RGBA", (W, H), (*INK, 255))
        d = ImageDraw.Draw(stage)
        yh, depth = STAGE_HORIZON, H - STAGE_HORIZON
        for xb in range(-2600, W + 2600, 96):
            d.line([(540, yh), (xb, H)], fill=(120, 140, 180, 14), width=1)
        for n in range(80):
            y = yh + depth / (1 + n * 0.16)
            a = int(24 * ((y - yh) / depth) ** 0.6)
            if a < 2:
                break
            d.line([(0, y), (W, y)], fill=(120, 140, 180, a), width=1)
        haze = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        hd = ImageDraw.Draw(haze)
        for y in range(yh, yh + 300):
            hd.line([(0, y), (W, y)], fill=(*INK, int(255 * (1 - (y - yh) / 300) ** 1.6)))
        stage.alpha_composite(haze)
        glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(glow).line([(0, yh), (W, yh)], fill=(150, 170, 215, 46), width=3)
        stage.alpha_composite(glow.filter(ImageFilter.GaussianBlur(20)))
        beam = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(beam).polygon(
            [(490, -60), (590, -60), (790, STAGE_BASE + 20), (290, STAGE_BASE + 20)], fill=(255, 236, 190, 26)
        )
        stage.alpha_composite(beam.filter(ImageFilter.GaussianBlur(48)))
        pool = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(pool).ellipse([240, STAGE_BASE - 64, 840, STAGE_BASE + 64], fill=(255, 226, 160, 130))
        stage.alpha_composite(pool.filter(ImageFilter.GaussianBlur(55)))
        return stage

    def bag_group(self, lift: float, mirror: float) -> tuple[Image.Image, int]:
        """The finished bag with all twelve buttons and its reflection on the floor, as
        one layer so the pull-back can scale it as a whole. Returns the layer and the
        y of the bag's base within it."""
        top = 24
        layer = Image.new("RGBA", (BAG_W, top + self.bag.height + REFL_H + 48), (0, 0, 0, 0))
        yb = int(top - lift)
        base = yb + self.bag.height
        if mirror > 0.01:
            refl = ImageOps.flip(self.bag).crop((0, 0, BAG_W, REFL_H))
            r, g, b, a = refl.split()
            grad = ImageOps.invert(Image.linear_gradient("L").resize((BAG_W, REFL_H)))
            grad = grad.point(lambda v: int(v * 0.45 * mirror))
            dim = 0.55
            refl = Image.merge("RGBA", (
                r.point(lambda v: int(v * dim)), g.point(lambda v: int(v * dim)),
                b.point(lambda v: int(v * dim)), ImageChops.multiply(a, grad),
            ))
            layer.alpha_composite(refl.filter(ImageFilter.GaussianBlur(2.5)), (0, base + int(2 * lift)))
        layer.alpha_composite(self.bag, (0, yb))
        dx, dy = -self.bag_x, yb - self.bag_y
        for i in range(len(LABS)):
            peek = self.peeks[i]
            arc = int(10 * math.sin(math.pi * (i + 0.5) / len(LABS)))
            layer.alpha_composite(peek, (self.landing_x[i] - peek.width // 2 + dx, self.rim_y - 76 - arc + dy))
        layer.alpha_composite(self.front, (0, self.front_y + dy))
        for strap, (sx, sy) in self.straps:
            layer.alpha_composite(strap, (sx + dx, sy + dy))
        return layer, base

    def vignette(self) -> Image.Image:
        v = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(v)
        steps = 40
        for i in range(steps):
            f = i / steps
            inset = -int(W * 0.5 * f)
            d.rounded_rectangle(
                [inset, inset, W - inset, H - inset], radius=400, outline=(0, 0, 0, 10), width=26
            )
        return v.filter(ImageFilter.GaussianBlur(40))

    # ---- timeline ------------------------------------------------------------

    def phase(self, t: float):
        if t < INTRO:
            return ("intro", t, None)
        t -= INTRO
        index = int(t // PER_BUTTON)
        if index < len(LABS):
            return ("button", t - index * PER_BUTTON, index)
        return ("outro", t - len(LABS) * PER_BUTTON, None)

    def landed_count(self, kind: str, local: float, index: int | None) -> int:
        if kind == "intro":
            return 0
        if kind == "outro":
            return len(LABS)
        return index + (1 if local >= IMPACT else 0)

    def frame(self, t: float) -> Image.Image:
        kind, local, index = self.phase(t)
        img = self.base.copy()
        landed = self.landed_count(kind, local, index)

        colour = self.colours[index] if kind == "button" else GOLD
        # The button that has just landed is the previous one; its flare and the bag's
        # squash run for SETTLE seconds under the current button's entrance.
        impact_age, impact_colour = None, colour
        if kind == "button" and index > 0 and local < SETTLE:
            impact_age, impact_colour = local, self.colours[index - 1]
        elif kind == "outro" and local < SETTLE:
            impact_age, impact_colour = local, self.colours[-1]

        # Light in the scene: a travelling ribbon behind the button and a pool of the
        # button's colour on the floor that flares as it lands.
        if kind == "button":
            if local < DROP_START:
                lead = 0.35 + 0.3 * math.sin(t * 2.2)
                add_glow(img, (540, 520), 1000, colour, 0.20 * lead)
            else:
                p = min(1.0, (local - DROP_START) / (IMPACT - DROP_START))
                y = 520 + (self.rim_y - 520) * drop_curve(p)
                add_glow(img, (self.trail_x(index, p), y), 900, colour, 0.26)
        add_glow(img, (540, self.rim_y + 40), 1500, colour, 0.18)
        if impact_age is not None:
            add_glow(img, (540, self.rim_y + 40), 1500, impact_colour, 0.40 * math.exp(-impact_age * 4.0))

        if kind == "outro":
            img = self.draw_outro_scene(img, local, impact_age)
            img.alpha_composite(self.vig)
            return img

        self.draw_bag(img, kind, local, impact_age, landed, impact_colour)
        if kind == "button":
            self.draw_button(img, index, local, colour)
        else:
            self.draw_intro(img, local)
        self.draw_chrome(img, landed, kind, local)
        img.alpha_composite(self.vig)
        return img

    def trail_x(self, index: int, p: float) -> float:
        return 540 + (self.drop_x[index] - 540) * p

    def draw_bag(self, img, kind, local, impact_age, landed, colour) -> None:
        squash = 1.0
        if impact_age is not None and impact_age < 0.5:
            # One soft compression that eases back out; no rebound, so nothing shakes.
            squash = 1.0 - 0.009 * math.exp(-impact_age * 5.0) * min(1.0, impact_age / 0.06)
        bag = self.bag
        y = self.bag_y
        if abs(squash - 1.0) > 0.001:
            nh = max(1, int(self.bag.height * squash))
            bag = self.bag.resize((BAG_W, nh), Image.BILINEAR)
            y = self.bag_y + (self.bag.height - nh)
        # No fade-in on the bag: platforms use frame one as the cover, so the opening
        # frame has to be the finished composition, not black.
        img.alpha_composite(bag, (self.bag_x, y))

        for i in range(landed):
            peek = self.peeks[i]
            arc = int(10 * math.sin(math.pi * (i + 0.5) / len(LABS)))
            img.alpha_composite(peek, (self.landing_x[i] - peek.width // 2, self.rim_y - 76 - arc))

        front = self.front
        fy = self.front_y
        if abs(squash - 1.0) > 0.001:
            nh = max(1, int(self.front.height * squash))
            front = self.front.resize((BAG_W, nh), Image.BILINEAR)
            fy = self.front_y + (self.bag.height - int(self.bag.height * squash))
        img.alpha_composite(front, (self.bag_x, fy))
        for strap, pos in self.straps:
            img.alpha_composite(strap, pos)

        if impact_age is not None and impact_age < 0.7:
            add_glow(img, (self.drop_x[min(landed, len(LABS)) - 1], self.rim_y - 10),
                     560, colour, 0.55 * math.exp(-impact_age * 4.5))

    def draw_button(self, img, index, local, colour) -> None:
        card = self.cards[index]
        cx, cy = CARD_CENTRE

        if local < POP_END:
            p = local / POP_END
            scale = 0.62 + (1.0 - 0.62) * ease_out_back(p)
            alpha, rot, x, y = p, -7 * (1 - p), cx, cy
        elif local < DROP_START:
            scale, alpha, rot = 1.0, 1.0, 0.0
            x, y = cx, cy + 7 * math.sin((local - POP_END) * 3.1)
        elif local < IMPACT:
            p = (local - DROP_START) / (IMPACT - DROP_START)
            e = drop_curve(p)
            scale = 1.0 - 0.62 * e
            x = self.trail_x(index, e)
            y = cy + (self.rim_y + 70 - cy) * e
            rot, alpha = 6 * e, 1.0
        else:
            return

        size = max(8, int(scale * card.width))
        drawn = card if size == card.width else card.resize((size, size), Image.LANCZOS)
        if rot:
            drawn = drawn.rotate(-rot, Image.BICUBIC, expand=True)

        if local >= DROP_START:
            p = (local - DROP_START) / (IMPACT - DROP_START)
            for g in range(1, 4):
                gp = max(0.0, drop_curve(p) - g * 0.07)
                gx = cx + (self.drop_x[index] - cx) * gp
                gy = cy + (self.rim_y + 70 - cy) * gp
                ghost = drawn.copy()
                ghost.putalpha(ghost.getchannel("A").point(lambda v, g=g: int(v * (0.16 - g * 0.04))))
                img.alpha_composite(ghost, (int(gx - ghost.width / 2), int(gy - ghost.height / 2)))

        if alpha < 1.0:
            drawn = drawn.copy()
            drawn.putalpha(drawn.getchannel("A").point(lambda v: int(v * alpha)))
        add_glow(img, (x, y), int(size * 1.9), colour, 0.30 * alpha)
        img.alpha_composite(drawn, (int(x - drawn.width / 2), int(y - drawn.height / 2)))

        fade = min(1.0, local / 0.14)
        if local > TITLE_FADE[0]:
            fade = max(0.0, 1.0 - (local - TITLE_FADE[0]) / (TITLE_FADE[1] - TITLE_FADE[0]))
        if fade > 0.01:
            self.draw_title(img, self.titles[index], index, fade, local)

    def draw_title(self, img, title, index, fade, local) -> None:
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        lines = wrap(d, title, self.f_title, 860)
        rise = int(16 * (1 - min(1.0, local / 0.22)))
        y = TITLE_TOP + rise
        num = f"LAB {index + 1:02d} / {len(LABS)}"
        tracked_text(d, (540, y - 52), num, self.f_kicker, (*self.colours[index], 255), 4.0)
        for line in lines:
            d.text((540, y), line, font=self.f_title, fill=(*WHITE, 255), anchor="ma")
            y += 66
        if fade < 1.0:
            layer.putalpha(layer.getchannel("A").point(lambda v: int(v * fade)))
        img.alpha_composite(layer)

    def draw_intro(self, img, local) -> None:
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        # Full opacity from frame one (it doubles as the thumbnail); only a slow settle.
        a = 1.0
        out = 1.0 if local < INTRO - 0.5 else max(0.0, (INTRO - local) / 0.5)
        rise = int(14 * (1 - ease_out(min(1.0, local / 1.2))))
        d.text((540, 430 + rise), "Twelve AI labs.", font=self.f_big, fill=(*WHITE, 255), anchor="ma")
        d.text((540, 530 + rise), "One toolkit.", font=self.f_big, fill=(*GOLD, 255), anchor="ma")
        d.text((540, 668 + rise), "What MasterClass Executive is adding", font=self.f_sub, fill=(*MUTED, 255), anchor="ma")
        d.text((540, 716 + rise), "across all aspects of my work", font=self.f_sub, fill=(*MUTED, 255), anchor="ma")
        layer.putalpha(layer.getchannel("A").point(lambda v: int(v * a * out)))
        img.alpha_composite(layer)

    def draw_outro_scene(self, img: Image.Image, local: float, impact_age: float | None) -> Image.Image:
        """The pull-back. The bag lifts a fraction and its reflection deepens, then the
        camera pulls back until it stands small under one spotlight on a stage whose
        floor runs off to the horizon. One line, the eyebrow, and out."""
        lift_p = ease_out(clamp((local - 0.2) / 0.9))
        p = drop_curve(clamp((local - 0.7) / 3.5))

        if impact_age is not None:
            add_glow(img, (self.drop_x[-1], self.rim_y - 10), 560, self.colours[-1],
                     0.55 * math.exp(-impact_age * 4.5))

        chrome_fade = 1.0 - clamp(local / 0.5)
        if chrome_fade > 0:
            chrome = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            self.draw_chrome(chrome, len(LABS), "outro", local)
            chrome.putalpha(chrome.getchannel("A").point(lambda v: int(v * chrome_fade)))
            img.alpha_composite(chrome)

        if p > 0:
            img = Image.blend(img, self.stage, p)

        group, base_y = self.bag_group(14 * lift_p, lift_p)
        s = 1.0 - (1.0 - STAGE_SCALE) * p
        floor = self.bag_y + self.bag.height
        ay = floor + (STAGE_BASE - floor) * p
        if s < 0.999:
            group = group.resize((max(1, int(group.width * s)), max(1, int(group.height * s))), Image.LANCZOS)
        img.alpha_composite(group, (int(540 - group.width / 2), int(ay - base_y * s)))

        text = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(text)
        ta = ease_out(clamp((local - 3.0) / 1.0))
        if ta > 0:
            rise = int(22 * (1 - ta))
            for i, line in enumerate(("Building expertise", "one skill at a time.")):
                d.text((540, 700 + i * 104 + rise), line, font=self.f_serif,
                       fill=(*GOLD, int(255 * ta)), anchor="ma")
        ea = clamp((local - 4.6) / 0.6)
        if ea > 0:
            tracked_text(d, (540, 940), "MASTERCLASS EXECUTIVE", self.f_eyebrow, (*GOLD, int(220 * ea)), 7.0)
        img.alpha_composite(text)

        black = clamp((local - (OUTRO - 1.0)) / 1.0)
        if black > 0:
            img.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, int(255 * black))))
        return img

    def draw_chrome(self, img, landed, kind, local) -> None:
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        tracked_text(d, (540, EYEBROW_Y), "MASTERCLASS EXECUTIVE", self.f_eyebrow, (*GOLD, 220), 7.0)
        n = len(LABS)
        span = 56 * (n - 1)
        for i in range(n):
            x = 540 - span / 2 + i * 56
            if i < landed:
                fill = (*self.colours[i], 255)
                r = 9
                if kind == "button" and i == landed - 1 and local < 0.3:
                    r = 9 + int(5 * math.exp(-local * 12))
            else:
                fill, r = (255, 255, 255, 40), 6
            d.ellipse([x - r, DOTS_Y - r, x + r, DOTS_Y + r], fill=fill)
        img.alpha_composite(layer)

    def camera(self, img: Image.Image, t: float) -> Image.Image:
        kind, local, index = self.phase(t)
        # A slow push-in across the whole cut and a gentle one over the closing card.
        # No kick on the landings: the bag takes the weight, the frame stays still.
        zoom = 1.0 + 0.016 * (t / TOTAL)
        if zoom <= 1.0005:
            return img
        cw, ch = int(W / zoom), int(H / zoom)
        box = ((W - cw) // 2, (H - ch) // 2, (W - cw) // 2 + cw, (H - ch) // 2 + ch)
        return img.crop(box).resize((W, H), Image.BICUBIC)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stills", nargs="*", type=float)
    ap.add_argument("--out", default=str(HERE.parent / "kris-pierce-toolkit.mp4"))
    args = ap.parse_args()

    scene = Scene()
    scene.vig = scene.vignette()

    if args.stills:
        OUT.mkdir(parents=True, exist_ok=True)
        for t in args.stills:
            frame = scene.camera(scene.frame(t), t)
            path = OUT / f"_still_{t:06.2f}.png"
            frame.convert("RGB").save(path)
            print(path)
        return 0

    frames = int(TOTAL * FPS)
    print(f"{TOTAL:.1f}s, {frames} frames", file=sys.stderr)
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        # Conservative H.264: Main profile, no B-frames (so presentation order is decode
        # order and there is no edit list), a keyframe every second. Any platform's
        # thumbnailer can read frame one from this.
        "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p",
        "-profile:v", "main", "-level", "4.0", "-bf", "0", "-g", "30", "-keyint_min", "30",
        "-sc_threshold", "0", "-movflags", "+faststart", args.out,
    ]
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(frames):
        t = i / FPS
        frame = scene.camera(scene.frame(t), t)
        proc.stdin.write(frame.convert("RGB").tobytes())
        if i % 60 == 0:
            print(f"  {i}/{frames}", file=sys.stderr)
    proc.stdin.close()
    if proc.wait() != 0:
        return 1
    print(args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
