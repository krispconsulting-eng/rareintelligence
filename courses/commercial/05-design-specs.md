# Design specs

High-fidelity specifications for the Rare Intelligence surfaces, built on the v3
system in `brand-guidelines.md` and `typography-guide.md`. Every token here is an
existing v3 token; the only shift is the blue-led accent from
`01-brand-identity.md`. Nothing new is introduced. Accessibility target is WCAG
2.1 AA, per `PRODUCT.md`.

There are four surfaces: the catalogue, the course sales page, the course player,
and the certificate. A live prototype of the sales and catalogue surfaces is
provided as a self-contained page alongside this blueprint.

## Shared foundations

- **Container:** max-width 1240px, padding `clamp(20px, 5vw, 72px)`.
- **Section spacing:** `clamp(64px, 9vw, 128px)`.
- **Background:** Cream 50 `#FBF9F5`. Cards Paper white `#FFFFFF`.
- **Dark surfaces:** forest gradient `linear-gradient(165deg, #1E3D34 0%, #234A52 100%)`.
- **Primary accent:** Blue 600 `#3E6F8E`. Secondary Teal 600 `#3D7A6B`.
- **Type:** Outfit display, Archivo body. Overlines Archivo 12px, weight 600,
  uppercase, tracking 0.2em, Blue 700 on light, Blue 200 on dark.
- **Buttons:** pill radius 999px, Archivo 15px weight 600, padding 14px 28px.
  Primary is Blue 600 on cream text; hover `translateY(-2px)` with the blue
  shadow `0 16px 34px -14px rgba(62,111,142,0.65)`; active `scale(0.985)`.
- **Cards:** radius `lg` (24px) or `xl` (32px), border `rgba(29,28,33,0.09)`,
  shadow `card` `0 18px 48px -28px rgba(29,28,33,0.30)`, hover
  `translateY(-2px)` with shadow `md`.
- **Motion:** ease-out `cubic-bezier(0.22,1,0.36,1)`, 200 to 400ms for micro,
  700 to 900ms for reveals. All motion respects `prefers-reduced-motion`.
- **Shadows:** always the cooled base `rgba(29,28,33,...)`, never pure black.

## Surface 1: the catalogue (`/learn`)

The shelf. It has to make the two programs legible in one glance and route a
visitor to the right course.

- **Header:** light-led, per the five moves in `01-brand-identity.md`. A cream
  editorial hero split two ways: on the left the eyebrow label (with its leading
  node), a grounded Outfit headline with the key phrase in Blue 600, lead text,
  two buttons, and a short trust row; on the right the signature **pathway card**,
  a contained forest-gradient panel showing the tiers as a node-and-line step
  diagram. This is the front door and the clearest statement that this is not the
  consulting home page.
- **Program split:** two clear programs, "Families and advocates" and
  "Organisations", each introduced by a label and a one-line description.
- **Numbered tiers:** within each program, courses are grouped under large
  numbered tier indices (01 Orientation, 02 Partnering, and so on), each with a
  hairline rule and a right-aligned tier note. The numbering is a real sequence,
  not decoration.
- **Course cards:** a responsive grid of reference-style cards, Paper white on
  cream, 14px radius, flatter shadow. Each card carries an index numeral, an
  optional chip (Sage "Free" or Teal "Most chosen"), the course title in Outfit,
  a one-line outcome, a hairline meta row (self-paced, module count, "current as
  at" date), the price, and a button.
- **Bundle callout:** after each program grid, a wider forest-gradient panel
  offering the pathway bundle at its price, with the single-course total shown
  struck through as the anchor.
- **Responsive:** three columns at desktop, two at tablet, one at mobile. Cards
  keep a consistent height per row; the button sits at the card foot.

## Surface 2: the course sales page (`/learn/[course]`)

One page per course, public and indexable. This is where the sale is made, so it
is generous with substance and free of hype.

Structure, top to bottom:

1. **Header.** Overline (tier and audience), course title in Outfit H1, a
   two-line outcome statement, price, and a primary buy button. A secondary line:
   "Content current as at [date]".
2. **What you will be able to do.** The outcome, expanded into three or four
   concrete capabilities. Outcome-first, per the brand.
3. **What is inside.** The module list from the course design, each with a
   one-line description. This is the syllabus; showing it in full is a trust
   signal, not a giveaway.
4. **Who it is for.** The audience note, plainly stated, including who it is not
   for.
5. **Why it is credible.** A short, factual block on Kris and the sources the
   content is built from. No testimonial theatre; the credibility is real, so
   state it.
6. **Currency.** A short note on how the content is kept current, with the "as
   at" date. This is a differentiator, so give it a line.
7. **Buy.** A final forest-gradient CTA panel with the price, the button, and the
   bundle alternative alongside.

- **Sticky buy affordance** on desktop: a slim summary with price and button that
  follows as the visitor scrolls the syllabus. Never a pop-up, never a timer.

## Surface 3: the course player (`/learn/[course]/[lesson]`, gated)

Where the learning happens. Calm, readable, and focused. This surface sits behind
the access gate.

- **Layout:** a two-pane layout. Left, a lesson list for the course with progress
  ticks (Sage 500) and the current lesson highlighted. Right, the lesson content
  in a comfortable reading measure (about 68 characters), Archivo body at 17px,
  line-height 1.62.
- **Lesson head:** overline (module), lesson title in Outfit H1, and the "current
  as at" date.
- **Progress:** a thin progress bar for the course at the top of the left pane.
  Completing a lesson is a single clear action ("Mark complete") that advances to
  the next lesson.
- **Media:** where a lesson has video or audio, it sits at the top of the reading
  pane in a `lg`-radius frame. Text lessons need no media to feel complete.
- **Completion:** finishing the last lesson reveals a quiet completion state and
  triggers the certificate (per `04-automation-signup-to-certificate.md`). No
  confetti; a plain, earned acknowledgement.
- **Focus and calm:** no upsells inside the player. The next-course prompt lives
  in email, not in the middle of learning.

## Surface 4: the certificate

Specified in `01-brand-identity.md`; the design detail:

- **Format:** A4 landscape PDF, rendered from the branded HTML template.
- **Header band:** forest gradient, with the Rare Intelligence wordmark in cream
  and the "by Kris Pierce Consulting" endorsement in the overline style.
- **Body:** on Paper white. "This certifies that" in Archivo, the learner name in
  Outfit H1 weight 600, the course title in Outfit H2, all centred with generous
  space.
- **Footer:** completion date, certificate id, and "Content current as at
  [date]" in Archivo XS Taupe 500, plus Kris's name and role. A hairline rule in
  Taupe 100 above the footer.
- **Restraint:** no seals, no ribbons, no gold. The forest band and the
  typography carry it. The credibility is in the name and the currency date, not
  in ornament.

## Accessibility

- Body text contrast at least 4.5:1; large text at least 3:1. The v3 pairings in
  the typography guide already meet this; hold to them.
- Visible focus states on every interactive element, using the Blue focus ring.
- Full keyboard operation of the player, including lesson navigation and mark
  complete.
- Respect `prefers-reduced-motion`: reveals and hovers reduce to opacity or
  nothing.
- Alt text on all imagery; captions or transcripts on any video or audio.

## Next actions

- Review the live sales and catalogue prototype provided with this blueprint.
- Confirm the blue-led accent reads correctly against the consulting site.
- Approve the surfaces so they can be built as pages in the `/learn` section.
