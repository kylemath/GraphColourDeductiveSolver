/* ========================================================
   app.js — Tab navigation & initialisation
   Agent 1012 — Four Colour Theorem Interactive Demo
   ======================================================== */

(function () {
  'use strict';

  /* --------------------------------------------------
     Tab switching
     -------------------------------------------------- */
  function switchTab(tabId) {
    document.querySelectorAll('.tab').forEach(t => {
      t.classList.toggle('active', t.dataset.tab === tabId);
      t.setAttribute('aria-selected', t.dataset.tab === tabId);
    });
    document.querySelectorAll('.tab-panel').forEach(p => {
      p.classList.toggle('active', p.id === `tab-${tabId}`);
    });

    if (!initialised[tabId]) {
      initialised[tabId] = true;
      initTab(tabId);
    }
  }

  const initialised = {};

  function initTab(tabId) {
    switch (tabId) {
      case 'intro':
        IntroDemo.init();
        break;
      case 'maps':
        DualDemo.init();
        MiniFigures.init();
        break;
      case 'euler':
        EulerDemo.init();
        break;
      case 'kempe':
        KempeDemo.init();
        break;
      case 'proof':
        DischargeDemo.init();
        break;
      case 'interactive':
        Playground.init();
        break;
    }
  }

  /* --------------------------------------------------
     Event listeners
     -------------------------------------------------- */
  document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => switchTab(tab.dataset.tab));
  });

  document.querySelectorAll('.btn-next, .btn-prev').forEach(btn => {
    btn.addEventListener('click', () => {
      switchTab(btn.dataset.next);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  });

  /* --------------------------------------------------
     Canvas high-DPI scaling
     -------------------------------------------------- */
  function scaleCanvas(canvas) {
    const dpr = window.devicePixelRatio || 1;
    const rect = canvas.getBoundingClientRect();
    if (rect.width === 0) return;
    const w = canvas.width;
    const h = canvas.height;
    canvas.style.width = w + 'px';
    canvas.style.height = h + 'px';
  }

  function scaleAllCanvases() {
    document.querySelectorAll('canvas').forEach(scaleCanvas);
  }

  /* --------------------------------------------------
     Initialise on load
     -------------------------------------------------- */
  window.addEventListener('DOMContentLoaded', () => {
    scaleAllCanvases();
    initialised['intro'] = true;
    initTab('intro');
  });

  window.addEventListener('resize', () => {
    scaleAllCanvases();
  });
})();
