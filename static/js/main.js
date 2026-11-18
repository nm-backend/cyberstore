(function () {
  // mobile menu
  var burger = document.querySelector("[data-burger]");
  var nav = document.querySelector("[data-nav]");
  if (burger && nav) {
    var setMenu = function (open) {
      nav.classList.toggle("open", open);
      burger.setAttribute("aria-expanded", String(open));
      burger.setAttribute("aria-label", open ? "Закрыть меню" : "Открыть меню");
    };
    burger.addEventListener("click", function () {
      setMenu(!nav.classList.contains("open"));
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") setMenu(false);
    });
    document.addEventListener("click", function (event) {
      if (!nav.classList.contains("open")) return;
      if (nav.contains(event.target) || burger.contains(event.target)) return;
      setMenu(false);
    });
  }

  // mobile filters
  var filterToggle = document.querySelector("[data-filter-toggle]");
  var filters = document.querySelector("[data-filters]");
  if (filterToggle && filters) {
    filterToggle.addEventListener("click", function () {
      var open = filters.classList.toggle("open");
      filterToggle.setAttribute("aria-expanded", String(open));
    });
  }

  // catalog: apply select/checkbox filters immediately
  var filterForm = document.querySelector("[data-filter-form]");
  if (filterForm) {
    filterForm.addEventListener("change", function (event) {
      if (event.target.matches("select, input[type=checkbox]")) filterForm.submit();
    });
  }

  // product gallery
  var main = document.querySelector("[data-gallery-main]");
  document.querySelectorAll("[data-thumb]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      if (main) {
        main.src = btn.dataset.full;
        main.alt = btn.dataset.alt || "";
      }
      document.querySelectorAll("[data-thumb]").forEach(function (b) {
        b.setAttribute("aria-current", String(b === btn));
      });
    });
  });

  // lead dialog
  var dialog = document.querySelector("[data-lead-dialog]");
  document.querySelectorAll("[data-open-lead]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      if (dialog && dialog.showModal) dialog.showModal();
    });
  });
  document.querySelectorAll("[data-close-lead]").forEach(function (btn) {
    btn.addEventListener("click", function () { if (dialog) dialog.close(); });
  });
  if (dialog) {
    dialog.addEventListener("click", function (event) {
      if (event.target === dialog) dialog.close();
    });
  }

  // flash messages fade out
  document.querySelectorAll(".msg").forEach(function (msg) {
    setTimeout(function () { msg.remove(); }, 6000);
  });
})();
