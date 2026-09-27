(function () {
  const story = document.getElementById('story-frame');

  function fitStory() {
    let doc;
    try {
      doc = story.contentDocument;
    } catch (err) {
      return;
    }
    if (!doc || !doc.documentElement) return;
    const h = Math.max(
      doc.documentElement.scrollHeight,
      doc.body ? doc.body.scrollHeight : 0
    );
    story.style.height = (h + 4) + 'px';
  }

  function bindStory() {
    fitStory();
    const doc = story.contentDocument;
    if (!doc || !doc.body) return;
    if (window.ResizeObserver) {
      const observer = new ResizeObserver(fitStory);
      observer.observe(doc.body);
    }
    doc.querySelectorAll('img').forEach((img) => {
      if (!img.complete) img.addEventListener('load', fitStory);
    });
    window.setTimeout(fitStory, 250);
    window.setTimeout(fitStory, 1000);
  }

  story.addEventListener('load', bindStory);

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
