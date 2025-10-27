document.addEventListener('DOMContentLoaded', function () {
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

  // Assign reliable IDs to all headers if missing
  document.querySelectorAll('h1, h2, h3, h4, h5, h6').forEach(header => {
    if (!header.id) {
      header.id = githubSlug(header.textContent);
    }
  });

  // TOC anchor link handling (prevent crash on bad targets)
  document.querySelectorAll('a[href^="#"]').forEach(link => {
    const targetId = link.getAttribute('href').slice(1);
    const target = document.getElementById(targetId);
    if (target) {
      link.addEventListener('click', function (e) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth' });
        history.pushState(null, null, `#${targetId}`);
      });
    } else {
      console.warn(`Broken TOC link: #${targetId}`);
    }
  });

  // IntersectionObserver polyfill check and fallback
  if (!('IntersectionObserver' in window)) {
    console.warn('IntersectionObserver not supported, using fallback');
    // Fallback: show all elements immediately
    document.querySelectorAll('h1, h2, h3, .glass, div[align="center"]:has(img)').forEach((el) => {
      el.style.opacity = 1;
      el.style.transform = 'translateY(0)';
    });
    return;
  }

  // Optimize: Only animate major sections instead of every element
  const sections = document.querySelectorAll(
    'h1, h2, h3, .glass, div[align="center"]:has(img)'
  );

  // Animate sections on scroll with unobserve after reveal
  const reveal = (el, observer) => {
    el.style.opacity = 1;
    el.style.transform = 'translateY(0)';
    // Unobserve after revealing to prevent memory leaks
    observer.unobserve(el);
  };

  const animationObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        reveal(entry.target, observer);
      }
    });
  }, { 
    threshold: 0.1,
    rootMargin: '50px' // Start animation slightly before element enters viewport
  });

  sections.forEach((el) => {
    el.style.opacity = 0;
    el.style.transform = 'translateY(50px)';
    el.style.transition = 'opacity 0.5s ease-out, transform 0.5s ease-out';
    animationObserver.observe(el);
  });

  // Lazy load images with IntersectionObserver
  const lazyImages = document.querySelectorAll('img[src]');
  
  const imageObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const img = entry.target;
        
        // Add loading state
        img.style.opacity = '0';
        img.style.transition = 'opacity 0.3s ease-in';
        
        // Create a temporary image to load in background
        const tempImg = new Image();
        tempImg.onload = () => {
          img.style.opacity = '1';
          img.classList.add('loaded');
        };
        tempImg.onerror = () => {
          console.warn('Failed to load image:', img.src);
          img.style.opacity = '0.5';
          img.alt = img.alt || 'Failed to load image';
        };
        
        // Start loading
        if (img.dataset.src) {
          tempImg.src = img.dataset.src;
          img.src = img.dataset.src;
        } else {
          tempImg.src = img.src;
        }
        
        // Stop observing this image
        observer.unobserve(img);
      }
    });
  }, {
    rootMargin: '200px', // Start loading 200px before image enters viewport
    threshold: 0.01
  });

  lazyImages.forEach((img) => {
    imageObserver.observe(img);
  });

  // Cleanup observers on page unload to prevent memory leaks
  window.addEventListener('beforeunload', () => {
    animationObserver.disconnect();
    imageObserver.disconnect();
  });
});
