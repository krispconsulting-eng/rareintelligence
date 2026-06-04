# Rare Intelligence — Launch Plan

A project-management map to take Rare Intelligence from "site built" to "live business."

**Assumptions (edit these):**
- Runway: **~6 weeks**. Example start **Mon 8 Jun 2026** → public launch **week of 20 Jul 2026**.
- Team: **founder-led** (you), with occasional **dev** and **design/copy** help.
- Scope: marketing site + newsletter + membership (Signal Circle) + Impact Project intake.

**Owner legend:** 👤 You (founder) · 💻 Dev · 🎨 Design/Copy · 🤖 Claude (can draft/build)

**Status:** ⬜ Not started · 🟦 In progress · ✅ Done · 🔴 Blocked (needs a decision)

---

## Where we are now (baseline — done)
- ✅ 7-page responsive site (Home, About, Work With Me, Membership, Impact, Resources, Brand)
- ✅ Deep Signal brand system (`brand.css`) + in-site guidelines (`brand.html`)
- ✅ 4 logo options; **Option A** locked as primary; favicon set
- ✅ Content map + drafts (`CONTENT.md`)
- ⬜ Everything below = the path to live

---

## Timeline at a glance

```
Week 1  Foundations & decisions      ───▶ M1  Decisions locked
Week 2  Content & assets             ───▶ M2  Content complete
Week 3  Build-out & integrations     ───▶ M3  Funnels live on staging
Week 4  QA & pre-launch hardening    ───▶ M4  Launch-ready
Week 5  Soft launch (network)        ───▶ M5  Soft launch + feedback
Week 6  Public launch                ───▶ M6  🚀 Live
        Post-launch (ongoing)        ───▶ Cadence + iterate
```

---

## Phase 1 · Foundations & decisions — Week 1
**Goal:** lock every open decision so nothing blocks the build. Gate: **M1**.

| # | Task | Owner | Depends on | Est. | Status |
|---|------|-------|-----------|------|--------|
| 1.1 | Confirm founder name, positioning, one-liner | 👤 | — | 0.5d | 🔴 |
| 1.2 | Decide: Impact Project **live** vs **launching** (sets stats/tense) | 👤 | — | 0.5d | 🔴 |
| 1.3 | Lock membership tiers, prices, billing cadence | 👤 | — | 0.5d | 🔴 |
| 1.4 | Choose tech stack (see "Recommended stack" below) | 👤💻 | — | 0.5d | ⬜ |
| 1.5 | Register/confirm domain `rareintelligence.com` (+ email) | 👤 | 1.4 | 0.5d | ⬜ |
| 1.6 | Create accounts: host, email/CRM, payments, analytics, membership | 👤 | 1.4 | 1d | ⬜ |
| 1.7 | Set up brand email `hello@` / `impact@` | 👤 | 1.5 | 0.5d | ⬜ |

**M1 — Decisions locked:** name, pricing, Impact status, stack, domain, accounts all set.

---

## Phase 2 · Content & assets — Week 2
**Goal:** every 🔴 in `CONTENT.md` filled and all assets produced. Gate: **M2**.

| # | Task | Owner | Depends on | Est. | Status |
|---|------|-------|-----------|------|--------|
| 2.1 | Write real founder origin story + bio (drafts in CONTENT.md) | 👤🤖 | 1.1 | 0.5d | ⬜ |
| 2.2 | Founder headshot + any real photography | 👤🎨 | — | 0.5d | ⬜ |
| 2.3 | Collect 3+ real testimonials (with permission, names/roles) | 👤 | — | 2d | 🔴 |
| 2.4 | Finalise true stats (Home + Impact) or "launching" framing | 👤 | 1.2 | 0.5d | ⬜ |
| 2.5 | Write 4 lead-magnet files (outlines in CONTENT.md) | 👤🤖 | — | 2d | ⬜ |
| 2.6 | Confirm podcast + newsletter names/links (or hide blocks) | 👤 | — | 0.5d | ⬜ |
| 2.7 | Write newsletter welcome + free-brief auto-reply (drafts ready) | 👤🤖 | 1.6 | 0.5d | ⬜ |
| 2.8 | Proof all pages in the Deep Signal voice | 👤🤖 | 2.1–2.4 | 0.5d | ⬜ |

