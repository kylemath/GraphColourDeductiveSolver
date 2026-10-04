(function () {
  function fitFrame(frame) {
    let doc;
    try {
      doc = frame.contentDocument;
    } catch (err) {
      return;
    }
    if (!doc || !doc.body) return;
    // Measure the body, not the root: the root never reports less than the
    // frame's current height, so a frame sized too tall could never shrink.
    const h = doc.body.scrollHeight;
    frame.style.height = (h + 4) + 'px';
  }

  function bindFrame(frame) {
    const fit = () => fitFrame(frame);
    fit();
    const doc = frame.contentDocument;
    if (!doc || !doc.body) return;
    if (window.ResizeObserver) {
      const observer = new ResizeObserver(fit);
      observer.observe(doc.body);
    }
    doc.querySelectorAll('img').forEach((img) => {
      if (!img.complete) img.addEventListener('load', fit);
    });
    window.setTimeout(fit, 250);
    window.setTimeout(fit, 1000);
  }

  document.querySelectorAll('iframe.frame-story').forEach((frame) => {
    frame.addEventListener('load', () => bindFrame(frame));
  });

  const links = Array.from(document.querySelectorAll('.site-nav nav a[href^="#"]'));
  const sections = links
    .map((link) => document.querySelector(link.getAttribute('href')))
    .filter(Boolean);

  if (window.IntersectionObserver) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        const id = '#' + entry.target.id;
        links.forEach((link) => {
          link.classList.toggle('is-active', link.getAttribute('href') === id);
        });
      });
    }, { rootMargin: '-15% 0px -70% 0px', threshold: 0 });
    sections.forEach((section) => observer.observe(section));
  }
})();
