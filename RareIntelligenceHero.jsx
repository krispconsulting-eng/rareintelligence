import React from "react";

/**
 * Rare Intelligence — home page hero
 * Deep Signal brand system v1.0 · KrispConsulting
 *
 * Self-contained: Google Fonts load via <link>, keyframes live in the
 * inline <style> block, and all colours are Deep Signal tokens. Tailwind
 * handles layout/spacing; brand colours use arbitrary-value classes or
 * inline styles. No warm hues — restraint is the brand.
 *
 * Art placeholders (supplied separately):
 *   /mascot.png   — cute 3D zebra mascot, transparent background
 *   /favicon.png  — small badge mark beside the nav wordmark
 */

/* ---- Deep Signal tokens ------------------------------------------------ */
const C = {
  midnight: "#080F1E",
  card:     "#0E1C35",
  lift:     "#152844",
  indigo:   "#2D3580",
  cobalt:   "#1A4FBF",
  ocean:    "#0E7FA8",
  teal:     "#00C9B1", // the one accent
  aqua:     "#3DD6C8",
  seafoam:  "#80EAD8",
  mint:     "#C2F5EE",
  ghost:    "#EEF8F7",
  grey:     "#8BA8A5",
};

const F = {
  display: '"Bricolage Grotesque", sans-serif',
  body:    '"Instrument Sans", sans-serif',
  serif:   '"Lora", serif',
  mono:    '"DM Mono", monospace',
};

/* Brand gradient — punctuation only: a contained band, never the page */
const GRADIENT_BRAND_DIAG =
  `linear-gradient(135deg, ${C.indigo} 0%, ${C.cobalt} 34%, ${C.ocean} 67%, ${C.teal} 100%)`;

/* Navy veil over the band — deepest where the copy sits, so text stays AAA;
   plus a quiet teal bloom behind the mascot */
const BAND_VEIL =
  "radial-gradient(58% 58% at 76% 68%, rgba(0,201,177,0.14), transparent 72%), " +
  "linear-gradient(100deg, rgba(8,15,30,0.90) 0%, rgba(8,15,30,0.66) 55%, rgba(8,15,30,0.30) 100%)";

/* The zebra — fine 35° diagonal, felt not seen (layer opacity keeps it ≤20%) */
const ZEBRA =
  "repeating-linear-gradient(125deg, transparent 0 8px, rgba(255,255,255,0.55) 8px 10px)";

const FONTS_HREF =
  "https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@700;800&family=DM+Mono:wght@400;500&family=Instrument+Sans:wght@400;500;600&family=Lora:ital,wght@1,500&display=swap";

const NAV_LINKS = ["Home", "Product", "About", "Contact"];

/* ---- Signature ring ----------------------------------------------------
 * Ten dots cycling the family around a vivid-teal core: teal at the top
 * (the signal), descending through aqua → ocean → cobalt to indigo at the
 * bottom (the depth), with two small seafoam companions flanking the top.
 * Mirrors assets/logo/option-b-signal-ring.svg. Stays sharp — never blurs.
 */
const RING_DOTS = [
  { angle: -90,  color: C.teal,    r: 10 },
  { angle: -45,  color: C.aqua,    r: 10 },
  { angle:   0,  color: C.ocean,   r: 10 },
  { angle:  45,  color: C.cobalt,  r: 10 },
  { angle:  90,  color: C.indigo,  r: 10 },
  { angle: 135,  color: C.cobalt,  r: 10 },
  { angle: 180,  color: C.ocean,   r: 10 },
  { angle: 225,  color: C.aqua,    r: 10 },
  { angle: -111, color: C.seafoam, r: 6, inset: true },
  { angle: -69,  color: C.seafoam, r: 6, inset: true },
];

function SignalRing() {
  const CX = 200;
  const ORBIT = 168;
  return (
    <svg
      viewBox="0 0 400 400"
      aria-hidden="true"
      className="absolute inset-0 h-full w-full"
    >
      <defs>
        <linearGradient id="ri-core-disc" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stopColor={C.lift} />
          <stop offset="1" stopColor={C.card} />
        </linearGradient>
        <radialGradient id="ri-core-glow" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor={C.teal} stopOpacity="0.22" />
          <stop offset="55%" stopColor={C.teal} stopOpacity="0.08" />
          <stop offset="100%" stopColor={C.teal} stopOpacity="0" />
        </radialGradient>
      </defs>

      {/* quiet navy disc with the vivid-teal core glow */}
      <circle cx={CX} cy={CX} r={146} fill="url(#ri-core-disc)" stroke={C.cobalt} strokeWidth="1" strokeOpacity="0.5" />
      <circle cx={CX} cy={CX} r={146} fill="url(#ri-core-glow)" />

      {/* outer ring */}
      <circle cx={CX} cy={CX} r={ORBIT} fill="none" stroke={C.teal} strokeWidth="1.5" opacity="0.5" />

      {/* ten dots cycling the family */}
      {RING_DOTS.map(({ angle, color, r, inset }) => {
        const rad = (angle * Math.PI) / 180;
        const orbit = inset ? ORBIT - 4 : ORBIT;
        return (
          <circle
            key={angle}
            cx={CX + orbit * Math.cos(rad)}
            cy={CX + orbit * Math.sin(rad)}
            r={r}
            fill={color}
          />
        );
      })}
    </svg>
  );
}

