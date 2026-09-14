# Sequence

32 seconds at 120 bpm, where one bar is two seconds. Each lab gets one bar, so every
landing falls on a downbeat. Titles are the official lab names, taken from the supplied
artwork filenames and used verbatim, including US spellings.

| Time | Lab | Title on screen | Lands |
|---|---|---|---|
| 0.0–4.0 | | Twelve AI labs. One toolkit. | |
| 4.0–6.0 | 01 | Data Analysis with AI | 5.5 |
| 6.0–8.0 | 02 | Build Full Marketing Campaigns with AI | 7.5 |
| 8.0–10.0 | 03 | Training AI Agents | 9.5 |
| 10.0–12.0 | 04 | Financial Analysis and Modeling with AI | 11.5 |
| 12.0–14.0 | 05 | Answer Engine Optimization | 13.5 |
| 14.0–16.0 | 06 | Build Prototypes with AI | 15.5 |
| 16.0–18.0 | 07 | How AI Teams Build and Govern Agents | 17.5 |
| 18.0–20.0 | 08 | Turn Your Workflow into an AI Superpower | 19.5 |
| 20.0–22.0 | 09 | Customer Research with Synthetic Users | 21.5 |
| 22.0–24.0 | 10 | Build AI Agents for Sales and GTM | 23.5 |
| 24.0–26.0 | 11 | Storytelling and Slide Decks with AI | 25.5 |
| 26.0–28.0 | 12 | AI for Customer Support | 27.5 |
| 28.0–32.0 | | Kris Pierce Toolkit | |

Two titles are shortened on screen because the full names do not fit the dwell time:
lab 03 is *Training AI Agents: From Domain Expertise to Working Agent* and lab 05 is
*Answer Engine Optimization: AI Search Beyond SEO*. Both appear in full in `post.md`.

## Inside one bar

| Beat | Time in bar | What happens |
|---|---|---|
| 1 | 0.00 | Button pops in at the upper centre, scaling up with a slight overshoot |
| 1–2 | 0.00–0.95 | Holds still enough to read, title and LAB nn / 12 beneath it |
| 3 | 0.95–1.50 | Drops on a gravity curve, tilting, with a colour trail behind it |
| 4 | 1.50 | Lands: passes behind the bag's front panel, the bag bumps, a flare in the button's own colour bursts at the mouth, the camera kicks in |
| 4 | 1.50–2.00 | Settles. The button is now visible peeking out of the bag and its dot fills |

## Changing the pace

`PER_BUTTON` in `build/render.py` sets the dwell. At 2.0 seconds a two-line title gets
about 1.1 seconds of clear reading time. Raising it to 2.5 makes the cut 38 seconds and
is the change to make if the titles feel rushed; the beat grid then no longer lines up
with whole bars, so either accept that or use a 96 bpm track.