**M2 — Content complete:** no placeholders, no `[brackets]`, no dummy quotes left.

---

## Phase 3 · Build-out & integrations — Week 3
**Goal:** the site does real things — captures leads, takes payments, tracks visits. Gate: **M3**.

| # | Task | Owner | Depends on | Est. | Status |
|---|------|-------|-----------|------|--------|
| 3.1 | Deploy site to host + connect domain + HTTPS | 💻 | 1.5 | 0.5d | ⬜ |
| 3.2 | Wire newsletter signup → email/CRM (replace `data-stub`) | 💻 | 1.6 | 0.5d | ⬜ |
| 3.3 | Wire "free brief" + contact forms → inbox/CRM | 💻 | 1.6 | 0.5d | ⬜ |
| 3.4 | Gate lead magnets behind email capture; set download links | 💻 | 2.5, 3.2 | 0.5d | ⬜ |
| 3.5 | Stand up membership (Skool/Circle) + join flow from Membership page | 👤💻 | 1.3 | 1d | ⬜ |
| 3.6 | Connect payments (Stripe) for paid tiers | 👤💻 | 1.3 | 0.5d | ⬜ |
| 3.7 | Set booking link (Calendly) on Work With Me | 👤 | 1.6 | 0.25d | ⬜ |
| 3.8 | Add analytics (Plausible/GA4) + consent banner if needed | 💻 | 3.1 | 0.5d | ⬜ |
| 3.9 | SEO: titles, meta, OG/Twitter images, sitemap.xml, robots.txt, favicons | 💻🎨 | 3.1 | 1d | ⬜ |
| 3.10 | Email auto-responders live (welcome, brief reply) | 👤 | 2.7 | 0.5d | ⬜ |

**M3 — Funnels live on staging:** signups, payments, bookings and downloads all work end-to-end.

---

## Phase 4 · QA & pre-launch hardening — Week 4
**Goal:** it's correct, fast, accessible and legal. Gate: **M4**.

| # | Task | Owner | Depends on | Est. | Status |
|---|------|-------|-----------|------|--------|
| 4.1 | Cross-browser + device QA (Chrome, Safari, Firefox, iOS, Android) | 👤💻 | M3 | 1d | ⬜ |
| 4.2 | Link audit — kill every `#` and `mailto` placeholder | 👤 | M3 | 0.5d | ⬜ |
| 4.3 | Accessibility pass (contrast already AA; alt text, focus, headings, labels) | 💻 | M3 | 0.5d | ⬜ |
| 4.4 | Performance (Lighthouse ≥90; compress images, preload fonts) | 💻 | M3 | 0.5d | ⬜ |
| 4.5 | Forms tested: success + error + spam protection | 👤 | 3.2–3.4 | 0.5d | ⬜ |
| 4.6 | Legal: Privacy Policy, Terms, cookie/consent, medical disclaimer page | 👤 | — | 1d | 🔴 |
| 4.7 | Payment + membership end-to-end test (real card, then refund) | 👤 | 3.5, 3.6 | 0.5d | ⬜ |
| 4.8 | Backups + analytics goal/conversion tracking confirmed | 💻 | 3.8 | 0.25d | ⬜ |

**M4 — Launch-ready:** QA green, legal pages live, funnels verified with real transactions.

---

## Phase 5 · Soft launch — Week 5
**Goal:** real users, low stakes, fast feedback. Gate: **M5**.

