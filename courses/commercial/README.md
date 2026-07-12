# Commercial and operational blueprint

How the Rare Intelligence courses are sold and run. This is brand-agnostic:
positioning, pricing, platform, content currency and automation. It carries no
visual design. When these become real pages, build them in this repository's
brand (`assets/css/brand.css`, `WEBSITE-PLAYBOOK.md`, `HERO-GUIDE.md`).

| File | What it covers |
|---|---|
| `00-commercial-strategy.md` | Positioning, packaging, pricing, the funnel, and a staged launch. |
| `02-platform-architecture.md` | Selling and delivering on your own stack with Stripe, no paid LMS. |
| `03-content-governance.md` | The mechanism that keeps courses current as TGA, PBAC, MSAC, ACNC and policy change, with a visible currency date. |
| `04-automation-signup-to-certificate.md` | The end-to-end automation, from purchase to certificate delivery. |
| `05-design-specs.md` | The four course surfaces (catalogue, sales page, player, certificate) as a structure and accessibility reference. Reskin the tokens to this repository's brand; keep the layout and accessibility guidance. |

## The decisions already made

- **Selling from launch.** Stripe is live from day one. A short free intro course
  is the top of the funnel.
- **Own stack, no paid LMS.** Courses are sold and delivered on your own site and
  hosting. The only costs are per-sale (Stripe) and services you already run.
- **Pricing.** Free intro, a flat $145 per course, program pathways ($590
  families, $790 organisations), and a whole pack (both programs, $1,190) that is
  the only place the three bonuses live.
- **Self-paced.** The courses are self-paced. The differentiators are the depth
  of the content, the design, and that it stays current.

## Notes for this repository

- `02-platform-architecture.md` targets this repository directly: plain HTML, CSS
  and JavaScript on Vercel with `cleanUrls`, course pages as static pages under
  `/courses`, and the Stripe webhook, entitlements and certificate running as
  Vercel Serverless Functions in `/api`. No framework and no build step.
- `05-design-specs.md` describes the surfaces and the accessibility bar. Take the
  structure and the WCAG guidance; replace the colour and type tokens with this
  repository's brand.
