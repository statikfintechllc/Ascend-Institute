document.addEventListener('DOMContentLoaded', function () {
  const sections = document.querySelectorAll('h2, h3, h4, p, ul, ol, img, code, pre');

  const reveal = (el) => {
    el.style.opacity = 1;
    el.style.transform = 'translateY(0)';
  };

  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        reveal(entry.target);
      }
    });
  }, { threshold: 0.1 });

  sections.forEach(el => {
    el.style.opacity = 0;
    el.style.transform = 'translateY(50px)';
    el.style.transition = 'all 0.5s ease-out';
    observer.observe(el);
  });
});
