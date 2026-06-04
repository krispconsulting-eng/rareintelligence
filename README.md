# Rare Intelligence — Website & Brand

A polished, responsive marketing site for **Rare Intelligence** — AI for rare-disease
leaders, built on AI, clinical evidence and lived experience.

> *Rare by nature. Intelligent by design.*

The visual system is the **"Deep Signal"** identity defined in the official
*Rare Intelligence · Brand Guidelines v1.0* (KrispConsulting, 2026): a disciplined
cool-blue palette, no warm hues, a single vivid-teal accent, and a faint zebra texture
(the universal symbol of rare disease).

## Pages

| File | Page |
| --- | --- |
| `index.html` | Home |
| `about.html` | About — story, mission, the SIGNAL Method™, values |
| `work-with-me.html` | Work With Me — advisory / AI builds / speaking |
| `membership.html` | Membership — the Signal Circle, pricing tiers |
| `impact.html` | Impact Project — pro-bono intelligence |
| `resources.html` | Resources — guides, podcast, newsletter |
| `brand.html` | **Brand guidelines** — Deep Signal reference, in-site |
| `logo-options.html` | The four logo options, side by side |

## Brand system (Deep Signal)

Tokens live in `assets/css/brand.css` (single source of truth); components in
`assets/css/styles.css`.

- **Colour** — Midnight Navy `#080F1E` base → Deep Indigo `#2D3580` → Cobalt `#1A4FBF`
  → Ocean `#0E7FA8` → **Vivid Teal `#00C9B1`** (the one accent). Ghost `#EEF8F7` text,
  Warm Grey `#8BA8A5` muted. No warm hues — restraint is the brand.
- **Gradient** — indigo → cobalt → ocean → teal, used as *punctuation only* (bands,
  headers, footers), never full-page wallpaper.
- **Type** — Bricolage Grotesque (800, wordmark/headlines), Instrument Sans (body/UI),
  Lora Italic (taglines & quotes only), DM Mono (eyebrows/stats/captions).
- **Texture** — the zebra: a 35° diagonal stripe at 10–20% opacity, felt not seen.
- **Voice** — a trusted colleague, not a guru: direct, specific, grounded, anti-hype.

## Logo

Four options were designed, all on the Deep Signal palette (see `logo-options.html`):

| | Option | Idea |
| --- | --- | --- |
| **A** | `option-a-badge.svg` | The Deep Signal Badge — canonical gradient disc + teal ring + zebra (**primary**) |
| **B** | `option-b-signal-ring.svg` | The Signature Ring — dots cycling the family around the monogram |
| **C** | `option-c-zebra-cut.svg` | Zebra Cut — modern squircle, visible zebra, gradient RI |
| **D** | `option-d-pulse.svg` | Pulse → Signal — heartbeat rising into intelligence bars |

`assets/logo/mark.svg` is the badge-only mark (favicon / avatar). Option A is currently
wired in as the site's primary; swap freely once a direction is chosen.

## Structure

```
.
├── index.html · about.html · work-with-me.html · membership.html
├── impact.html · resources.html · brand.html · logo-options.html
├── assets/
│   ├── css/brand.css      # Deep Signal tokens
│   ├── css/styles.css     # components & layout
│   ├── js/main.js         # nav, scroll-reveal, form stubs
│   └── logo/              # 4 logo options + mark
└── README.md
```

## Running locally

No build step. Open `index.html`, or:

```bash
python3 -m http.server 8000   # → http://localhost:8000
```

## Placeholders to replace before launch

- Founder name/bio and photography (currently gradient placeholders).
- Statistics on Home & Impact (illustrative).
- Contact addresses, social links, podcast links.
- Form submissions are front-end stubs (`data-stub` in `main.js`) — wire to a real provider.

Copy throughout notes that content is educational and **not medical advice**.
