# Content governance: keeping courses current

The mechanism that keeps Rare Intelligence content correct as rules and law
change. This is a real differentiator, not a footnote. Most online courses are
accurate on the day they publish and slowly rot afterwards. Rare Intelligence
courses carry a visible currency date and a process behind it, which is worth
saying plainly in the marketing because almost no one else can.

The rare disease system moves: the TGA changes pathways, the PBAC and MSAC change
processes and forms, the National Strategic Action Plan is refreshed, the ACNC
updates obligations, and the Medicines Australia Code is revised. A course that
still describes last year's process is worse than no course, because a learner
acts on it.

## The principle

The git repo is the single source of truth. Content currency is a property of the
content, tracked in the content, and surfaced to the learner. No separate system
can drift out of sync, because there is no separate system: the pages, the
certificate date, and the review process all read from the same files.

## Module frontmatter

Every lesson file carries a small block of metadata. This is the spine of the
whole mechanism.

```yaml
---
title: Access, regulation and HTA in Australia
order: 4
owner: kris
last_reviewed: 2026-07-01
next_review: 2027-01-01
regulatory_refs:
  - TGA
  - PBAC
  - MSAC
  - Medicines Australia Code
---
```

- **`last_reviewed`** is shown to the learner as "Content current as at 1 July
  2026" and is printed on the certificate.
- **`next_review`** drives the review schedule. When today passes it, the lesson
  is flagged for review.
- **`regulatory_refs`** is the link between a lesson and the external things that
  can make it wrong. When one of those bodies changes something, you can find
  every lesson that depends on it in seconds.

## The regulatory watch register

A single file, `regulatory-watch.md`, lists the external sources that can trigger
a content change, who owns watching each, and how often to check. It is the
human half of the mechanism.

| Source | What to watch | Cadence | Affects refs |
|---|---|---|---|
| TGA | Orphan drug and provisional pathways, guidance updates | Quarterly | TGA |
| PBAC | Process and consumer-input changes, guidelines | Quarterly | PBAC |
| MSAC | Process and consumer-input changes | Quarterly | MSAC |
| Department of Health | National Strategic Action Plan for Rare Diseases | Twice yearly | National Action Plan |
| ACNC | Charity obligations, governance standards | Twice yearly | ACNC |
| Medicines Australia | Code of Conduct edition changes | On release | Medicines Australia Code |
| NHMRC | Statement on Consumer and Community Involvement | Twice yearly | NHMRC CCI |

## How an update flows

1. **A change is noticed**, either at the scheduled check or because a source
   published something. Optionally, a monitor watches the key source pages and
   raises a flag automatically (see below).
2. **Find affected lessons.** Search `regulatory_refs` for the changed body. This
   returns the exact list of lessons to review, across both suites.
3. **Update the content** in the repo, a normal edit and commit.
4. **Bump `last_reviewed`** (and set the next `next_review`). This automatically
   updates the "current as at" date shown to learners and printed on future
   certificates.
5. **Push.** The affected pages redeploy. There is nothing else to synchronise.
6. **Optionally notify enrolled learners** of a material change, through a Kit
   broadcast to the relevant course segment. For a substantive legal change, this
   is a mark of quality, not a chore.

## Automating the watch (optional, still no fixed cost)

The scheduled human check is enough to launch. When you want to reduce the manual
load, a monitor can watch the source pages and raise a flag when they change,
without any subscription:

- A scheduled Vercel function (cron) fetches the key source pages and compares a
  hash or a key section against the last stored version.
- On a change, it opens a GitHub issue in this repo, tagged with the affected
  `regulatory_refs`, so the review lands in your normal workflow.
- The Firecrawl monitor tools available in this workspace can do the watching
  directly if you would rather not run the cron yourself.

Either way, the trigger is external change, the action is a review task, and the
resolution is a content edit. The loop is closed and cheap.

## The review cadence

- **Quarterly** for the regulatory bodies most likely to change process (TGA,
  PBAC, MSAC).
- **Twice yearly** for policy and governance (National Action Plan, ACNC, NHMRC).
- **On release** for the Medicines Australia Code, which changes by edition.
- **Any lesson past its `next_review`** is flagged regardless, as a backstop.

A lesson that has been reviewed and needs no change still gets its
`last_reviewed` bumped, so the currency date always reflects a genuine check.

## What the learner sees

- On every lesson and course page: "Content current as at [date]".
- On the certificate: the same date, tying the credential to a point in time.
- On a material change to a course they are enrolled in: an optional, plainly
  worded note that the content has been updated and why.

This is the honest version of "kept up to date", with the receipts to prove it.

## Next actions

- Add the frontmatter block to the lesson files as the courses are built.
- Create `regulatory-watch.md` from the register above and assign the owner.
- Decide whether to run the automated monitor now or start with the scheduled
  human check and add automation later.
