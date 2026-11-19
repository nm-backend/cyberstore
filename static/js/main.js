(function () {
  // mobile menu
  var burger = document.querySelector("[data-burger]");
  var nav = document.querySelector("[data-nav]");
  var setMenu = function (open) {
    if (!nav || !burger) return;
    nav.classList.toggle("open", open);
    burger.setAttribute("aria-expanded", String(open));
    burger.setAttribute("aria-label", open ? "Закрыть меню" : "Открыть меню");
  };
  if (burger && nav) {
    burger.addEventListener("click", function () {
      setMenu(!nav.classList.contains("open"));
    });
  }

  // catalog dropdown in the nav
  var drops = Array.prototype.slice.call(document.querySelectorAll("[data-nav-drop]"));
  var closeDrops = function (except) {
    drops.forEach(function (drop) {
      if (drop === except || !drop.classList.contains("open")) return;
      drop.classList.remove("open");
      var toggle = drop.querySelector("[data-nav-drop-toggle]");
      if (toggle) toggle.setAttribute("aria-expanded", "false");
    });
  };
  drops.forEach(function (drop) {
    var toggle = drop.querySelector("[data-nav-drop-toggle]");
    if (!toggle) return;
    toggle.addEventListener("click", function (event) {
      event.preventDefault();
      var open = !drop.classList.contains("open");
      closeDrops(drop);
      drop.classList.toggle("open", open);
      toggle.setAttribute("aria-expanded", String(open));
    });
  });
  document.addEventListener("click", function (event) {
    drops.forEach(function (drop) {
      if (drop.classList.contains("open") && !drop.contains(event.target)) closeDrops(null);
    });
    if (!nav || !nav.classList.contains("open")) return;
    if (nav.contains(event.target) || (burger && burger.contains(event.target))) return;
    setMenu(false);
  });

  // mobile filters drawer
  var filterToggle = document.querySelector("[data-filter-toggle]");
  var filters = document.querySelector("[data-filters]");
  var setFilters = function (open) {
    if (!filters) return;
    filters.classList.toggle("open", open);
    document.body.classList.toggle("filters-open", open);
    if (filterToggle) filterToggle.setAttribute("aria-expanded", String(open));
  };
  if (filterToggle && filters) {
    filterToggle.addEventListener("click", function () {
      setFilters(!filters.classList.contains("open"));
    });
  }
  document.querySelectorAll("[data-filter-close]").forEach(function (btn) {
    btn.addEventListener("click", function () { setFilters(false); });
  });

  // Escape closes the mobile menu and the filter drawer (search has its own handler)
  document.addEventListener("keydown", function (event) {
    if (event.key !== "Escape") return;
    if (nav && nav.classList.contains("open")) setMenu(false);
    if (filters && filters.classList.contains("open")) setFilters(false);
  });

  // catalog: only selects explicitly marked as auto-submit reload the page
  var filterForm = document.querySelector("[data-filter-form]");
  if (filterForm) {
    filterForm.addEventListener("change", function (event) {
      if (event.target.matches("select[data-auto-submit]")) filterForm.submit();
    });
  }

  // live search over category tiles
  document.querySelectorAll("[data-cat-search]").forEach(function (input) {
    var section = input.closest("[data-cat-section]");
    if (!section) return;
    var tiles = Array.prototype.slice.call(section.querySelectorAll(".category-tile"));
    var empty = section.querySelector("[data-cat-search-empty]");
    input.addEventListener("input", function () {
      var query = input.value.trim().toLowerCase();
      var shown = 0;
      tiles.forEach(function (tile) {
        var name = (tile.getAttribute("data-tile-name") || "").toLowerCase();
        var match = !query || name.indexOf(query) !== -1;
        tile.hidden = !match;
        if (match) shown += 1;
      });
      if (empty) empty.hidden = shown !== 0;
    });
  });

  // live search inside a long filter group
  document.querySelectorAll("[data-filter-search]").forEach(function (input) {
    var group = input.closest(".filter-group");
    if (!group) return;
    var items = Array.prototype.slice.call(group.querySelectorAll(".checkbox-item"));
    input.addEventListener("input", function () {
      var query = input.value.trim().toLowerCase();
      items.forEach(function (item) {
        item.hidden = Boolean(query) && item.textContent.toLowerCase().indexOf(query) === -1;
      });
    });
  });

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

  // one Escape closes the catalog dropdown, mobile filters and the menu
  document.addEventListener("keydown", function (event) {
    if (event.key !== "Escape") return;
    closeDrops(null);
    setFilters(false);
    setMenu(false);
  });

  // flash messages fade out
  document.querySelectorAll(".msg").forEach(function (msg) {
    setTimeout(function () { msg.remove(); }, 6000);
  });
})();
