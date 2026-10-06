// Coordinator's forecast badge: reads forecast.json and shows the current estimate in the header.
(function () {
  var host = document.getElementById('forecast');
  if (!host) return;
  var pct = function (p) { return (p * 100).toFixed(p < 0.1 ? 0 : 0) + '%'; };
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]; }); };

  fetch('forecast.json?t=' + Date.now()).then(function (r) { return r.json(); }).then(function (f) {
    var hist = (f.history || []).map(function (h) { return '<li><b>' + pct(h.p) + '</b> · ' + esc(h.time.slice(0, 16).replace('T', ' ')) + ' · ' + esc(h.note) + '</li>'; }).join('');
    var comps = (f.components || []).map(function (c) { return '<li><b>' + pct(c.p) + '</b> ' + esc(c.label) + '</li>'; }).join('');
    var list = function (a) { return (a || []).map(function (s) { return '<li>' + esc(s) + '</li>'; }).join(''); };
    host.innerHTML =
      '<button type="button" class="forecast-chip" aria-expanded="false" title="' + esc(f.question) + '">' +
      '<span class="forecast-label">Solve as planned</span><span class="forecast-value">' + pct(f.probability) + '</span></button>' +
      '<div class="forecast-pop" hidden>' +
      '<p class="forecast-q">' + esc(f.question) + '</p>' +
      '<p class="forecast-by">' + esc(f.by) + ' · updated ' + esc(f.updated.slice(0, 16).replace('T', ' ')) + '</p>' +
      '<h4>Components</h4><ul>' + comps + '</ul>' +
      '<h4>Evidence for</h4><ul>' + list(f.evidence_for) + '</ul>' +
      '<h4>Evidence against</h4><ul>' + list(f.evidence_against) + '</ul>' +
      '<h4>History</h4><ul>' + hist + '</ul></div>';
    var btn = host.querySelector('.forecast-chip'), pop = host.querySelector('.forecast-pop');
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = pop.hidden; pop.hidden = !open; btn.setAttribute('aria-expanded', String(open));
    });
    document.addEventListener('click', function (e) { if (!host.contains(e.target)) { pop.hidden = true; btn.setAttribute('aria-expanded', 'false'); } });
  }).catch(function () { host.hidden = true; });
})();

// Dashboard mode: poll the ledger and reload when a new revision lands.
(function () {
  var start = null;
  function poll() {
    fetch('planning.json?t=' + Date.now()).then(function (r) { return r.json(); }).then(function (d) {
      if (start === null) { start = d.revision; return; }
      if (d.revision !== start) location.reload();
    }).catch(function () {});
  }
  poll();
  setInterval(poll, 60000);
})();
