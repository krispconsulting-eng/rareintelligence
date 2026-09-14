# Kris Pierce Toolkit: the video

Two finished cuts, both vertical 9:16, 1080 x 1920, 30fps, 34 seconds:

- `kris-pierce-toolkit-sound.mp4` has the sound design and is the one to post.
- `kris-pierce-toolkit.mp4` is the same picture with no audio, for adding a music track
  of your own.

Twelve official MasterClass Executive lab buttons pop in one at a time, each held long
enough to read, then drop into the black leather bag marked KRIS PIERCE TOOLKIT. The
bag fills up as it goes, and the dots across the top track twelve of twelve.

`poster.png` is a frame for the thumbnail.

## The sound

Two layers, both built by `build/make_audio.py` from the same timing constants as
the picture.

Sound design on top: a whoosh on each drop, a soft weighted thump on each landing,
and the twelve landings tuned to an ascending A minor pentatonic so the bag audibly
fills up as it visually does.

A quiet music bed underneath, at 120 bpm in A minor: four-on-the-floor kick, eighth-note
hats, a syncopated bass and a rolling pentatonic pluck, building through the twelve
labs. It sits about 6 dB under the landings and ducks briefly on each one so the hits
stay clear.

The ending is scored on its own. The bed drops out on the last bar line, a low swell
rises under the pull-back for three seconds, and it resolves into one held A as the
closing line lands, decaying to the end. Every hit is on its frame, the mix peaks at
-1 dBFS, and it is balanced so the landings still read on a phone speaker.

The bed is synthesised, not a licensed track, so it is deliberately understated. If you
want something with more character, mix a track under the silent cut instead; the beat
grid is below.

## What is in the cut

| Time | What happens |
|---|---|
| 0.0–4.0 | Opens on the finished frame, bag and title in place, so frame one doubles as the cover on every platform. "Twelve AI labs. One toolkit." / "What MasterClass Executive is adding to my work in rare disease, policy and HTA" |
| 4.0–28.0 | Twelve labs, two seconds each: pop in, hold with the title and LAB nn / 12, drop, land |
| 28.0–34.0 | The pull-back. The bag lifts a fraction, its reflection deepens, and the camera pulls back until it stands small under one spotlight on a stage whose floor runs to the horizon. "This is the start." in gold serif, then the eyebrow, then out. |

## Adding music

Optional. The cut runs on a 120 bpm grid with a landing on the fourth beat of every
bar, so any 120 bpm track drops straight in with no nudging. Landings are at 5.5, 7.5,
9.5, 11.5, 13.5, 15.5, 17.5, 19.5, 21.5, 23.5, 25.5 and 27.5 seconds. Pick something
driving rather than ambient. Instagram and TikTok can add a licensed track over the
sound version in-app; for LinkedIn, mix a track under `kris-pierce-toolkit.mp4` in the
edit.

Narration is optional and the twenty-second script in `voiceover.md` fits this cut.

## Rebuilding it

```bash
pip install pillow numpy            # ffmpeg must be on the path
cd build
python3 prepare_bag.py              # keys the checkerboard out of the supplied bag
python3 render.py                   # writes ../kris-pierce-toolkit.mp4, about 2.5 min
python3 render.py --stills 6.35 20  # single frames instead, for checking a change
python3 make_audio.py --mux         # builds the sound and writes ../kris-pierce-toolkit-sound.mp4
```

Set `TOOLKIT_FONT_DIR` to a folder of Inter TTFs to match the delivered cut; without it
the renderer falls back to Liberation Sans and the type will differ slightly.

Everything is driven by constants at the top of `build/render.py`: `PER_BUTTON` for
dwell time, `BPM`, the layout positions, and `LABS` for the titles and their order.
`edit-guide.md` explains how the animation is put together.

## Files

| File | What it is |
|---|---|
| `kris-pierce-toolkit-sound.mp4` | The cut with sound design, ready to post |
| `kris-pierce-toolkit.mp4` | The cut with no audio, for a music track of your own |
| `poster.png` | Thumbnail frame |
| `sequence.md` | The timeline, lab by lab |
| `edit-guide.md` | How the animation works and how to change it |
| `voiceover.md` | Narration scripts |
| `post.md` | Draft of the accompanying post |
| `assets/` | The keyed bag and where the source artwork lives |
| `prompts.md` | Unused: prompts for generating the backgrounds with a video model instead |
| `build/` | `prepare_bag.py`, `render.py` and `make_audio.py` |
