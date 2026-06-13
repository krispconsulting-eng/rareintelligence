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
  "radial-gradient(58% 58% at 76% 68%, rgba(0,201,177,0.18), transparent 72%), " +
  "linear-gradient(100deg, rgba(8,15,30,0.66) 0%, rgba(8,15,30,0.34) 52%, rgba(8,15,30,0.04) 100%)";

const FONTS_HREF =
  "https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@700;800&family=DM+Mono:wght@400;500&family=Instrument+Sans:wght@400;500;600&family=Lora:ital,wght@1,500&display=swap";

const NAV_LINKS = ["Home", "Product", "About", "Contact"];

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
        @keyframes ri-rock {
          0%, 100% { transform: perspective(1100px) rotateX(0deg); }
          25%      { transform: perspective(1100px) rotateX(6deg); }
          75%      { transform: perspective(1100px) rotateX(-6deg); }
        }
        .ri-mascot-glow, .ri-mascot {
          -webkit-mask-image: linear-gradient(to bottom, #000 56%, rgba(0,0,0,0.16) 86%, transparent 100%);
                  mask-image: linear-gradient(to bottom, #000 56%, rgba(0,0,0,0.16) 86%, transparent 100%);
        }
        .ri-mascot-glow {
          position: absolute; left: 50%; top: 0; width: 100%;
          transform: translateX(-50%) scale(1.07);
          z-index: 1; pointer-events: none;
          filter: blur(24px) saturate(1.15); opacity: .6;
        }
        .ri-mascot {
          position: relative; z-index: 2;
          transform-origin: 50% 92%;
          transform: perspective(1100px) rotateX(0deg);
          transition: transform .5s cubic-bezier(0.22,1,0.36,1);
          will-change: transform;
          filter: drop-shadow(0 22px 44px rgba(8,15,30,0.45));
        }
        .ri-mascot:hover { animation: ri-rock 6s ease-in-out infinite; }
        .ri-atmos { position: absolute; inset: -22% -18%; z-index: 0; pointer-events: none; filter: blur(34px); opacity: .95; }
        .ri-atmos span { position: absolute; border-radius: 9999px; }
        @media (prefers-reduced-motion: reduce) {
          .ri-mascot, .ri-mascot:hover { animation: none; transition: none; }
          .ri-cta, .ri-cta * { transition: none; }
        }
      `}</style>

      {/* Slim transparent nav */}
      <header className="mx-auto flex w-full max-w-7xl items-center justify-between px-6 py-6 lg:px-10">
        <a href="/" className="flex items-center gap-3">
          {/* Circular zebra logo badge */}
          <span
            className="grid h-10 w-10 place-items-center overflow-hidden rounded-full"
            style={{ border: `2px solid ${C.teal}`, background: C.midnight }}
          >
            <img
              src="/logo-circle.png"
              alt="Rare Intelligence"
              className="h-full w-full object-cover"
              onError={(e) => { e.currentTarget.style.display = "none"; }}
            />
          </span>
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
            <div className="relative mx-auto w-full max-w-[360px] sm:max-w-[420px] lg:max-w-[460px]">
              {/* Cool-palette bokeh atmosphere, blurred behind the zebra */}
              <div className="ri-atmos" aria-hidden="true">
                <span style={{ width: 240, height: 240, left: "2%",   top: "2%",     background: C.cobalt,  opacity: 0.60 }} />
                <span style={{ width: 170, height: 170, right: "-4%", top: "16%",    background: C.ocean,   opacity: 0.55 }} />
                <span style={{ width: 140, height: 140, left: "-6%",  top: "46%",    background: C.teal,    opacity: 0.50 }} />
                <span style={{ width: 90,  height: 90,  right: "6%",  top: "54%",    background: C.aqua,    opacity: 0.60 }} />
                <span style={{ width: 210, height: 210, left: "24%",  bottom: "-4%", background: C.indigo,  opacity: 0.60 }} />
                <span style={{ width: 70,  height: 70,  left: "50%",  top: "8%",     background: C.seafoam, opacity: 0.45 }} />
                <span style={{ width: 110, height: 110, right: "20%", bottom: "8%",  background: C.teal,    opacity: 0.40 }} />
              </div>
              {/* Blurred halo copy so the zebra's edge dissolves into the page */}
              <img src="/mascot.png" alt="" aria-hidden="true" className="ri-mascot-glow w-full"
                   onError={(e) => { e.currentTarget.style.display = "none"; }} />
              {/* Zebra: still at rest, rocks forward/back on hover.
                  Hidden gracefully until /mascot.png exists. */}
              <img
                src="/mascot.png"
                alt="The Rare Intelligence zebra mascot"
                className="ri-mascot block w-full"
                onError={(e) => { e.currentTarget.style.visibility = "hidden"; }}
              />
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}
