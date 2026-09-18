// Language switcher.
//
// Both language blocks are present in the served HTML. With JavaScript off they
// simply stack, which is correct if longer — nobody is left without a policy
// they can read. This script picks one, reveals the switcher, and remembers the
// choice.
//
// Order of preference: a previous explicit choice, then the browser's language,
// then English.
(function () {
  var STORE = "pacheco-lang";
  var THEME = "pacheco-theme";

  function systemTheme() {
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches
      ? "dark"
      : "light";
  }

  function savedTheme() {
    try {
      var t = localStorage.getItem(THEME);
      return t === "dark" || t === "light" ? t : null;
    } catch (e) {
      return null;
    }
  }

  function applyTheme(theme) {
    document.documentElement.dataset.theme = theme;
    var btn = document.querySelector(".theme");
    if (btn) btn.setAttribute("aria-pressed", String(theme === "dark"));
  }

  function preferred() {
    var saved;
    try {
      saved = localStorage.getItem(STORE);
    } catch (e) {
      saved = null; // Private browsing, or site data blocked.
    }
    if (saved === "en" || saved === "es") return saved;

    var langs = navigator.languages || [navigator.language || "en"];
    for (var i = 0; i < langs.length; i++) {
      if (/^es\b/i.test(langs[i])) return "es";
      if (/^en\b/i.test(langs[i])) return "en";
    }
    return "en";
  }

  function apply(lang) {
    document.documentElement.lang = lang;

    document.querySelectorAll(".langblock").forEach(function (block) {
      block.hidden = block.getAttribute("lang") !== lang;
    });

    document.querySelectorAll(".langbar button").forEach(function (btn) {
      btn.setAttribute("aria-current", String(btn.dataset.lang === lang));
    });

    // The <title> and meta description should match what is on screen.
    var title = document.querySelector('[data-title-' + lang + ']');
    if (title) document.title = title.getAttribute("data-title-" + lang);

    var theme = document.querySelector(".theme");
    if (theme) theme.setAttribute("aria-label", theme.getAttribute("data-label-" + lang));
  }

  document.addEventListener("DOMContentLoaded", function () {
    var bar = document.querySelector(".langbar");
    if (!bar) return;

    bar.hidden = false;

    // Theme: the reader's saved choice, else the system's. Only a click is
    // remembered, so a reader who never touches it keeps following the system.
    applyTheme(savedTheme() || systemTheme());
    if (window.matchMedia) {
      window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", function () {
        if (!savedTheme()) applyTheme(systemTheme());
      });
    }

    bar.addEventListener("click", function (event) {
      var toggle = event.target.closest(".theme");
      if (toggle) {
        var next = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
        applyTheme(next);
        try {
          localStorage.setItem(THEME, next);
        } catch (e) {
          // The choice just will not survive a reload.
        }
        return;
      }

      var btn = event.target.closest("button[data-lang]");
      if (!btn) return;
      var lang = btn.dataset.lang;
      apply(lang);
      try {
        localStorage.setItem(STORE, lang);
      } catch (e) {
        // Nothing to do — the choice just will not survive a reload.
      }
    });

    apply(preferred());

    // Mail links are served in two halves so the address is not sitting in
    // the HTML for harvesters; without JavaScript the readable fallback stays.
    document.querySelectorAll("a.mail[data-u]").forEach(function (a) {
      var addr = a.dataset.u + "@" + a.dataset.d;
      a.href = "mailto:" + addr;
      a.textContent = addr;
    });
  });
})();
