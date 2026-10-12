(function () {
  'use strict';

  // The Writing reader pulls each piece's own published page into this one,
  // keeps its text and markup as they are, scopes its stylesheet to the
  // piece, and builds a side outline from the headings.

  var PIECES = [
    { id: 'long-table', kind: 'Play', src: '../play/index.html' },
    { id: 'afternoon-call', kind: 'Play', src: '../play/afternoon.html' },
    { id: 'vacancy', kind: 'Play', src: '../play/vacancy.html' },
    { id: 'fifth-degree', kind: 'Poem', src: '../poem/index.html' },
    { id: 'fever-dream', kind: 'Story', src: '../story/index.html' }
  ];

  var piecesBox = document.querySelector('.pieces');
  var outlineList = document.querySelector('.outline-list');
  var outline = document.getElementById('outline');
  var toggle = document.querySelector('.outline-toggle');
  var where = document.querySelector('.where');
  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var framed = false;
  try { framed = window.self !== window.top; } catch (err) { framed = true; }
  if (!framed) document.querySelector('.home-link').hidden = false;

  PIECES.forEach(function (p) { p.url = new URL(p.src, location.href); });

  function pieceForUrl(url) {
    for (var i = 0; i < PIECES.length; i++) {
      if (PIECES[i].url.pathname === url.pathname) return PIECES[i];
    }
    return null;
  }

  function slug(text) {
    return text.toLowerCase().replace(/[’']/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '') || 'section';
  }

  // ---- CSS scoping -----------------------------------------------------------

  function scopeSelector(sel, scope) {
    sel = sel.trim();
    sel = sel.replace(/^(?:html|:root)\s+body(?![\w-])/, 'body');
    var m = sel.match(/^(:root|html|body)(?![\w-])/);
    if (m) return scope + sel.slice(m[0].length);
    return scope + ' ' + sel;
  }

  function splitSelectors(text) {
    // Split on top-level commas only (commas inside :is(), :not() etc. stay).
    var out = [], depth = 0, start = 0;
    for (var i = 0; i < text.length; i++) {
      var c = text[i];
      if (c === '(') depth++;
      else if (c === ')') depth--;
      else if (c === ',' && depth === 0) { out.push(text.slice(start, i)); start = i + 1; }
    }
    out.push(text.slice(start));
    return out;
  }

  function scopeRules(rules, scope) {
    var out = '';
    for (var i = 0; i < rules.length; i++) {
      var r = rules[i];
      if (r.type === 1) { // style rule
        var sels = splitSelectors(r.selectorText).map(function (s) { return scopeSelector(s, scope); });
        out += sels.join(', ') + ' { ' + r.style.cssText + ' }\n';
      } else if (r.type === 4) { // media
        out += '@media ' + r.media.mediaText + ' {\n' + scopeRules(r.cssRules, scope) + '}\n';
      } else if (r.type === 12) { // supports
        out += '@supports ' + r.conditionText + ' {\n' + scopeRules(r.cssRules, scope) + '}\n';
      } else if (r.type === 3) {
        // @import: skip
      } else {
        out += r.cssText + '\n';
      }
    }
    return out;
  }

  function scopeCss(cssText, scope) {
    var probe = document.createElement('style');
    probe.media = 'not all';
    probe.textContent = cssText;
    document.head.appendChild(probe);
    var result = '';
    try { result = scopeRules(probe.sheet.cssRules, scope); } catch (err) { result = ''; }
    probe.remove();
    return result;
  }

  function collectCss(doc, baseUrl) {
    var parts = [];
    doc.querySelectorAll('style, link[rel="stylesheet"]').forEach(function (el) {
      if (el.tagName === 'STYLE') {
        parts.push(Promise.resolve(el.textContent));
      } else {
        var href = new URL(el.getAttribute('href'), baseUrl);
        if (href.origin !== location.origin) return; // third-party themes are left out
        parts.push(fetch(href).then(function (r) { return r.ok ? r.text() : ''; }).catch(function () { return ''; }));
      }
    });
    return Promise.all(parts).then(function (list) { return list.join('\n'); });
  }

  // ---- Content preparation ---------------------------------------------------

  function prepare(piece, doc) {
    var base = piece.url;
    var root = document.createElement('div');
    root.className = 'piece-body';
    root.setAttribute('data-scope', piece.id);

    Array.prototype.slice.call(doc.body.childNodes).forEach(function (node) {
      if (node.nodeType === 1 && node.tagName === 'SCRIPT') return;
      root.appendChild(document.importNode(node, true));
    });
    root.querySelectorAll('script').forEach(function (s) { s.remove(); });

    // Interactive parts are replaced by a link to the original page.
    root.querySelectorAll('.interactive-module').forEach(function (mod) {
      var h = mod.querySelector('h1, h2, h3, h4');
      var desc = mod.querySelector('.module-desc, p');
      var card = document.createElement('aside');
      card.className = 'interactive-link';
      var kind = document.createElement('span');
      kind.className = 'kind';
      kind.textContent = 'Interactive';
      card.appendChild(kind);
      var title = document.createElement('h3');
      title.textContent = h ? h.textContent.trim() : 'Interactive simulation';
      card.appendChild(title);
      if (desc && desc.textContent.trim()) {
        var p = document.createElement('p');
        p.textContent = desc.textContent.trim();
        card.appendChild(p);
      }
      var link = document.createElement('a');
      link.href = piece.src;
      if (framed) link.target = '_top';
      link.textContent = 'Open the interactive version on the original page →';
      var lp = document.createElement('p');
      lp.appendChild(link);
      card.appendChild(lp);
      mod.replaceWith(card);
    });

    // Make every id unique across the reader.
    var prefix = piece.id + '--';
    root.querySelectorAll('[id]').forEach(function (el) { el.id = prefix + el.id; });
    root.querySelectorAll('[for], [aria-labelledby], [aria-describedby], [aria-controls]').forEach(function (el) {
      ['for', 'aria-labelledby', 'aria-describedby', 'aria-controls'].forEach(function (attr) {
        var v = el.getAttribute(attr);
        if (v) el.setAttribute(attr, v.split(/\s+/).map(function (x) { return prefix + x; }).join(' '));
      });
    });

    // Links: in-page anchors get the prefix, links to another piece jump to
    // it here, everything else resolves against the piece's own address.
    root.querySelectorAll('a[href]').forEach(function (a) {
      var href = a.getAttribute('href');
      if (href.charAt(0) === '#') {
        if (href.length > 1) a.setAttribute('href', '#' + prefix + href.slice(1));
        return;
      }
      var url;
      try { url = new URL(href, base); } catch (err) { return; }
      var other = url.origin === location.origin ? pieceForUrl(url) : null;
      if (other) {
        a.setAttribute('href', '#' + (url.hash ? other.id + '--' + url.hash.slice(1) : other.id));
      } else {
        a.setAttribute('href', url.href);
        if (framed && url.origin === location.origin) a.target = '_top';
      }
    });
    root.querySelectorAll('[src]').forEach(function (el) {
      el.setAttribute('src', new URL(el.getAttribute('src'), base).href);
    });

    // Headings for the outline.
    var heads = [];
    var used = {};
    root.querySelectorAll('[id]').forEach(function (el) { used[el.id] = true; });
    function ensureId(el, text) {
      if (el.id) return el.id;
      var id = prefix + slug(text), n = 2;
      while (used[id] || document.getElementById(id)) id = prefix + slug(text) + '-' + n++;
      used[id] = true;
      el.id = id;
      return id;
    }
    var h1 = root.querySelector('h1');
    var title = h1 ? h1.textContent.trim() : doc.title;
    var subs = root.querySelectorAll('h2, h3');
    subs.forEach(function (h) {
      var text = h.textContent.trim();
      if (!text) return;
      if (h.closest('nav')) return;
      heads.push({ el: h, id: ensureId(h, text), text: text, level: h.tagName === 'H2' ? 1 : 2 });
    });
    // A story with no section headings: use its scene directions as stops.
    if (!root.querySelector('h2')) {
      var scenes = root.querySelectorAll('.scene-direction');
      var extra = [];
      scenes.forEach(function (el, i) {
        var words = el.textContent.replace(/^[\s*(]+/, '').split(/\s+/).slice(0, 7).join(' ');
        extra.push({ el: el, id: ensureId(el, 'scene-' + (i + 1)), text: words.replace(/[.,;:]+$/, '') + '…', level: 1 });
      });
      heads = heads.concat(extra);
      heads.sort(function (a, b) {
        return a.el.compareDocumentPosition(b.el) & Node.DOCUMENT_POSITION_FOLLOWING ? -1 : 1;
      });
    }
    return { root: root, title: title, heads: heads };
  }

  // ---- Rendering -------------------------------------------------------------

  var entries = []; // {id, el, link, pieceItem, text}

  function buildPieceShell(piece) {
    var section = document.createElement('section');
    section.className = 'piece';
    section.id = piece.id;
    section.setAttribute('aria-label', piece.kind);
    var meta = document.createElement('div');
    meta.className = 'piece-meta';
    meta.innerHTML = '<span class="kind"></span><a>Open the original page</a>';
    meta.querySelector('.kind').textContent = piece.kind;
    var orig = meta.querySelector('a');
    orig.href = piece.src;
    if (framed) orig.target = '_top';
    section.appendChild(meta);
    var status = document.createElement('p');
    status.className = 'piece-status';
    status.textContent = 'Loading…';
    section.appendChild(status);
    piecesBox.appendChild(section);

    var item = document.createElement('li');
    item.className = 'o-piece';
    var link = document.createElement('a');
    link.className = 'o-link';
    link.href = '#' + piece.id;
    link.innerHTML = '<span class="o-kind"></span><span class="o-title"></span>';
    link.querySelector('.o-kind').textContent = piece.kind;
    link.querySelector('.o-title').textContent = piece.id;
    item.appendChild(link);
    outlineList.appendChild(item);
    piece.section = section;
    piece.status = status;
    piece.item = item;
    piece.link = link;
  }

  function fillPiece(piece, data, css) {
    var style = document.createElement('style');
    style.textContent = scopeCss(css, '[data-scope="' + piece.id + '"]');
    document.head.appendChild(style);
    piece.status.remove();
    piece.section.appendChild(data.root);
    piece.section.setAttribute('aria-label', data.title);
    piece.link.querySelector('.o-title').textContent = data.title;

    var sub = document.createElement('ol');
    data.heads.forEach(function (h) {
      var li = document.createElement('li');
      li.className = 'lvl-' + h.level;
      var a = document.createElement('a');
      a.className = 'o-link';
      a.href = '#' + h.id;
      a.textContent = h.text;
      li.appendChild(a);
      sub.appendChild(li);
      h.link = a;
      h.piece = piece;
    });
    piece.item.appendChild(sub);
    piece.heads = data.heads;
    piece.title = data.title;
  }

  function failPiece(piece) {
    piece.status.innerHTML = 'This piece could not be loaded here. <a>Read it on its own page</a>.';
    piece.status.querySelector('a').href = piece.src;
    piece.link.querySelector('.o-title').textContent = piece.id.replace(/-/g, ' ');
  }

  function rebuildEntries() {
    entries = [];
    PIECES.forEach(function (p) {
      entries.push({ id: p.id, el: p.section, link: p.link, piece: p, text: p.title || p.id });
      (p.heads || []).forEach(function (h) {
        entries.push({ id: h.id, el: h.el, link: h.link, piece: p, text: h.text });
      });
    });
  }

  // ---- Scroll-spy ------------------------------------------------------------

  var activeEntry = null;
  var ticking = false;
  var hashTimer = null;

  function barHeight() {
    var bar = document.querySelector('.bar');
    return bar && getComputedStyle(bar).display !== 'none' ? bar.offsetHeight : 0;
  }

  function spy() {
    ticking = false;
    if (!entries.length) return;
    var line = barHeight() + Math.min(120, window.innerHeight * 0.25);
    var found = entries[0];
    for (var i = 0; i < entries.length; i++) {
      if (entries[i].el.getBoundingClientRect().top <= line) found = entries[i];
      else break;
    }
    // At the very bottom, the last heading wins even if it cannot reach the line.
    if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 2) {
      found = entries[entries.length - 1];
    }
    if (window.scrollY < 40) found = null;
    setActive(found);
  }

  function setActive(entry) {
    if (entry === activeEntry) return;
    if (activeEntry) activeEntry.link.classList.remove('is-active');
    PIECES.forEach(function (p) { p.item.classList.toggle('is-current', !!entry && entry.piece === p); });
    activeEntry = entry;
    if (!entry) {
      where.textContent = '';
      return;
    }
    entry.link.classList.add('is-active');
    entry.link.setAttribute('aria-current', 'location');
    outlineList.querySelectorAll('[aria-current]').forEach(function (a) {
      if (a !== entry.link) a.removeAttribute('aria-current');
    });
    var pieceTitle = entry.piece.title || '';
    where.textContent = entry.el === entry.piece.section ? pieceTitle : pieceTitle + ' · ' + entry.text;
    keepVisible(entry.link);
    window.clearTimeout(hashTimer);
    hashTimer = window.setTimeout(function () {
      if (history.replaceState && location.hash !== '#' + entry.id) history.replaceState(null, '', '#' + entry.id);
    }, 400);
  }

  function keepVisible(link) {
    var box = outline.getBoundingClientRect();
    var r = link.getBoundingClientRect();
    var margin = 48;
    if (r.top < box.top + margin) outline.scrollTop -= (box.top + margin - r.top);
    else if (r.bottom > box.bottom - margin) outline.scrollTop += (r.bottom - (box.bottom - margin));
  }

  window.addEventListener('scroll', function () {
    if (!ticking) { ticking = true; window.setTimeout(spy, 60); }
  }, { passive: true });
  window.addEventListener('resize', function () { spy(); });

  // ---- Navigation ------------------------------------------------------------

  function jumpToHash(smooth) {
    var id = decodeURIComponent(location.hash.slice(1));
    if (!id) return;
    var el = document.getElementById(id);
    if (!el) return;
    el.scrollIntoView({ behavior: smooth && !reduceMotion ? 'smooth' : 'instant', block: 'start' });
  }

  window.addEventListener('hashchange', function () { jumpToHash(true); });

  outlineList.addEventListener('click', function (event) {
    var a = event.target.closest('a.o-link');
    if (!a) return;
    var target = document.getElementById(a.getAttribute('href').slice(1));
    if (target) {
      // Move keyboard focus with the jump so Tab continues from the section.
      if (!target.hasAttribute('tabindex')) target.setAttribute('tabindex', '-1');
      window.setTimeout(function () { target.focus({ preventScroll: true }); }, 0);
    }
    closeOutline(false);
  });

  // ---- Mobile outline drawer ---------------------------------------------------

  function openOutline() {
    document.body.classList.add('outline-open');
    toggle.setAttribute('aria-expanded', 'true');
    var a = outlineList.querySelector('.is-active') || outlineList.querySelector('a');
    if (a) window.setTimeout(function () { a.focus(); keepVisible(a); }, 0);
  }

  function closeOutline(returnFocus) {
    if (!document.body.classList.contains('outline-open')) return;
    document.body.classList.remove('outline-open');
    toggle.setAttribute('aria-expanded', 'false');
    if (returnFocus) toggle.focus();
  }

  toggle.addEventListener('click', function () {
    if (document.body.classList.contains('outline-open')) closeOutline(true);
    else openOutline();
  });
  document.querySelector('.scrim').addEventListener('click', function () { closeOutline(true); });
  document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape') closeOutline(true);
  });

  // ---- Load ------------------------------------------------------------------

  PIECES.forEach(buildPieceShell);

  var loads = PIECES.map(function (piece) {
    return fetch(piece.url)
      .then(function (res) {
        if (!res.ok) throw new Error(res.status);
        return res.text();
      })
      .then(function (html) {
        var doc = new DOMParser().parseFromString(html, 'text/html');
        return collectCss(doc, piece.url).then(function (css) {
          fillPiece(piece, prepare(piece, doc), css);
        });
      })
      .catch(function () { failPiece(piece); });
  });

  Promise.all(loads).then(function () {
    rebuildEntries();
    // Let the injected styles apply before measuring.
    window.setTimeout(function () {
      jumpToHash(false);
      spy();
      // Images above the target can shift it while they load: re-align once
      // or twice, unless the reader has started scrolling.
      if (location.hash) {
        var y = window.scrollY;
        [500, 1500].forEach(function (ms) {
          window.setTimeout(function () {
            if (window.scrollY !== y) return;
            jumpToHash(false);
            y = window.scrollY;
          }, ms);
        });
      }
    }, 0);
  });
})();
