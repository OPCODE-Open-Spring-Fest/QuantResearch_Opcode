// Scroll animation observer
export const initScrollAnimations = (): void => {
  if (typeof window === 'undefined') return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
      }
    });
  }, { threshold: 0.1 });

  const fadeElements = document.querySelectorAll('.fade-in-section');
  fadeElements.forEach((el) => {
    observer.observe(el);
  });
};

// Parallax effect
export const initParallax = (): void => {
  if (typeof window === 'undefined') return;

  const handleScroll = (): void => {
    const scrolled = window.pageYOffset;
    const parallaxElements = document.querySelectorAll('[data-parallax]');
    
    parallaxElements.forEach((el) => {
      const speed = parseFloat(el.getAttribute('data-parallax-speed') || '0.5');
      (el as HTMLElement).style.transform = `translateY(${scrolled * speed}px)`;
    });
  };

  window.addEventListener('scroll', handleScroll);
};

// Typewriter effect
export const initTypewriter = (element: HTMLElement, text: string, speed: number = 100): void => {
  let i = 0;
  element.innerHTML = '';

  const type = (): void => {
    if (i < text.length) {
      element.innerHTML += text.charAt(i);
      i++;
      setTimeout(type, speed);
    }
  };

  type();
};

// Initialize all animations
export const initAllAnimations = (): void => {
  if (typeof window === 'undefined') return;
  
  initScrollAnimations();
  initParallax();
  
  // Initialize typewriter effects for elements with data-typewriter attribute
  const typewriterElements = document.querySelectorAll('[data-typewriter]');
  typewriterElements.forEach((el) => {
    const text = el.getAttribute('data-typewriter') || '';
    const speed = parseInt(el.getAttribute('data-typewriter-speed') || '100');
    initTypewriter(el as HTMLElement, text, speed);
  });
};

// Cleanup function for useEffect
export const cleanupAnimations = (): void => {
  if (typeof window === 'undefined') return;
  
  // Remove scroll event listeners
  window.removeEventListener('scroll', () => {});
};