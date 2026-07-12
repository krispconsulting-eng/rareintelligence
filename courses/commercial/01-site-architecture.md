# Site architecture

How the `/courses` section is laid out, page by page, so it does one job: turn a
visitor into a learner, then a learner into a repeat buyer. This is the page map
and the funnel. The pricing and offers behind it are in
`00-commercial-strategy.md`; how the pages are built and gated is in
`02-platform-architecture.md`; how each surface looks is in `05-design-specs.md`.

## The premise, in one line

The section exists to turn a visitor into a learner, and then a learner into a
repeat buyer. Every page has one job and hands the visitor to the next.

## The page map

All pages sit under `/courses` and resolve through Vercel `cleanUrls`, so the URL
has no `.html`. Public and static unless marked gated.

```
/courses                                   catalogue — the shelf; route to the right course
├── /courses/[course]                       sales page — make the case for one course
│   └── /courses/[course]/[lesson]  (gated)  player — deliver the lesson to a paid learner
├── /courses/free-downloads                  free library — useful assets, gated by email only
├── /courses/webinars           (reserved)   hold page — register interest, live sessions later
└── certificate                 (issued)     proof of completion, emailed on finish
```

| Page | Path | Its one job |
|---|---|---|
| Catalogue | `/courses` | Make the two programs legible at a glance and route the visitor to the right course. |
| Course sales page | `/courses/[course]` | Make the case for one course and take the sale. One page per course; the same template throughout. |
| Course player | `/courses/[course]/[lesson]` | Deliver the lesson to a paid learner. Gated. Calm, no upsells. |
| Free downloads | `/courses/free-downloads` | Give away genuinely useful assets in exchange for an email, and warm the reader toward the free intro. |
| Webinars | `/courses/webinars` | Hold the space. Capture register-interest emails now; host live sessions later. Reserved. |
| Certificate | issued on completion | Prove the course, or the whole pack, was finished, with the "current as at" date. |

The free intro course, "Understanding the rare disease system," is public and
static end to end: its sales page is `/courses/course-understanding-the-system`
and it is the template every other sales page follows.

## Navigation

- **Top nav.** "Courses" sits in the site's top navigation, alongside the rest of
  the site. The free intro is the standing top-nav call to action, labelled
  **Start free**. It is the one CTA that never changes, because the free course is
  always the front door.
- **Section sub-nav.** Inside `/courses`, a light sub-nav carries the three public
  destinations: **Catalogue · Free downloads · Webinars**. Sales pages and the
  gated player do not add nav items; a learner reaches them from the catalogue or
  from a link, and the player keeps its own lesson list instead.

## The funnel

Each stage hands off to the next. Nothing is skipped and nothing is over-promised.

| Stage | Where it lives | What it does |
|---|---|---|
| Top of funnel | Free downloads (email) + free intro course | Capture the email into Kit; teach enough to earn trust. |
| Middle | A single course, flat $145 | The first paid step and the impulse buy. |
| Deepen | A pathway — $590 families and advocates, $790 organisations | The committed learner buys their whole side of the catalogue. |
| Best value | The whole pack, $1,190 | Both programs at the best per-course price, and the only place the three bonuses live. |

The hand-offs, plainly:

1. **Free downloads → free intro.** A reader takes a template or checklist, joins
   the list, and the download page points them at the free intro course as the
   next honest step.
2. **Free intro → single course.** The intro orients the learner and shows what
   Course 2 unlocks. Its completion is the best possible lead for the first paid
   course.
3. **Single course → pathway.** The sales page and the post-course email offer the
   rest of that program at a saving over buying course by course.
4. **Pathway → whole pack.** At $1,190 the whole pack is cheaper than both
   pathways bought separately, and it is the only way to get the bonuses, so the
   person who wanted more than one program is nudged all the way up.

The catalogue's bundle callouts and each sales page's final CTA panel are where
these hand-offs are made visible. Nurture between them runs in Kit, per
`00-commercial-strategy.md`.

## Free downloads

Genuinely useful assets, given away and gated only by an email address. Not
teasers: templates, checklists and primers a family or organisation can use the
same day. They feed the marketing list in Kit and warm the reader toward the free
intro course.

Example assets:

- A consumer-input template for a PBAC or MSAC submission.
- A "newly diagnosed" orientation checklist for families.
- A governance and constitution starter for a small organisation.
- A one-page primer on how the Australian rare disease system fits together.
- A grant-application skeleton.

Each download captures the email into Kit, tagged to the downloads funnel, and the
page closes by pointing the reader at the free intro course. The toolkit that
ships with the whole pack is a deeper, paid relative of these; the free downloads
are the taste, not the toolkit.

## Webinars — reserved space

Built on purpose, on hold on purpose. The page exists so the nav is honest and the
plan is visible, but it promises nothing that is not ready. It reads as "coming
soon" and does one active thing now: captures register-interest emails into Kit.

Later, it hosts live sessions, and their recordings are added to the library so
the value compounds. Until then it is a placeholder that keeps the sub-nav
complete without over-promising. It is the honest opposite of announcing a webinar
series before there is one.

## How this maps to the other docs

| Doc | What it settles |
|---|---|
| `00-commercial-strategy.md` | The offers, pricing and funnel this architecture arranges into pages. |
| `02-platform-architecture.md` | How these pages are built and gated on the real stack: static HTML on Vercel, Stripe, Supabase, the `/api` functions. |
| `03-content-governance.md` | How each page's "current as at" date stays true as the rules change. |
| `04-automation-signup-to-certificate.md` | What happens after the buy button: enrolment, delivery and the certificate. |
| `05-design-specs.md` | How each surface here — catalogue, sales page, player, certificate — is designed. |

## Build order

Ship the selling surfaces first, then delivery, then the reserved space.

1. **Catalogue, the free intro sales page, and free downloads.** The public front
   of the section: something to see, something to buy toward, and a reason to join
   the list. Start building the list from day one.
2. **Paid sales pages and checkout.** The rest of the sales pages on the intro
   template, wired to Stripe, so the first paid course can be sold and the funnel
   is complete end to end.
3. **Player and certificate.** The gated delivery surface and the completion
   proof, so a paid learner can finish a course and receive their certificate.
4. **Webinars go live.** Turn the reserved page into real live sessions once demand
   is proven, and add the recordings to the library.
