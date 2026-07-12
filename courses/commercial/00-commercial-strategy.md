# Commercial strategy

How Rare Intelligence is positioned, packaged, priced and sold from your own
site. The premise: sell from launch, on your own stack, with no fixed platform
cost.

## Positioning

Rare Intelligence sells one thing: the ability to act inside the systems that
decide rare disease outcomes. Not awareness, not inspiration, capability. A
family finishes able to navigate a diagnosis and a system. An advocate finishes
able to sit at a research, regulatory or reimbursement table. An organisation
finishes able to govern, fund and grow.

The register is the same as the consulting practice: peer to peer, direct,
outcome-first. The marketing does not sell hope or urgency. It states plainly
what a learner will be able to do, and lets that be the reason to buy. This is
the opposite of the course-launch playbook of countdowns and manufactured
scarcity, and that difference is itself a signal of quality.

The one-line promise:

> Learn the systems that decide rare disease outcomes, from someone who has sat
> on both sides of them.

## What makes it worth paying for

Three things, none of which is a gimmick:

1. **Depth and accuracy.** The content is built from the major international
   patient-training programs and anchored to the Australian system. It is
   correct, current, and specific, not a generic overview.
2. **Lived and professional credibility together.** Kris has been a carer in
   rare disease for two decades and has held senior advisory roles in HTA,
   genomics and consumer engagement. Very few people can teach both the
   experience and the machinery. That is the moat.
3. **It stays current.** Rules change; the courses change with them, with a
   visible "current as at" date on every module. Most online courses rot the day
   they are published. This one does not (see `03-content-governance.md`).

## The catalogue and packaging

The two suites are the launch catalogue. They package four ways, so a learner
can buy small, buy a pathway, buy the whole pack, or license for a team.

### 1. Single course (self-paced)

Any one course, bought on its own. The entry point and the impulse purchase.

### 2. Pathway (a full program)

All courses in one program, families and advocates or organisations, at a
discount to buying them singly. The main offer for a committed learner who wants
their side of the catalogue.

### 3. The whole pack (both programs, plus the bonuses)

Every course in both programs, at the best per-course price, and the only place
the bonuses live: the **Working with Industry** course, the **toolkit** of
templates, and the **Rare Intelligence Practitioner credential**. This is the
top of the ladder and the aspirational buy. Buying the whole pack is also cheaper
than buying both pathways separately, so it is the natural upsell for anyone who
wanted more than one program.

### 4. Organisation licence (team seats)

A block of seats for an organisation's staff and volunteers, sold to the
organisations suite in particular. The highest-value line, and the one most
likely to be grant-funded on the buyer's side.

### Recommended free entry course

Course 1 of the families-and-advocates suite, "Understanding the rare disease
system," is recommended as a **free** short intro. It is the natural top of the
funnel: the people who most need orientation are the least able to pay for it,
giving it away builds the list and the goodwill, and it is the honest lead into
everything paid. Selling starts at Course 2 and across the organisations suite.
This is a recommendation, not a lock; you can price it if you prefer.

## Pricing

A simple, flat structure for the Australian market, in AUD, GST-inclusive. These
are defensible opening numbers, not fixed; test and adjust. The model is
deliberately easy to say in one line: the intro is free, every course is $145,
a program pathway saves you money, and the whole pack unlocks the bonuses.

| Line | Price (AUD) | Notes |
|---|---|---|
| Free intro course | 0 | Understanding the Rare Disease System. The front door and list builder. |
| Any single course | 145 | Flat, either program. Self-paced, lifetime access. |
| Families and advocates pathway | 590 | All six families courses. Lifetime access. |
| Organisations pathway | 790 | All seven organisations courses. Lifetime access. |
| The whole pack (both programs) | 1,190 | Every course in both programs, and the only place the bonuses live. Cheaper than the two pathways bought separately. |
| Organisation licence | 2,400 | Up to 10 seats across the organisations courses. |
| Live cohort intake (optional) | +300 per person | Facilitated version with live sessions, capped, run in intakes. |

### The bonuses (whole pack only)

The bonuses are the reason to buy the whole pack rather than one pathway. They
are not sold separately and do not come with a single pathway; the whole pack is
the only way to get them.

- **Working with Industry, inside the Code.** A full course on partnering with
  pharma and medtech authentically, within the Medicines Australia Code of
  Conduct. Worth $145 on its own terms; only available here.
