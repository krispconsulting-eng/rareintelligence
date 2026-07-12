# Automation: from purchase to certificate

The end-to-end automation, so that once a learner buys, everything from enrolment
to the certificate happens without you touching it. Built on the own-stack
architecture in `02-platform-architecture.md`: Stripe, Vercel functions,
Supabase, Kit and Resend. It reuses the Kit tagging discipline from the
`kit-lead-capture` and `funnel-tracking` skills rather than inventing a new one.

## The full lifecycle

Every stage has a trigger and an action. Nothing waits on a manual step.

| Stage | Trigger | Action |
|---|---|---|
| 1. Lead | Free intro course signup | Email captured into Kit, tagged to the intro-course funnel (per `kit-lead-capture`). |
| 2. Nurture | On the intro-course tag | Kit sequence teaches and makes the case for the first paid course. |
| 3. Purchase | Stripe Checkout completed | Webhook function fires (stage 4). |
| 4. Enrol | `checkout.session.completed` webhook | Record entitlement in Supabase; create or link the learner; tag the purchase in Kit; send a receipt via Resend. |
| 5. Onboard | Purchase tag added in Kit | Kit welcome sequence: how to log in, what to expect, where to start. |
| 6. Learn | Learner completes lessons | Progress rows written to Supabase. |
| 7. Complete | Final lesson completed | Certificate function fires (stage 8). |
| 8. Certify | Course completion | Render branded certificate to PDF; email via Resend; tag "completed [course]" in Kit. |
| 9. Continue | "completed" tag added | Kit post-course sequence: alumni, then the next course or the pathway bundle. |

## Stage 4: the purchase webhook, in detail

This is the one function that must be right, because it is where money becomes
access.

On `checkout.session.completed` from Stripe:

1. **Verify** the Stripe signature. Reject anything unsigned.
2. **Read** the product and the buyer's email from the session metadata.
3. **Upsert** the learner in Supabase (create if new, match by email if
   returning).
4. **Grant** the entitlement: insert a row in `entitlements` for the course,
   bundle, or licence, with the Stripe payment id as the source. For a bundle,
   grant every course in the program. For a licence, create the `licences` row
   with its seat count.
5. **Tag** the buyer in Kit: `purchased-[course]` (or `purchased-[bundle]`), plus
   the source tag carried through from the UTM, so attribution stays intact.
6. **Receipt** via Resend, or let Stripe send its own receipt if you prefer.
7. **Return 200** quickly. Do the slow parts (email) after acknowledging, or in a
   short queue, so Stripe does not retry.

Idempotency matters: Stripe can deliver a webhook more than once, so key the
entitlement on the Stripe payment id and ignore duplicates.

## Stage 8: the certificate, in detail

The certificate is generated from the branded HTML template defined in
`01-brand-identity.md`, so it needs no design tool and always matches the brand.

On course completion (all lessons for a course marked complete in Supabase):

1. **Assemble** the certificate data: learner name, course title, completion
   date, a unique certificate id, and the lesson's `last_reviewed` date for the
   "Content current as at" line.
2. **Render** the HTML template with that data.
3. **Convert to PDF.** Playwright is already a dependency in this repo and can
   render the HTML to a PDF in a function or a scheduled job. A lightweight
   HTML-to-PDF library is the alternative if a full browser is too heavy for the
   serverless runtime.
4. **Store** the PDF (Supabase storage, free tier) and record the certificate id
   against the learner, so it can be re-sent or verified later.
5. **Email** it via Resend with a short, plain message.
6. **Tag** "completed-[course]" in Kit to start the post-course sequence.

A certificate id that can be looked up gives you a simple verification page later
if an organisation ever wants to confirm one, without any extra system now.

## The Kit tag scheme

Keep tags consistent so segments stay clean and attribution holds, exactly as the
`funnel-tracking` skill prescribes.

- `funnel-[name]` on capture, carrying the source.
- `purchased-[course]` and `purchased-[bundle]` on payment.
- `completed-[course]` on certification.
- `alumni` once any course is completed.
- `licence-[organisation]` for team members under a licence.

Segments then fall out for free: buyers who have not started, learners stalled
mid-course, alumni who have not bought the next course, and so on. Each is a Kit
sequence you write once.

## Building it: order of work

1. **Stripe products and a single webhook function.** This alone lets you sell
   and grant access.
2. **Kit tags and the purchase and onboarding sequences.**
3. **Progress writing and the completion trigger.**
4. **The certificate function.**
5. **The post-course sequences.**

Stages 1 and 2 are the minimum to sell from launch. The certificate and
post-course automation can follow within the first courses, without holding up
the first sale.

## What needs your accounts

This is a blueprint; wiring it needs credentials you control, added as Vercel
environment variables, never committed:

- Stripe secret key and webhook signing secret.
- Supabase project URL and service key.
- Kit API key.
- Resend API key (if used).

Give the go-ahead and provide these as environment variables, and this becomes a
set of functions in the repo rather than a diagram.

## Next actions

- Approve the lifecycle and the tag scheme.
- Provide the Stripe and Kit accounts (Supabase and Resend can be created as part
  of the build).
- Confirm whether receipts come from Stripe or Resend, and whether learners get a
  material-change notice on content updates.
