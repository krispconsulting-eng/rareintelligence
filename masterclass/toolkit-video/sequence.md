# Sequence

28 seconds at 120 bpm. A new button every 1.5 seconds, three beats, with every landing
on a beat. The next button pops in at the moment the last one lands, so the settle after
a landing plays under the next hold. The ending takes three bars. Titles are the
official lab names, taken from the supplied artwork filenames and used verbatim,
including US spellings.

| Time | Lab | Title on screen | Lands |
|---|---|---|---|
| 0.0–4.0 | | Twelve AI labs. One toolkit. | |
| 4.0–5.5 | 01 | Data Analysis with AI | 5.5 |
| 5.5–7.0 | 02 | Build Full Marketing Campaigns with AI | 7.0 |
| 7.0–8.5 | 03 | Training AI Agents | 8.5 |
| 8.5–10.0 | 04 | Financial Analysis and Modeling with AI | 10.0 |
| 10.0–11.5 | 05 | Answer Engine Optimization | 11.5 |
| 11.5–13.0 | 06 | Build Prototypes with AI | 13.0 |
| 13.0–14.5 | 07 | How AI Teams Build and Govern Agents | 14.5 |
| 14.5–16.0 | 08 | Turn Your Workflow into an AI Superpower | 16.0 |
| 16.0–17.5 | 09 | Customer Research with Synthetic Users | 17.5 |
| 17.5–19.0 | 10 | Build AI Agents for Sales and GTM | 19.0 |
| 19.0–20.5 | 11 | Storytelling and Slide Decks with AI | 20.5 |
| 20.5–22.0 | 12 | AI for Customer Support | 22.0 |
| 22.0–22.9 | | The bag lifts a fraction; its reflection deepens on the floor; the dots and eyebrow fade | |
| 22.7–26.2 | | The pull-back: the stage floor fades in and the bag shrinks to a third, standing under one spotlight | |
| 25.0–28.0 | | "This is the start." rises in at 25.0; the eyebrow beneath it at 26.4; fade to black from 27.0 | |

Two titles are shortened on screen because the full names do not fit the dwell time:
lab 03 is *Training AI Agents: From Domain Expertise to Working Agent* and lab 05 is
*Answer Engine Optimization: AI Search Beyond SEO*. Both appear in full in `post.md`.

## Inside one button

| Time | What happens |
|---|---|
| 0.00 | Pops in at the upper centre, scaling up with a slight overshoot |
| 0.00–1.10 | Holds still enough to read, title and LAB nn / 12 beneath it |
| 1.10–1.50 | Drops in four tenths of a second, gathering speed then easing off into the bag, tilting slightly, with a faint colour trail |
| 1.50 | Lands: passes behind the bag's front panel, and the next button pops in at the same moment |
| 1.50–2.00 | Under the next button's hold: the bag gives a little and settles, a flare in the landed button's colour blooms at the mouth, its dot fills, and it peeks out of the bag |

## Changing the pace

`PER_BUTTON` in `build/render.py` is the gap between one button popping in and the
next, currently 1.5 seconds, equal to `IMPACT`. Raising it to 2.0 puts half a second
of clear air after each landing and makes the cut 34 seconds. Reading time is set
separately by `DROP_START`: at 1.10 a two-line title gets about a second of clear
reading; raise it and `IMPACT` together to hold longer.
