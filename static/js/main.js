(function () {
  "use strict";

  // Browsers already restore the catalog position on «back»; keep that, and
  // never reset scroll ourselves. This only makes the behaviour explicit.
  if ("scrollRestoration" in history) history.scrollRestoration = "auto";

  var scrollLocks = { menu: false, filters: false };
  function syncScrollLock() {
    var locked = scrollLocks.menu || scrollLocks.filters;
    document.documentElement.classList.toggle("no-scroll", locked);
    document.body.classList.toggle("no-scroll", locked);
  }
  function rememberFocus(element) {
    return element && element.focus ? element : null;
  }

  // Mobile menu
  var burger = document.querySelector("[data-burger]");
  var nav = document.querySelector("[data-nav]");
  var menuReturnFocus = null;
  var setMenu = function (open) {
    if (!nav || !burger) return;
    if (open && !nav.classList.contains("open")) menuReturnFocus = rememberFocus(document.activeElement);
    nav.classList.toggle("open", open);
    burger.setAttribute("aria-expanded", String(open));
    burger.setAttribute("aria-label", open ? "Закрыть меню" : "Открыть меню");
    scrollLocks.menu = open;
    syncScrollLock();
    if (!open && menuReturnFocus) {
      menuReturnFocus.focus();
      menuReturnFocus = null;
    }
  };
  if (burger && nav) {
    burger.addEventListener("click", function () {
      setMenu(!nav.classList.contains("open"));
    });
  }

  // Catalog dropdown in the nav
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

  // Mobile filters drawer
  var filterToggle = document.querySelector("[data-filter-toggle]");
  var filters = document.querySelector("[data-filters]");
  var filterBackdrop = document.querySelector("[data-filter-backdrop]");
  var filterReturnFocus = null;
  var setFilters = function (open) {
    if (!filters) return;
    if (open && !filters.classList.contains("open")) {
      filterReturnFocus = filterToggle || rememberFocus(document.activeElement);
    }
    filters.classList.toggle("open", open);
    document.body.classList.toggle("filters-open", open);
    if (filterBackdrop) filterBackdrop.hidden = !open;
    if (filterToggle) filterToggle.setAttribute("aria-expanded", String(open));
    scrollLocks.filters = open;
    syncScrollLock();
    if (open) {
      var close = filters.querySelector("[data-filter-close]");
      if (close) close.focus();
    } else if (filterReturnFocus) {
      filterReturnFocus.focus();
      filterReturnFocus = null;
    }
  };
  if (filterToggle && filters) {
    filterToggle.addEventListener("click", function () {
      setFilters(!filters.classList.contains("open"));
    });
  }
  document.querySelectorAll("[data-filter-close]").forEach(function (btn) {
    btn.addEventListener("click", function () { setFilters(false); });
  });
  if (filterBackdrop) {
    filterBackdrop.addEventListener("click", function () { setFilters(false); });
  }
  if (filters) {
    filters.addEventListener("click", function (event) {
      if (event.target === filters) setFilters(false);
    });
  }

  document.addEventListener("keydown", function (event) {
    if (event.key !== "Escape") return;
    if (drops.some(function (drop) { return drop.classList.contains("open"); })) {
      closeDrops(null);
    }
    if (filters && filters.classList.contains("open")) setFilters(false);
    if (nav && nav.classList.contains("open")) setMenu(false);
  });

  // Empty filter values must not end up as price_min=&price_max= in the URL.
  function cleanEmptyFields(form) {
    Array.prototype.forEach.call(form.elements, function (field) {
      if (!field.name || field.disabled) return;
      if (field.type === "checkbox" || field.type === "radio") return;
      if (!String(field.value || "").trim()) field.disabled = true;
    });
  }

  var filterForm = document.querySelector("[data-filter-form]");
  if (filterForm) {
    filterForm.addEventListener("submit", function () { cleanEmptyFields(filterForm); });
    filterForm.addEventListener("change", function (event) {
      if (event.target.matches("select[data-auto-submit], input[type='radio'][data-auto-submit]")) {
        cleanEmptyFields(filterForm);
        filterForm.submit();
      }
    });
  }

  // Sort without an inline onchange handler.
  document.querySelectorAll(".field-sort").forEach(function (select) {
    select.addEventListener("change", function () {
      if (select.form) select.form.submit();
    });
  });

  // Live search over category tiles
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

  // Live search inside a long filter group
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

  // Product gallery
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

  // Lead dialog
  var dialog = document.querySelector("[data-lead-dialog]");
  function openLeadDialog() {
    if (!dialog || !dialog.showModal) return;
    if (!dialog.open) dialog.showModal();
    var invalid = dialog.querySelector('[aria-invalid="true"]');
    var first = invalid || dialog.querySelector("#lead_name");
    if (first) first.focus();
  }
  document.querySelectorAll("[data-open-lead]").forEach(function (btn) {
    btn.addEventListener("click", openLeadDialog);
  });
  document.querySelectorAll("[data-close-lead]").forEach(function (btn) {
    btn.addEventListener("click", function () { if (dialog) dialog.close(); });
  });
  if (dialog) {
    dialog.addEventListener("click", function (event) {
      if (event.target === dialog) dialog.close();
    });
    if (dialog.dataset.openOnLoad) openLeadDialog();
  }

  // Russian inline validation. Server validation remains authoritative.
  var leadForm = document.querySelector("[data-lead-form]");
  if (leadForm) {
    leadForm.noValidate = true;
    var nameInput = leadForm.querySelector('[name="name"]');
    var phoneInput = leadForm.querySelector('[name="phone"]');
    var consentInput = leadForm.querySelector('[name="consent"]');

    function errorBox(input) {
      var holder = input.closest(".form-field-group") || input.closest(".consent-field");
      if (!holder) return null;
      var box = holder.querySelector(".field-error[data-js-error]");
      if (!box) {
        box = document.createElement("span");
        box.className = "field-error";
        box.setAttribute("data-js-error", "");
        holder.appendChild(box);
      }
      return box;
    }
    function setError(input, message) {
      if (!input) return;
      input.setAttribute("aria-invalid", "true");
      var box = errorBox(input);
      if (box) box.textContent = message;
    }
    function clearError(input) {
      if (!input) return;
      input.removeAttribute("aria-invalid");
      input.setCustomValidity("");
      var holder = input.closest(".form-field-group") || input.closest(".consent-field");
      if (holder) {
        holder.querySelectorAll(".field-error[data-js-error]").forEach(function (el) { el.remove(); });
      }
    }
    function validateLead() {
      var valid = true;
      [nameInput, phoneInput, consentInput].forEach(clearError);

      var name = nameInput ? nameInput.value.trim() : "";
      if (name.length < 2) {
        setError(nameInput, "Укажите имя — хотя бы 2 символа.");
        valid = false;
      } else if (name.length > 100) {
        setError(nameInput, "Имя не должно быть длиннее 100 символов.");
        valid = false;
      }

      var phone = phoneInput ? phoneInput.value.trim() : "";
      var digits = phone.replace(/\D/g, "");
      if (!/^[+0-9][0-9\s()\-]{6,29}$/.test(phone) || digits.length < 9 || digits.length > 15) {
        setError(phoneInput, "Введите номер телефона, например +996 555 123 456.");
        valid = false;
      }

      if (consentInput && !consentInput.checked) {
        setError(consentInput, "Подтвердите согласие на обработку персональных данных.");
        valid = false;
      }
      return valid;
    }

    [nameInput, phoneInput, consentInput].forEach(function (input) {
      if (!input) return;
      input.addEventListener("input", function () { clearError(input); });
      input.addEventListener("change", function () { clearError(input); });
    });

    leadForm.addEventListener("submit", function (event) {
      if (!validateLead()) {
        event.preventDefault();
        var firstInvalid = leadForm.querySelector('[aria-invalid="true"]');
        if (firstInvalid) firstInvalid.focus();
      }
    });
  }

  // Flash messages are in the document flow; still fade them after a while.
  document.querySelectorAll(".msg").forEach(function (msg) {
    setTimeout(function () { msg.remove(); }, 8000);
  });
})();