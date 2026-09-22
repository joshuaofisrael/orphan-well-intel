(function () {
  var form = document.getElementById("access-form");
  if (form) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
    });
  }

  var formBtn = document.getElementById("access-submit");
  var formResult = document.getElementById("form-result");
  if (formBtn && formResult) {
    var params = new URLSearchParams(window.location.search);
    var tier = params.get("tier");
    if (tier) {
      var choice = document.querySelector('input[type="radio"][value="' + tier + '"]');
      if (choice) choice.checked = true;
    }

    formBtn.addEventListener("click", function () {
      var ack = document.getElementById("ack");
      formResult.hidden = false;
      if (!ack || !ack.checked) {
        formResult.textContent = "Nothing was sent. Check the acknowledgement to finish this preview. This form does not email anyone or store what you typed.";
        return;
      }
      formResult.textContent = "Nothing was sent. No email was created, and nothing was stored in this browser. Access requests will be collected after Stripe is connected. Checkout is not available on this site.";
      var form = document.getElementById("access-form");
      if (form) form.reset();
    });
  }

  var filters = document.querySelectorAll("[data-filter]");
  var rows = document.querySelectorAll("tr[data-states]");
  var countEl = document.getElementById("filter-count");
  var emptyEl = document.getElementById("filter-empty");
  var search = document.getElementById("company-search");
  if (!filters.length || !rows.length) return;

  var active = "all";
  var query = "";

  function apply() {
    var shown = 0;
    rows.forEach(function (row) {
      var states = (row.getAttribute("data-states") || "").split(/\s+/);
      var name = (row.getAttribute("data-name") || "").toLowerCase();
      var stateOk = active === "all" || states.indexOf(active) !== -1;
      var textOk = !query || name.indexOf(query) !== -1;
      var show = stateOk && textOk;
      row.hidden = !show;
      if (show) shown += 1;
    });
    if (countEl) {
      countEl.textContent = shown + (shown === 1 ? " company shown" : " companies shown");
    }
    if (emptyEl) emptyEl.hidden = shown !== 0;
  }

  filters.forEach(function (btn) {
    btn.addEventListener("click", function () {
      active = btn.getAttribute("data-filter") || "all";
      filters.forEach(function (other) {
        other.setAttribute("aria-pressed", other === btn ? "true" : "false");
      });
      apply();
    });
  });

  if (search) {
    search.addEventListener("input", function () {
      query = search.value.trim().toLowerCase();
      apply();
    });
  }
})();
