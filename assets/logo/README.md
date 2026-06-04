# Rare Intelligence — Logo Suite

The complete logo package for the **Deep Signal** identity. Every file comes in **SVG**
(vector, with the Bricolage Grotesque / DM Mono fonts embedded so it renders anywhere —
no font install needed) and **PNG** (high-resolution, transparent background unless noted).

> *Rare by nature. Intelligent by design.*

## Folder structure

```
assets/logo/
├── primary/                 # The chosen mark — Option A "Deep Signal Badge"
│   ├── svg/                 # vector, font-embedded
│   └── png/                 # transparent, ~1000–1700px wide
├── options/                 # The four concept options (A–D), svg + png
├── favicon/                 # favicon.svg + 32 / 180 / 512 px (navy rounded bg)
├── mark.svg                 # badge-only mark (used as the site favicon)
└── option-*.svg             # source concept files
```

## Lockups (primary)

| File stem | Lockup | When to use |
| --- | --- | --- |
| `ri-horizontal-*` | Horizontal | **Default** — headers, documents, email signatures |
| `ri-stacked-*` | Stacked | Centred layouts, social profiles, covers |
| `ri-inline-*` | Inline | Single-line wide placements, footers, banners |
| `ri-tagline-*` | Tagline lockup | Introductions — adds “AI for Rare Disease Leaders” |
| `ri-mark-*` | Badge only | App icons, avatars, favicons, tight spaces |

## Colourways

| Suffix | Use on | Notes |
| --- | --- | --- |
| `-navy` | Dark / navy backgrounds | Full-colour badge, ghost wordmark |
| `-white` | Light / white backgrounds | Full-colour badge, navy wordmark |
| `-gradient` | The brand gradient panel | Includes gradient background (not transparent) |
| `-reversed` | Busy / single-colour / watermark | Monochrome ghost outline |
| `-colour` / `-reversed` (mark) | Badge full-colour vs mono | — |

## Favicons

- `favicon/favicon.svg` — scalable, transparent (already wired into the site `<head>`).
- `favicon/favicon-32.png` — browser tab.
- `favicon/favicon-180.png` — Apple touch icon.
- `favicon/favicon-512.png` — PWA / large.

To wire the PNG favicons, add to each page `<head>`:
```html
<link rel="apple-touch-icon" sizes="180x180" href="assets/logo/favicon/favicon-180.png" />
<link rel="icon" type="image/png" sizes="32x32" href="assets/logo/favicon/favicon-32.png" />
```

## Usage rules (from the brand guidelines)

- **Clear space:** keep space equal to half the badge diameter on every side.
- **Minimum size:** below 24px, use the **badge only** (`ri-mark-*`).
- **Don't:** recolour outside Deep Signal, stretch, rotate, add effects, or place the
  colour mark on a low-contrast background — switch colourway instead.
- The **primary** is `ri-horizontal-navy`. Reach for other lockups only when the layout
  needs them.

## Fonts

The SVGs are self-contained. To **edit** them or set new type, install the free Google
fonts: **Bricolage Grotesque** (800) for the wordmark, **DM Mono** (500) for the tagline.
