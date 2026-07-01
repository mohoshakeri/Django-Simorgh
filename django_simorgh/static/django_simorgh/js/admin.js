(function () {
  var root = document.documentElement;
  var storageKey = "django-simorgh-mode";
  var savedMode = localStorage.getItem(storageKey);
  var prefersDark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
  var mode = savedMode || (prefersDark ? "dark" : "light");

  function setMode(nextMode) {
    root.dataset.simorghMode = nextMode;
    localStorage.setItem(storageKey, nextMode);
    document.querySelectorAll("[data-simorgh-mode-label]").forEach(function (node) {
      var button = node.closest("[data-simorgh-theme-toggle]");
      var darkLabel = button ? button.dataset.simorghDarkLabel : "Dark";
      var lightLabel = button ? button.dataset.simorghLightLabel : "Light";
      node.textContent = nextMode === "dark" ? lightLabel : darkLabel;
    });
  }

  function setSidebar(open) {
    root.dataset.simorghSidebar = open ? "open" : "closed";
  }

  document.addEventListener("DOMContentLoaded", function () {
    setMode(mode);

    document.querySelectorAll("[data-simorgh-theme-toggle]").forEach(function (button) {
      button.addEventListener("click", function () {
        setMode(root.dataset.simorghMode === "dark" ? "light" : "dark");
      });
    });

    document.querySelectorAll("[data-simorgh-sidebar-toggle]").forEach(function (button) {
      button.addEventListener("click", function () {
        setSidebar(root.dataset.simorghSidebar !== "open");
      });
    });

    document.querySelectorAll(".simorgh-app__button").forEach(function (button) {
      button.addEventListener("click", function () {
        var app = button.closest(".simorgh-app");
        if (app) {
          app.classList.toggle("is-open");
          button.setAttribute("aria-expanded", app.classList.contains("is-open") ? "true" : "false");
        }
      });
    });
  });
})();
