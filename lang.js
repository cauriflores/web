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
  }

  document.addEventListener("DOMContentLoaded", function () {
    var bar = document.querySelector(".langbar");
    if (!bar) return;

    bar.hidden = false;

    bar.addEventListener("click", function (event) {
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
  });
})();
