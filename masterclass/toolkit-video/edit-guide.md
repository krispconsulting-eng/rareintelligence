# Edit guide

How the cut is assembled, and what to change if you want it to behave differently.
Everything here is in `build/render.py`.

## Layers, bottom to top

1. Background: near-black ground, a faint charcoal grid, and a pool of light in the
   colour of whichever button is in play.
2. The bag.
3. Buttons already in the bag, fanned across the mouth.
4. The bag's front panel, re-composited from the rim down, plus the two handle straps.
   This is what a falling button disappears behind, so it goes into the bag rather than
   sliding over its face.
5. The falling button and its trail.
6. Type: the eyebrow, the twelve dots, the lab title.

The bag artwork is never redrawn. The only things done to it are a scale and, on
landing, a brief vertical squash of about two per cent.

## Button artwork

The twelve lab artworks are used exactly as supplied. The renderer only scales them,
rounds the corners, adds a hairline edge and a shadow, and rotates them a few degrees.
Nothing is recoloured or retitled.

They arrived at 80 x 80 pixels, which is the one real constraint on this cut. On screen
they are shown at 264 pixels, upscaled in two Lanczos steps with an unsharp mask at
each, which keeps edges crisp but cannot invent detail. If full-size originals turn up,
drop them into `masterclass/` under the same filenames and the cards sharpen with no
other change.

Because the artwork carries no lettering, every title is set as type beneath the card
rather than lifted off the button.

## Light and colour

Each button's dominant colour is read from its own artwork, then pushed to a consistent
vividness. That colour drives the trail behind the falling button, the flare when it
lands, the pool of light on the floor and its dot in the progress row. So the palette
comes from the labs themselves, not from a fixed scheme.

## Motion

Quick on the way in, soft on the way down. A scale-up with overshoot on entry, then a
drop that gathers speed and eases off into the bag rather than hitting it, with a slight
tilt and a faint three-step trail. On landing the bag gives about one per cent and eases
back with no rebound, and a flare of the button's colour blooms at the mouth. The frame
itself does not move on a landing; the only camera movement is a slow push-in across
the whole 32 seconds and a gentle one over the closing card.

No strobing and no flicker anywhere, deliberately. Flares are short and single, never
repeated fast enough to flash.

## Type

The titles are the official lab names. Two-line titles are broken evenly rather than
greedily, so no title hangs on a single orphan word.

The title fades out as the drop begins, which is what keeps the falling card from
crossing the text.

## The ending

Three bars. The bed drops out on the bar line after the twelfth landing. The bag,
with all twelve buttons in it, is rendered as one group together with a reflection of
itself on the floor; it lifts fourteen pixels over nine tenths of a second while the
reflection deepens. Then the flat grid crossfades into a stage: a perspective floor
converging on a horizon, hazed near the vanishing point, with a single beam and a pool
of light where the bag will stand. The group scales down to about a third and rises to
that spot over three and a half seconds on the same curve as the drops. "This is the
start." fades up in Playfair Display at 600 weight, the eyebrow follows beneath it, and
the frame fades to black over the last second. The scale flip is the point: it stops
being a handbag and becomes a foundation.

The stage geometry is four constants: `STAGE_HORIZON`, `STAGE_BASE` (where the bag
stands), `STAGE_SCALE` and `REFL_H`.

## Safe areas

The bag and every caption sit above y=1655, clear of the roughly 260 pixels of controls
that Reels and TikTok put over the bottom of the frame. The eyebrow and dots sit below
y=100 for the same reason at the top. Keep both if you move anything.

## Common changes

| To do this | Change |
|---|---|
| Slow the titles down | `PER_BUTTON` (see `sequence.md` on the beat grid) |
| Change a title | `LABS` |
| Reorder the labs | `LABS`, order is the order they drop |
| Shift the bag | `BAG_W`, `BAG_BOTTOM_MARGIN` |
| Move where buttons disappear | `BAG_FRONT_Y`, measured on the bag artwork |
| Change how wide they fan in the bag | `BAG_MOUTH` |
