/* Rare Intelligence — interactions
   1. Mobile nav toggle
   2. Scroll-reveal for .reveal elements
   3. Newsletter / membership forms → Web3Forms
*/
(function () {
  "use strict";

  // Set to the Web3Forms access key for the hello@ inbox before launch.
  const WEB3FORMS_KEY = "";

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

  /* ---- Forms → Web3Forms (https://web3forms.com) ---- */
  document.querySelectorAll("form[data-stub]").forEach(function (form) {
    // Honeypot: invisible to people, irresistible to bots.
    const honeypot = document.createElement("input");
    honeypot.type = "text";
    honeypot.name = "botcheck";
    honeypot.tabIndex = -1;
    honeypot.autocomplete = "off";
    honeypot.setAttribute("aria-hidden", "true");
    honeypot.style.cssText = "position:absolute;left:-9999px;width:1px;height:1px;opacity:0;";
    form.appendChild(honeypot);

    const note = form.parentElement.querySelector("[data-stub-note]");
    const button = form.querySelector("button[type=submit]");

    function show(message) {
      if (note) {
        note.textContent = message;
        note.style.display = "block";
      }
    }

    form.addEventListener("submit", function (e) {
      e.preventDefault();

      // Bots fill the hidden field; quietly drop those submissions.
      if (honeypot.value) return;

      if (!WEB3FORMS_KEY) {
        show("We're not quite live yet — email hello@rareintelligence.com and we'll add you personally.");
        return;
      }

      const payload = {
        access_key: WEB3FORMS_KEY,
        subject: "Rare Intelligence — " + (form.dataset.source || "website") + " signup",
        "form-source": form.dataset.source || window.location.pathname,
        name: (form.elements.name && form.elements.name.value) || "",
        email: form.elements.email.value,
        botcheck: honeypot.value
      };

      if (button) button.disabled = true;
      show("Sending…");

      fetch("https://api.web3forms.com/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json", "Accept": "application/json" },
        body: JSON.stringify(payload)
      })
        .then(function (res) { return res.json(); })
        .then(function (data) {
          if (data && data.success) {
            show("Thanks! You're on the list — we'll be in touch soon.");
            form.reset();
          } else {
            show("Something went wrong — please try again, or email hello@rareintelligence.com.");
          }
        })
        .catch(function () {
          show("Something went wrong — please try again, or email hello@rareintelligence.com.");
        })
        .finally(function () {
          if (button) button.disabled = false;
        });
    });
  });

  /* ---- Footer year ---- */
  const yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();
})();
