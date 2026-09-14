# Assets

## What is where

| Path | What |
|---|---|
| `../../Codex Image 14 Sept 2026, 15_44_19.png` | The bag as supplied |
| `../../ai-lab-01…12-*.png` | The twelve official lab-button artworks as supplied |
| `bag/kris-pierce-toolkit-bag.png` | The bag with a real alpha channel, built by `../build/prepare_bag.py` |

The source files sit at the top of `masterclass/` where they were uploaded. The
renderer reads them from there, so leave them alone or update the paths in
`../build/render.py`.

## The bag

Supplied as RGB with the transparency checkerboard flattened into the pixels, so it had
to be keyed: mark the grey, bright pixels, keep the ones connected to the border plus
the large enclosed gap between the handles, then pull the matte in a pixel and soften it
to kill the fringe the checker left on antialiased edges. That is
`../build/prepare_bag.py`, and `bag/kris-pierce-toolkit-bag.png` is the result.

Front-facing black leather tote with gold hardware; "MasterClass Executive" in gold
serif across the front panel; a six-colour strip beneath it; "KRIS PIERCE TOOLKIT" in
small gold capitals below that.

Two positions are measured off this artwork and hard-coded in `../build/render.py`:
`BAG_FRONT_Y = 500` is the top edge of the front panel, the line a falling button
disappears behind, and `BAG_MOUTH = (250, 970)` is the span of the open mouth. Both are
in the keyed image's own pixels, so they only need changing if the bag artwork is
replaced.

## The twelve buttons

All twelve are 80 x 80 pixels and carry no lettering. Two consequences, both handled in
the cut but worth knowing:

- On screen they are shown at 300 pixels, which is about as far as an 80-pixel source
  stretches before it softens. Full-size originals would sharpen the cards noticeably
  and need no other change; they are worth pulling off the MasterClass platform if you
  can.
- Every lab title is set as type beneath the card, because there is no title on the
  artwork to show.

Titles come from the filenames and are used verbatim, US spellings included, since they
are product names. Two are shortened on screen to fit the dwell time; see
`../sequence.md`.

## One thing to know about this repository

`rareintelligence` is public and is deployed as a live site, so the MasterClass artwork
committed here is publicly reachable. That was fine to do and nothing is broken by it,
but if the artwork should not be public, the fix is to move `masterclass/` into a
private repository of its own rather than to delete files from this one: they stay in
the git history either way.
