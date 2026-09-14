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
they are shown at 300 pixels, which is as far as they stretch before the softness
shows. If full-size originals turn up, drop them in and the cards get sharper with no
other change.

Because the artwork carries no lettering, every title is set as type beneath the card
rather than lifted off the button.

## Light and colour

Each button's dominant colour is read from its own artwork, then pushed to a consistent
vividness. That colour drives the trail behind the falling button, the flare when it
lands, the pool of light on the floor and its dot in the progress row. So the palette
comes from the labs themselves, not from a fixed scheme.

## Motion

Fast and physical, on purpose: a scale-up with overshoot on entry, a gravity curve on
the drop, a tilt, a four-step ghost trail, and on landing a bag bump, a flare and a
three per cent camera kick that eases back out. There is also a slow push-in across the
whole 32 seconds and a stronger one over the closing card.

No strobing and no flicker anywhere, deliberately. Flares are short and single, never
repeated fast enough to flash.

## Type

The titles are the official lab names. Two-line titles are broken evenly rather than
greedily, so no title hangs on a single orphan word.

The title fades out as the drop begins, which is what keeps the falling card from
crossing the text.

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
