document.addEventListener('DOMContentLoaded', function () {
  const sections = document.querySelectorAll(
    'h1, h2, h3, h4, h5, h6, p, ul, ol, img, code, pre, .glass'
  );

  // GitHub-style slug generator
  function githubSlug(text) {
    return text
      .trim()
      .toLowerCase()
      .replace(/[\s+]+/g, '-')              // spaces to hyphens
      .replace(/[^a-z0-9\-]/g, '')          // remove non-alphanumeric
      .replace(/\-+/g, '-')                 // collapse dashes
      .replace(/^\-+|\-+$/g, '');           // trim leading/trailing hyphens
  }

  // Assign reliable IDs to all headers
  document.querySelectorAll('h1, h2, h3, h4, h5, h6').forEach(header => {
    if (!header.id) {
      header.id = githubSlug(header.textContent);
    }
  });

  // Check for broken TOC links
  document.querySelectorAll('a[href^="#"]').forEach(link => {
    const targetId = link.getAttribute('href');
    if (!document.querySelector(targetId)) {
      console.warn(Broken TOC link: ${targetId});
    }
  });

  // Animate sections on scroll
  const reveal = (el) => {
    el.style.opacity = 1;
    el.style.transform = 'translateY(0)';
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        reveal(entry.target);
      }
    });
  }, { threshold: 0.1 });

  sections.forEach((el) => {
    el.style.opacity = 0;
    el.style.transform = 'translateY(50px)';
    el.style.transition = 'all 0.5s ease-out';
    observer.observe(el);
  });
});
