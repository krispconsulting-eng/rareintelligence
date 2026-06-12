# Hero Draft — Step‑by‑Step Guide

How to take the **Deep Signal home hero** from the current draft to launch.
The draft lives on branch `claude/practical-archimedes-r9g8ol` and exists in two forms:

| Form | File(s) | Use it when… |
| --- | --- | --- |
| **Static site** (live home page) | `index.html` + `assets/css/styles.css` | You're shipping this repo as‑is (Vercel, no build step) |
| **React component** | `RareIntelligenceHero.jsx` | You later move to a React/Next/Vite app |

Both are the same design and stay in sync. Until the mascot art exists, the
hero shows the signature ring with a quiet teal core — no broken‑image box.

---

## Step 1 · Run the draft locally

```bash
git fetch origin claude/practical-archimedes-r9g8ol
git checkout claude/practical-archimedes-r9g8ol
python3 -m http.server 8000      # → http://localhost:8000
```

No build step. Edit, save, refresh.

> The four brand fonts load from Google Fonts, so the page needs internet
> access to look right. Offline you'll see fallback system type — don't
> judge the design from that.

## Step 2 · Generate the mascot art

Use the two prompts from the build brief (§3) in your image tool of choice
(Midjourney, DALL·E, Imagen, etc.):

1. **Hero zebra** — cute 3D Pixar‑style zebra, round glasses, cool palette
   only (indigo/cobalt/ocean/teal — **no warm tones**), transparent PNG,
   portrait 3:4, **~1200 px tall**.
2. **Badge head** — minimal flat‑3D zebra head, indigo→teal gradient disc,
   thin teal ring, transparent PNG, square, **512 px**.

Quality bar before you accept a render: clean alpha edges, no ground shadow,
no warm rim light, stripes present but not high‑contrast dominant, reads
friendly at 50 % zoom.

## Step 3 · Drop the art in

| File | Static site | React app |
| --- | --- | --- |
| Hero zebra | `mascot.png` in the **repo root** | `/public/mascot.png` |
| Badge head | *(not used — header keeps the RI monogram mark)* | `/public/favicon.png` |

On Vercel the repo root *is* the public root, so one `mascot.png` at root
serves both worlds. Reload — the zebra appears inside the ring and starts
its slow drift in and out of focus.

> Per Brand Guidelines §02 the **official favicon stays the RI monogram**
> (`assets/logo/favicon/…`, already wired in `index.html`). The zebra badge
> is a playful avatar/app‑tile mark only.

## Step 4 · Verify the brand rules

Run through this in Chrome DevTools:

- [ ] **Fonts load** — Network tab → filter `fonts.g` → four families, 200s.
- [ ] **One teal action per view** — the only filled‑teal element above the
      fold is the "See how it works" button. (Headline *Rare* and ring dots
      are accents, not actions.)
- [ ] **Gradient is band‑only** — midnight‑navy floor is visible around the
      rounded band; the page background never becomes the gradient.
- [ ] **Zebra texture is felt, not seen** — faint 35° diagonal inside the
      band only; if you notice it immediately, it's too strong.
- [ ] **Reduced motion** — DevTools → Rendering → *Emulate CSS
      prefers‑reduced‑motion: reduce* → mascot stops drifting and stays sharp.
- [ ] **Mobile stacking** — device toolbar at 390 px → copy first, mascot +
      ring below, nothing clipped.
- [ ] **Only the zebra blurs** — watch one 5 s loop; ring dots stay crisp.

## Step 5 · Tune the design (knobs)

All in `assets/css/styles.css` (mirror any change in the `.jsx` to stay in sync):

| What | Where | Current | Notes |
| --- | --- | --- | --- |
| Drift speed | `@keyframes ri-drift` / `.hero-mascot` | `5s` | 6–7 s feels calmer |
| Max blur | `@keyframes ri-drift` 50 % frame | `6px` | 4 px is subtler |
| Float height / breathing | same frame | `-12px` / `scale(1.04)` | |
| Veil darkness over copy | `.hero-band::before` linear‑gradient | `.90 / .66 / .30` | lower = more gradient shows |
| Teal bloom behind mascot | `.hero-band::before` radial‑gradient | `0.14` | |
| Stripe visibility | `.hero-band::after` opacity | `.9` of an ~8 % stripe | keep ≤ 20 % effective |
| Ring dot size | inline SVG in `index.html` | `r=10` (companions `6`) | |
| Mascot size in ring | `.hero-mascot-slot` width | `53%` | |
| Band height | `.hero-band-inner` min-height | `min(620px, 100vh−240px)` | |

## Step 6 · Ship

1. Open a PR from `claude/practical-archimedes-r9g8ol` → `main` and review
   the diff (3 files + this guide).
2. Merge — Vercel deploys the static site automatically.
3. After deploy, re‑run Step 4 against the live URL once.

---

### Appendix · Using the React component

`RareIntelligenceHero.jsx` is self‑contained (fonts via `<link>`, keyframes
inline). Drop it into any React project with Tailwind ≥ 3 configured:

```jsx
import RareIntelligenceHero from "./RareIntelligenceHero";
export default function Home() {
  return <RareIntelligenceHero />;
}
```

Art goes in `/public/mascot.png` and `/public/favicon.png`. Tailwind must
scan the file (add it to `content` in `tailwind.config.js`) because the
component uses arbitrary‑value classes like `bg-[#00C9B1]`.