| # | Task | Owner | Depends on | Est. | Status |
|---|------|-------|-----------|------|--------|
| 5.1 | Share with 15–25 trusted people (network, past clients, advocates) | 👤 | M4 | 0.5d | ⬜ |
| 5.2 | Seed the membership with founding members (free/discount) | 👤 | 3.5 | ongoing | ⬜ |
| 5.3 | Collect feedback (short form) + watch analytics/heatmaps | 👤 | 5.1 | 3d | ⬜ |
| 5.4 | Fix top issues; tighten the highest-drop funnel step | 👤💻🤖 | 5.3 | 1d | ⬜ |
| 5.5 | Prep launch assets: announcement post, email, 3–5 social tiles | 👤🎨🤖 | M4 | 1d | ⬜ |

**M5 — Soft launch done:** feedback incorporated, funnels converting, launch assets ready.

---

## Phase 6 · Public launch — Week 6
**Goal:** go loud. Gate: **M6 🚀**.

| # | Task | Owner | Depends on | Est. | Status |
|---|------|-------|-----------|------|--------|
| 6.1 | Publish launch announcement (LinkedIn + Instagram) | 👤 | 5.5 | 0.5d | ⬜ |
| 6.2 | Send launch email to full list | 👤 | 5.5 | 0.5d | ⬜ |
| 6.3 | Podcast / partner / community shout-outs | 👤 | 5.5 | 0.5d | ⬜ |
| 6.4 | Monitor: uptime, forms, payments, replies — same-day response | 👤 | 6.1 | ongoing | ⬜ |
| 6.5 | Thank founding members; capture first launch testimonials | 👤 | 6.1 | ongoing | ⬜ |

**M6 — 🚀 Live:** site public, announced across channels, monitored, first signups in.

---

## Launch day (T-0) checklist
- [ ] DNS/HTTPS green; site loads on a fresh device + incognito
- [ ] All nav links + CTAs go somewhere real (no `#`)
- [ ] Newsletter, brief, contact forms submit → land in inbox/CRM
- [ ] Buy a paid tier with a real card → access granted → refund tested
- [ ] Booking link opens correct calendar
- [ ] Analytics recording; conversion goals firing
- [ ] OG image + title preview correct when pasted into LinkedIn/Slack
- [ ] Mobile pass on a real phone
- [ ] Legal pages reachable from footer
- [ ] Announcement post + email scheduled/sent

---

## Post-launch (ongoing)
- **Content cadence:** newsletter every 2 weeks; 1 resource/month; podcast if live.
- **Membership:** weekly community presence, monthly workshop + office hours.
- **Iterate:** monthly review of analytics → fix the weakest funnel step.
- **Impact Project:** open intake, publish first community story when ready.

---

## Recommended stack (static site, low-ops, founder-friendly)
| Need | Recommendation | Why |
|------|----------------|-----|
| Hosting | **Cloudflare Pages / Netlify / Vercel** | Free tier, instant deploys from this Git repo, HTTPS |
| Forms | **Netlify Forms / Formspree** | No backend; drops into the existing `data-stub` forms |
| Email/Newsletter | **MailerLite / ConvertKit** | Automations for welcome + lead-magnet delivery |
| Membership/Community | **Skool** (per brand doc) or Circle | Community + courses + payments in one |
| Payments | **Stripe** | Standard, integrates with Skool/Circle |
| Booking | **Calendly / SavvyCal** | Discovery calls |
| Analytics | **Plausible** (privacy-first) or GA4 | Lightweight, fewer consent headaches |
| Domain/email | **Cloudflare/registrar + Google Workspace** | `hello@rareintelligence.com` |

---

## Top risks & mitigations
| Risk | Mitigation |
|------|-----------|
| Content slips (testimonials, bio) blocks launch | Phase 2 front-loaded; use "launching" framing + ungated resources if needed |
| Medical-advice liability | Disclaimer on every page (done) + dedicated legal pages in 4.6; never give individual medical advice |
| Membership empty at launch | Seed founding members in 5.2 before going public |
| Solo bandwidth | 🤖 Claude drafts copy/lead magnets/build tasks; keep Week 6 light on net-new work |
| Scope creep | Anything not on this map → "v1.1 backlog," not a launch blocker |

---

*Tip: this is a living doc. Tick boxes as you go, and move anything non-essential to a
"v1.1 backlog" section at the bottom so launch stays on schedule.*