- **The toolkit.** The templates and worked examples that turn learning into
  doing: a consumer-input template for PBAC and MSAC, a governance and
  constitution starter, a grant-application skeleton, and a submission template.
- **The Rare Intelligence Practitioner credential.** A completion certificate for
  the full pack, not just a single course, with the "content current as at" date.
  The credential that says someone did the whole thing.

Notes on the logic:

- **Flat $145 is the whole story.** One price for every course keeps the offer
  legible and removes the friction of working out what a given course "should"
  cost.
- **The whole pack is where the bonuses live.** A single pathway is a good buy;
  the whole pack is the aspirational one, because it is the only way to unlock
  the industry course, the toolkit and the practitioner credential. At $1,190 it
  is also cheaper than buying both pathways separately ($1,380), so the person
  who was going to buy both is nudged all the way up.
- **The org licence is the revenue line.** One licence is worth several
  pathways, and organisations can fund it from grants or program budgets. Sell it
  actively.
- **The live cohort is a premium, not the default.** Self-paced is the product.
  A facilitated intake, run a few times a year, captures the people who will pay
  more for accountability and live access, and it doubles as a way to keep the
  content pressure-tested.
- **Concession and access.** Offer a quiet concession rate for
  under-resourced families and small groups, on request, no proof required. It
  fits the values, and it costs nothing to deliver a self-paced course to one
  more person.

## How it is sold: the funnel

Selling on your own stack means the funnel is Kit plus your site, exactly the
setup the `kit-lead-capture` and `funnel-tracking` skills already describe. Reuse
that, do not reinvent it.

1. **Traffic in.** Social (the `kris-social-positioning` engine), the consulting
   site, Kris's speaking and network, and rare disease organisation partners.
   Every link carries a UTM so you can see which source converts (per the
   `funnel-tracking` skill).
2. **Free intro course as the front door.** Signup captures the email into Kit,
   tagged to the intro-course funnel. This is the list.
3. **Nurture in Kit.** A short sequence that teaches, does not hound, and makes
   the case for the paid pathway by showing what the next course unlocks.
4. **Purchase via Stripe.** A Stripe Checkout link or embedded checkout on the
   course sales page. On success, the automation in
   `05-automation-signup-to-certificate.md` enrols them and tags the purchase in
   Kit.
5. **Deliver and complete.** The learner works through the course on your site.
   On completion, the certificate is generated and emailed automatically.
6. **Post-course.** Kit moves them into an alumni segment and, at the right
   moment, offers the next course or the bundle. Completion of one course is the
   best possible lead for the next.

Attribution is handled by the three layers the `funnel-tracking` skill defines:
Kit tags as the source of truth for who converted from where, UTMs for traffic
in, and Vercel Web Analytics custom events for on-site behaviour before the sale.

## Launch sequence

A staged launch, not a big-bang, so nothing is promised before it is ready.

1. **Soft launch: the free intro course.** Ship Course 1 free, wired to Kit.
   Start building the list and gathering feedback on the format.
2. **First paid course.** Add Course 2 of the families-and-advocates suite with
   Stripe live. This proves the full path: traffic, capture, nurture, purchase,
   deliver, certificate.
3. **Complete the families-and-advocates suite and open the bundle.** Once the
   suite is live, turn on the pathway bundle at its discount.
4. **Organisations suite and licences.** Add the organisations courses and open
   the organisation licence line, and begin selling licences directly to groups.
5. **First live cohort intake.** Once demand is proven, run a facilitated intake
   as the premium tier.

## What to measure

Keep it to the few numbers that decide anything:

- **List growth** from the free intro course, by source (UTM to Kit tag).
- **Free-to-paid conversion rate.** The single most important number.
- **Revenue per line** (single, bundle, licence), so you know where to push.
- **Course completion rate.** A proxy for quality and for how good a lead the
  learner is for the next course.
- **Refund and concession rates.** A health check, not a headline.

## Next actions

- Confirm the pricing structure, or adjust it.
- Decide whether Course 1 is free or priced.
- Set up a Stripe account and create the products and prices above (this can be
  done now; it costs nothing until a sale).
- Confirm the Kit tag and sequence plan against the `kit-lead-capture` and
  `funnel-tracking` skills before building.
