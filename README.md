# Rare Intelligence — Website

A polished, responsive marketing site for **Rare Intelligence**, a brand that blends
AI, clinical evidence and lived experience to deliver smarter answers to the rare
disease community.

The structure and tone are modelled on the energy of [wrightmode.com](https://www.wrightmode.com/)
(AI-first, human, jargon-free, community-driven) and adapted for a rare-disease
intelligence business.

> **Note on the brief:** the original design share link
> (`api.anthropic.com/v1/design/h/…/Guidelines.html`) returned a hard `404 Not Found`
> at build time — the link had expired/was invalid, so its `Guidelines.html` could not
> be read. The design system below was created fresh, using Wright Mode as the
> reference. Swap in real guidelines/assets when available.

## Pages

| File | Page | Purpose |
| --- | --- | --- |
| `index.html` | Home | Hero, stats, what-we-do, approach, pathways, CTA |
| `about.html` | About | Story, mission, the SIGNAL Method™, values |
| `work-with-me.html` | Work With Me | Advisory / AI builds / speaking, process, contact |
| `membership.html` | Membership | The Signal Circle — benefits, pricing tiers, FAQ |
| `impact.html` | Impact Project | Pro-bono intelligence for under-resourced communities |
| `resources.html` | Resources | Guides, prompt packs, podcast, newsletter |

## Design system

Defined as CSS custom properties in `assets/css/styles.css`.

- **Colours** — deep aubergine ink `#221733`, electric violet `#6B4EFF` (AI/intelligence),
  warm coral `#FF6B5C` (energy/CTA), gold `#F4B860`, teal-mint `#19C3A4` (data/signal),
  cream `#FAF6F0` background.
- **Type** — `Fraunces` (display serif, characterful) for headings, `Plus Jakarta Sans`
  for body, loaded from Google Fonts.
- **Components** — pill buttons, soft cards, numbered method steps, pricing tiers,
  resource rows, gradient CTA banners, sticky blurred header, dark footer.
- **Motion** — scroll-reveal via `IntersectionObserver`; respects
  `prefers-reduced-motion`.
- **Responsive** — fluid type (`clamp`), grid breakpoints at 940px and 720px, and an
  accessible mobile nav toggle.

## Structure

```
.
├── index.html
├── about.html
├── work-with-me.html
├── membership.html
├── impact.html
├── resources.html
├── assets/
│   ├── css/styles.css
│   └── js/main.js
└── README.md
```

## Running locally

No build step — it's static HTML/CSS/JS. Either open `index.html` directly, or serve it:

```bash
python3 -m http.server 8000
# then visit http://localhost:8000
```

## Placeholders to replace before launch

- Founder name/bio and real photography (currently gradient placeholders).
- Statistics on the home and Impact pages (illustrative).
- Contact addresses (`hello@`, `impact@rareintelligence.com`), social links, podcast links.
- Form submissions are front-end stubs (`data-stub` in `main.js`) — wire to a real
  email/CRM provider.

## Disclaimer

Copy throughout makes clear the content is educational and **not medical advice**.
