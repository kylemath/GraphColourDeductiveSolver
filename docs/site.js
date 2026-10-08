(function () {
  'use strict';

  // Hash router for the app shell. Each page in the side nav is a link with
  // data-route (and data-src for pages shown in a frame). Only the selected
  // page is shown; frames are created on first visit and the few most recent
  // are kept alive so their state survives switching back and forth.

  var MAX_LIVE_FRAMES = 4;

  // Old anchors from the single-page layout, and a few friendly synonyms.
  var ALIASES = {
    play: 'writing/long-table',
    'long-table': 'writing/long-table',
    afternoon: 'writing/afternoon-call',
    vacancy: 'writing/vacancy',
    poem: 'writing/fifth-degree',
    inspiration: 'writing/fever-dream',
    story: 'writing/fever-dream',
    proof: 'navigator',
    '66666': 'six-ring',
    'spin-glass': 'physics',
    'wrapping-the-sphere': 'wrap'
  };

  var body = document.body;
  var main = document.getElementById('main');
  var overview = document.querySelector('[data-page="overview"]');
  var viewer = document.querySelector('[data-page="viewer"]');
  var viewerTitle = document.getElementById('viewer-title');
  var viewerSub = viewer.querySelector('.viewer-sub');
  var viewerOpen = viewer.querySelector('.viewer-open');
  var framesBox = viewer.querySelector('.frames');
  var current = document.querySelector('.nav-current');
  var toggle = document.querySelector('.menu-toggle');
  var sideNav = document.getElementById('side-nav');
  var scrim = document.querySelector('.nav-scrim');

  var links = Array.prototype.slice.call(sideNav.querySelectorAll('a[data-route]'));
  var pages = {};
  links.forEach(function (link) {
    pages[link.dataset.route] = {
      route: link.dataset.route,
      link: link,
      src: link.dataset.src || null,
      title: link.dataset.title || link.textContent.trim(),
      sub: link.dataset.sub || '',
      frameTitle: link.dataset.frameTitle || link.dataset.title || link.textContent.trim()
    };
  });

  var frames = {};   // route -> element (iframe or placeholder)
  var lru = [];      // most recent last
  var siteTitle = document.title;

  function parseHash() {
    var raw = decodeURIComponent(location.hash.replace(/^#/, ''));
    if (!raw) return { route: 'overview', rest: '' };
    var slash = raw.indexOf('/');
    var head = slash < 0 ? raw : raw.slice(0, slash);
    var rest = slash < 0 ? '' : raw.slice(slash + 1);
    if (ALIASES[head]) {
      var target = ALIASES[head] + (rest ? '/' + rest : '');
      history.replaceState(null, '', '#' + target);
      return parseHash();
    }
    if (!pages[head]) return { route: 'overview', rest: '' };
    return { route: head, rest: rest };
  }

  function touch(route) {
    lru = lru.filter(function (r) { return r !== route; });
    lru.push(route);
    while (lru.length > MAX_LIVE_FRAMES) {
      var old = lru.shift();
      if (frames[old]) {
        frames[old].remove();
        delete frames[old];
      }
    }
  }

  function placeholder(page) {
    var box = document.createElement('div');
    box.className = 'frame placeholder-frame';
    box.innerHTML = '<div class="placeholder"><h3></h3><p>This page is still being built. Check back soon, or try the <a href="">direct link</a>.</p></div>';
    box.querySelector('h3').textContent = page.title;
    box.querySelector('a').href = page.src;
    box.style.overflow = 'auto';
    return box;
  }

  function makeFrame(page, rest) {
    var frame = document.createElement('iframe');
    frame.className = 'frame';
    frame.title = page.frameTitle;
    frame.src = page.src + (rest ? '#' + encodeURIComponent(rest) : '');
    return frame;
  }

  // Create the frame for a page. If the page is missing (for example a demo
  // that has not been published yet) show a short note instead of a 404.
  function ensureFrame(page, rest) {
    if (frames[page.route]) return;
    var frame = makeFrame(page, rest);
    frames[page.route] = frame;
    framesBox.appendChild(frame);
    if (window.fetch && location.protocol !== 'file:') {
      fetch(page.src, { method: 'HEAD' }).then(function (res) {
        if (res.ok || frames[page.route] !== frame) return;
        var note = placeholder(page);
        note.hidden = frame.hidden;
        frame.replaceWith(note);
        frames[page.route] = note;
      }).catch(function () {});
    }
  }

  function setSubAnchor(page, rest) {
    var frame = frames[page.route];
    if (!frame || frame.tagName !== 'IFRAME' || !rest) return;
    try {
      var win = frame.contentWindow;
      // Use an absolute URL: a bare '#x' would resolve against this page.
      var target = new URL(page.src + '#' + encodeURIComponent(rest), location.href);
      if (win && win.location.pathname === target.pathname) {
        if (win.location.hash !== target.hash) win.location.replace(target.href);
      } else {
        frame.src = target.href;
      }
    } catch (err) { /* cross-origin: ignore */ }
  }

  function render(moveFocus) {
    var state = parseHash();
    var page = pages[state.route];

    links.forEach(function (link) {
      if (link.dataset.route === state.route) link.setAttribute('aria-current', 'page');
      else link.removeAttribute('aria-current');
    });

    Object.keys(frames).forEach(function (r) { frames[r].hidden = r !== state.route; });

    if (state.route === 'overview' || !page.src) {
      overview.hidden = false;
      viewer.hidden = true;
      main.classList.remove('is-viewer');
      current.textContent = '';
      document.title = siteTitle;
      if (moveFocus) main.focus({ preventScroll: true });
    } else {
      overview.hidden = true;
      viewer.hidden = false;
      main.classList.add('is-viewer');
      viewerTitle.textContent = page.title;
      viewerSub.textContent = page.sub;
      viewerOpen.href = page.src + (state.rest ? '#' + encodeURIComponent(state.rest) : '');
      current.textContent = page.title;
      document.title = page.title + ' — Graph Colour';
      var existed = !!frames[page.route];
      ensureFrame(page, state.rest);
      frames[page.route].hidden = false;
      if (existed) setSubAnchor(page, state.rest);
      touch(page.route);
      if (moveFocus) viewerTitle.focus({ preventScroll: true });
    }
    closeNav(false);
  }

  // Mobile drawer --------------------------------------------------------------

  function openNav() {
    body.classList.add('nav-open');
    toggle.setAttribute('aria-expanded', 'true');
    scrim.hidden = false;
    var active = sideNav.querySelector('[aria-current="page"]') || sideNav.querySelector('a');
    if (active) window.setTimeout(function () { active.focus(); }, 0);
  }

  function closeNav(returnFocus) {
    if (!body.classList.contains('nav-open')) return;
    body.classList.remove('nav-open');
    toggle.setAttribute('aria-expanded', 'false');
    scrim.hidden = true;
    if (returnFocus) toggle.focus();
  }

  toggle.addEventListener('click', function () {
    if (body.classList.contains('nav-open')) closeNav(true);
    else openNav();
  });
  scrim.addEventListener('click', function () { closeNav(true); });
  document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape' && body.classList.contains('nav-open')) closeNav(true);
  });

  // Clicking the link for the page already shown still closes the drawer.
  sideNav.addEventListener('click', function (event) {
    if (event.target.closest('a')) closeNav(false);
  });

  window.addEventListener('hashchange', function () { render(true); });
  render(false);
})();