/* ---- Hero -------------------------------------------------------------- */
export default function RareIntelligenceHero() {
  return (
    <div
      className="flex min-h-screen flex-col antialiased"
      style={{ background: C.midnight, fontFamily: F.body }}
    >
      <link rel="preconnect" href="https://fonts.googleapis.com" />
      <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
      <link rel="stylesheet" href={FONTS_HREF} />

      <style>{`
        @keyframes ri-drift {
          0%, 100% { filter: blur(0px); transform: translateY(0) scale(1); }
          50%      { filter: blur(6px); transform: translateY(-12px) scale(1.04); }
        }
        .ri-mascot {
          animation: ri-drift 5s ease-in-out infinite;
          will-change: filter, transform;
        }
        @media (prefers-reduced-motion: reduce) {
          .ri-mascot { animation: none; }
          .ri-cta, .ri-cta * { transition: none; }
        }
      `}</style>

      {/* Slim transparent nav */}
      <header className="mx-auto flex w-full max-w-7xl items-center justify-between px-6 py-6 lg:px-10">
        <a href="/" className="flex items-center gap-3">
          <img src="/favicon.png" alt="" className="h-8 w-8" />
          <span
            className="text-lg tracking-[0.06em]"
            style={{ fontFamily: F.display, fontWeight: 800, color: C.ghost }}
          >
            RARE <span style={{ color: C.teal }}>INTELLIGENCE</span>
          </span>
        </a>
        <nav className="hidden items-center gap-9 text-[15px] font-medium sm:flex">
          {NAV_LINKS.map((label, i) => (
            <a
              key={label}
              href={i === 0 ? "/" : `/${label.toLowerCase()}`}
              className="transition-colors duration-200 hover:text-[#EEF8F7]"
              style={{ color: i === 0 ? C.ghost : C.grey }}
            >
              {label}
            </a>
          ))}
        </nav>
      </header>

      {/* Hero */}
      <main className="mx-auto w-full max-w-7xl flex-1 px-4 pb-14 pt-2 sm:px-6 lg:px-10">
        {/* Contained gradient band — the floor stays midnight navy */}
        <section className="relative overflow-hidden rounded-[2rem] sm:rounded-[2.75rem]">
          <div aria-hidden="true" className="absolute inset-0" style={{ background: GRADIENT_BRAND_DIAG }} />
          <div aria-hidden="true" className="absolute inset-0" style={{ background: BAND_VEIL }} />
          {/* the zebra — hidden thread, ~15% */}
          <div aria-hidden="true" className="absolute inset-0 opacity-[0.15]" style={{ background: ZEBRA }} />

          <div className="relative grid items-center gap-14 px-7 py-16 sm:px-12 sm:py-20 lg:min-h-[620px] lg:grid-cols-[minmax(0,1.05fr)_minmax(0,0.95fr)] lg:gap-12 lg:px-20 lg:py-24">
            {/* Copy */}
            <div className="max-w-xl">
              <p
                className="mb-7 text-[13px] uppercase tracking-[0.32em]"
                style={{ fontFamily: F.mono, fontWeight: 500, color: C.seafoam }}
              >
                AI for rare disease leaders
              </p>

              <h1
                className="text-[44px] leading-[1.04] sm:text-[58px] lg:text-[66px] xl:text-[78px]"
                style={{
                  fontFamily: F.display,
                  fontWeight: 800,
                  color: C.ghost,
                  letterSpacing: "-0.02em",
                  textWrap: "balance",
                }}
              >
                <em style={{ color: C.teal }}>Rare</em> by nature. Intelligent by design.
              </h1>

              <p
                className="mt-7 max-w-md text-lg leading-relaxed sm:text-xl"
                style={{ fontFamily: F.serif, fontStyle: "italic", fontWeight: 500, color: C.mint }}
              >
                Putting AI to work for the rare-disease community — practically,
                calmly, without hype.
              </p>

              {/* The one teal action per view */}
              <div className="mt-10">
                <a
                  href="#how-it-works"
                  className="ri-cta group inline-flex items-center gap-3 rounded-full bg-[#00C9B1] py-3 pl-7 pr-3 text-[17px] font-semibold text-[#080F1E] transition-all duration-300 hover:-translate-y-0.5 hover:bg-[#3DD6C8] hover:shadow-[0_14px_40px_rgba(0,201,177,0.25)]"
                >
                  See how it works
                  <span className="flex h-9 w-9 items-center justify-center rounded-full bg-[#080F1E] transition-transform duration-300 group-hover:translate-x-0.5">
                    <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
                      <path
                        d="M2.5 8h11m0 0L9.3 3.8M13.5 8l-4.2 4.2"
                        stroke={C.teal}
                        strokeWidth="1.7"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      />
                    </svg>
                  </span>
                </a>
              </div>
            </div>

            {/* Mascot in the signature ring — stacks below copy on mobile */}
            <div className="relative mx-auto w-full max-w-[400px] sm:max-w-[460px] lg:max-w-[540px]">
              <div className="relative aspect-square">
                <SignalRing />
                {/* only the zebra drifts out of focus; the ring stays sharp.
                    Hidden gracefully until /mascot.png exists. */}
                <div className="absolute left-1/2 top-1/2 w-[53%] -translate-x-1/2 -translate-y-1/2">
                  <img
                    src="/mascot.png"
                    alt="The Rare Intelligence zebra mascot"
                    className="ri-mascot block w-full"
                    onError={(e) => { e.currentTarget.style.visibility = "hidden"; }}
                  />
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}
