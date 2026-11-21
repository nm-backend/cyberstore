/* CyberStore — interaction layer: mobile search, reveal-on-scroll,
   installment calculator, loading state for catalog filters. */
(function () {
  "use strict";

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------------- Mobile search ---------------- */
  var searchToggle = document.querySelector("[data-search-toggle]");
  var searchPanel = document.querySelector("[data-mobile-search]");

  function setSearch(open) {
    if (!searchPanel || !searchToggle) return;
    searchPanel.hidden = !open;
    searchToggle.setAttribute("aria-expanded", String(open));
    searchToggle.classList.toggle("is-active", open);
    searchToggle.setAttribute("aria-label", open ? "Закрыть поиск" : "Открыть поиск");
    if (open) {
      var input = searchPanel.querySelector("input[type='search']");
      if (input) setTimeout(function () { input.focus(); }, 40);
    }
  }

  if (searchToggle && searchPanel) {
    searchToggle.addEventListener("click", function () {
      setSearch(searchPanel.hidden);
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && !searchPanel.hidden) setSearch(false);
    });
  }

  /* ---------------- Reveal on scroll ---------------- */
  var revealSelectors = [
    ".section", ".catalog-page-head", ".category-tiles-section",
    ".cat-box", ".card", ".category-tile", ".flow-step", ".calc-box",
    ".zone-card", ".plan-card", ".trust-card-m", ".contact-card",
    ".use-case-card", ".modern-banner", ".home-contacts-row", ".quick-link-card"
  ];

  var targets = Array.prototype.slice.call(
    document.querySelectorAll(revealSelectors.join(","))
  );

  if (targets.length && !reduceMotion && "IntersectionObserver" in window) {
    var seen = 0;
    targets.forEach(function (el) {
      if (el.closest(".hero-home")) return; // hero has its own entrance
      el.setAttribute("data-reveal", "");
      var siblings = Array.prototype.filter.call(el.parentNode.children, function (node) {
        return node.hasAttribute("data-reveal");
      });
      var index = siblings.indexOf(el);
      if (index > 0) el.style.setProperty("--reveal-delay", Math.min(index, 6) * 45 + "ms");
      seen += 1;
    });

    if (seen) {
      var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-in");
          observer.unobserve(entry.target);
        });
      }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });

      Array.prototype.forEach.call(
        document.querySelectorAll("[data-reveal]"),
        function (el) { observer.observe(el); }
      );
    }
  }

  /* ---------------- Installment calculator ---------------- */
  var calc = document.querySelector("[data-calculator]");
  if (calc) {
    var priceInput = calc.querySelector("[data-calc-price]");
    var termSelect = calc.querySelector("[data-calc-term]");
    var monthlyOut = calc.querySelector("[data-calc-monthly]");
    var waLink = calc.querySelector("[data-calc-wa]");

    var format = function (value) {
      return String(value).replace(/\B(?=(\d{3})+(?!\d))/g, " ") + " сом";
    };

    var recalc = function () {
      var price = parseInt(priceInput && priceInput.value, 10);
      var term = parseInt(termSelect && termSelect.value, 10);
      if (!price || price < 0 || !term) {
        if (monthlyOut) monthlyOut.textContent = "—";
        return;
      }
      var monthly = Math.round(price / term);
      if (monthlyOut) monthlyOut.textContent = format(monthly);
      if (waLink) {
        try {
          var url = new URL(waLink.href);
          url.searchParams.set(
            "text",
            "Здравствуйте! Хочу оформить рассрочку: " + format(price) +
              ", срок " + term + " мес., платёж около " + format(monthly) + "."
          );
          waLink.href = url.toString();
        } catch (error) { /* keep the template link */ }
      }
    };

    if (priceInput) priceInput.addEventListener("input", recalc);
    if (termSelect) termSelect.addEventListener("change", recalc);
    recalc();
  }

  /* ---------------- Catalog: loading state ---------------- */
  var filterForm = document.querySelector("[data-filter-form]");
  var results = document.querySelector(".catalog-results");
  if (filterForm && results) {
    filterForm.addEventListener("submit", function () {
      results.classList.add("is-loading");
    });
  }

  /* ---------------- Filters: selected count on the mobile button ---------------- */
  var filterToggle = document.querySelector("[data-filter-toggle]");
  if (filterForm && filterToggle) {
    var updateFilterCount = function () {
      var boxes = filterForm.querySelectorAll("input[type='checkbox']:checked").length;
      var prices = ["price_min", "price_max"].filter(function (name) {
        var field = filterForm.querySelector("input[name='" + name + "']");
        return field && field.value.trim() !== "";
      }).length;
      var total = boxes + prices;
      filterToggle.classList.toggle("has-active", total > 0);
      if (total > 0) filterToggle.setAttribute("data-active-count", String(total));
      else filterToggle.removeAttribute("data-active-count");
    };
    filterForm.addEventListener("change", updateFilterCount);
    filterForm.addEventListener("input", updateFilterCount);
    updateFilterCount();
  }

  /* ---------------- Product: room for the sticky purchase bar ---------------- */
  if (document.querySelector("[data-buy-bar]")) {
    document.body.classList.add("has-buy-bar");
  }
})();
