# Platform architecture

How Rare Intelligence is sold and delivered on your own stack, with Stripe live
from launch and no paid LMS. This fits the site you already have: a multi-page
Vite and React build on Vercel, with serverless functions (the pattern already
used in `engagement-platform/api/`).

## Principle

Own the stack, pay only per sale. Every fixed-cost service is avoided or kept on
a free tier. The only money that moves before you have revenue is nothing; the
only money that moves after is Stripe's per-transaction fee. Everything else is
either already paid for (Vercel, Kit) or free at this scale.

## The stack

| Layer | Tool | Cost | Why |
|---|---|---|---|
| Hosting and pages | Vercel (existing) | Already paid | Your site already lives here. |
| Course pages | Vite multi-page build, content from this repo | $0 | Same build you use now; courses are new entries. |
| Payments | Stripe (Checkout + webhooks) | Per sale only (about 1.75% + 30c AU domestic) | No monthly fee. Hosted checkout, so no card data touches your servers. |
| Accounts and data | Supabase (free tier) | $0 at launch scale | Postgres, plus passwordless magic-link auth, in one. Removes most custom auth code. |
| Marketing email and list | Kit (existing) | Already paid | List, tags, funnels, per the `kit-lead-capture` and `funnel-tracking` skills. |
| Transactional email | Resend (free tier, 3,000/month) | $0 at launch scale | Receipts and the certificate email. Kit can also do this if you prefer one tool. |
| Analytics | Vercel Web Analytics (existing) | Already paid | Custom events per the `funnel-tracking` skill. |

Supabase and Resend are the only new accounts, both free at this scale. If you
would rather stay entirely in-platform, Vercel Postgres and Vercel KV can replace
Supabase, at the cost of writing the magic-link auth yourself. The recommendation
is Supabase, because auth-plus-database in one saves the most build.

## How the pieces fit

```
                 krispierce.com.au/learn  (Vite multi-page, on Vercel)
                 ┌───────────────────────────────────────────────┐
   visitor  ──▶  │  catalogue  ─▶  course sales page  ─▶  checkout │
                 └───────────────────────────────────────────────┘
                                        │  Stripe Checkout (hosted)
                                        ▼
                              Stripe  ──webhook──▶  /api/stripe-webhook  (Vercel function)
                                                          │
                          ┌───────────────────────────────┼───────────────────────────┐
                          ▼                                ▼                           ▼
                  Supabase: record                Kit: tag purchase,           Resend: receipt
                  entitlement + create            start onboarding
                  or link account                 sequence
                                        │
   learner  ──magic link login──▶  course player (gated pages)  ──progress──▶  Supabase
                                        │
                                  on completion
                                        ▼
                          /api/issue-certificate (Vercel function)
                          renders branded HTML ─▶ PDF ─▶ Resend emails it
                          ─▶ Kit tags "completed" ─▶ post-course sequence
```

## The data model

Small and boring on purpose. Three tables in Supabase.

- **`learners`**: id, email, name, created_at. One row per person. Auth is
  Supabase magic link, so there are no passwords to store.
- **`entitlements`**: id, learner_id, product (course or bundle or licence),
  source (Stripe payment id), granted_at, expires_at (null for lifetime). This is
  the single source of truth for "can this person see this course".
- **`progress`**: id, learner_id, course, lesson, completed_at. One row per
  completed lesson. Course completion is derived: all lessons complete.

Organisation licences add one table, **`licences`** (id, organisation, seats,
purchased_by, seats_used), and seats issue entitlements as members join.

## Access control

The courses are paid, so pages must be gated. On a static site this is done with
a thin serverless check, not by hiding markup in the browser.

1. A learner logs in with a magic link (Supabase Auth emails a one-time link; no
   password).
2. Their session is a signed token in a cookie.
3. Course lesson content is served through a function (or a lightweight
   client fetch to `/api/lesson`) that checks the session and the entitlement
   before returning the lesson body. No entitlement, no content.
4. Sales pages, the catalogue, and the free intro course are fully public and
   static, so the marketing surface stays fast and indexable.

The free intro course needs no gate at all; it is static and public, which is
part of why it makes such a good front door.

## Selling: two build depths

You can start selling with almost no code, then deepen.

**MVP (fastest to first sale):**

- Stripe **Payment Links** for each product (created in the Stripe dashboard, no
  code).
- The sales page links to the Payment Link.
- A single Stripe **webhook** function records the entitlement in Supabase and
  tags the buyer in Kit.
- Course content delivered on gated pages as above.

This is enough to sell and deliver from day one.

**Full (when volume justifies it):**

- Replace Payment Links with Stripe **Checkout Sessions** created by a function,
  so you can pass metadata, support the organisation licence and seat counts, and
  handle discounts and concessions cleanly.
- Add the certificate and post-course automation in
  `04-automation-signup-to-certificate.md`.

## Course content pipeline

The content already lives in this repo as markdown. The build renders it to
pages; the git repo stays the single source of truth, which is what makes the
content-governance mechanism in `03-content-governance.md` work.

- Each course is a folder of lesson markdown files with frontmatter (title,
  order, `last_reviewed`, `next_review`, `regulatory_refs`).
- The Vite build turns each lesson into a page in the `/learn` section, applying
  the Rare Intelligence design (see `05-design-specs.md`).
- Updating content is a normal edit-and-commit. A push redeploys the affected
  pages. There is no separate CMS to keep in sync, and no LMS content to
  re-upload.

## What this costs to run

- Before any sale: nothing beyond what you already pay for Vercel and Kit.
- Per sale: Stripe's fee only.
- At launch volume: Supabase and Resend stay within free tiers. If the course
  ever outgrows them, that is a revenue problem worth having, and the paid tiers
  are modest.

## Next actions

- Create the Stripe account and the products and Payment Links from
  `00-commercial-strategy.md`.
- Create a Supabase project (free tier) and the three tables above.
- Create a Resend account (free tier) or decide to send transactional email
  through Kit.
- Give the go-ahead to scaffold the `/learn` section, the webhook function, and
  the gated course player in the repo.
