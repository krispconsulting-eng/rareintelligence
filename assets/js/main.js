/* Rare Intelligence — interactions
   1. Mobile nav toggle
   2. Scroll-reveal for .reveal elements
   3. Newsletter / contact form stubs (no backend yet)
*/
(function () {
  "use strict";

  /* ---- Mobile nav ---- */
  const header = document.querySelector(".site-header");
  const toggle = document.querySelector(".nav-toggle");
  if (toggle && header) {
    toggle.addEventListener("click", function () {
      const open = header.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    // close menu when a link is tapped
    header.querySelectorAll(".nav-links a").forEach(function (a) {
      a.addEventListener("click", function () {
        header.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  /* ---- Scroll reveal ---- */
  const revealEls = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && revealEls.length) {
    const io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("in");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
    );
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("in"); });
  }

  /* ---- Form stubs (front-end only for now) ---- */
  document.querySelectorAll("form[data-stub]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      const note = form.querySelector("[data-stub-note]");
      if (note) {
        note.textContent = "Thanks! You're on the list — we'll be in touch soon.";
        note.style.display = "block";
      }
      form.reset();
    });
  });

  /* ---- Footer year ---- */
  const yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();
})();
