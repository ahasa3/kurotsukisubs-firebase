/**
 * KUROTSUKISUBS - Main JavaScript
 * Nogizaka46 Fansub Website
 */

'use strict';

// ============================================
// DOM Ready
// ============================================
document.addEventListener('DOMContentLoaded', function () {
  initNavbar();
  initScrollTopButton();
  initAnimations();
  initPostCards();
  initMobileMenu();
});

// ============================================
// Navbar
// ============================================
function initNavbar() {
  const navbar = document.querySelector('.navbar');
  if (!navbar) return;

  // Scroll effect
  window.addEventListener('scroll', function () {
    if (window.scrollY > 50) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  });

  // Active link highlighting
  const currentPath = window.location.pathname;
  const navLinks = document.querySelectorAll('.nav-link');

  navLinks.forEach(function (link) {
    const href = link.getAttribute('href');
    if (href && (currentPath === href || currentPath.startsWith(href + '/'))) {
      link.classList.add('active');
    }
  });
}

// ============================================
// Mobile Menu
// ============================================
function initMobileMenu() {
  const toggle = document.querySelector('.navbar-toggle');
  const nav = document.querySelector('.navbar-nav');

  if (!toggle || !nav) return;

  toggle.addEventListener('click', function () {
    toggle.classList.toggle('open');
    nav.classList.toggle('open');
  });

  // Close on outside click
  document.addEventListener('click', function (e) {
    if (!toggle.contains(e.target) && !nav.contains(e.target)) {
      toggle.classList.remove('open');
      nav.classList.remove('open');
    }
  });

  // Close on nav link click
  nav.querySelectorAll('.nav-link').forEach(function (link) {
    link.addEventListener('click', function () {
      toggle.classList.remove('open');
      nav.classList.remove('open');
    });
  });
}

// ============================================
// Scroll to Top Button
// ============================================
function initScrollTopButton() {
  const btn = document.querySelector('.scroll-top-btn');
  if (!btn) return;

  window.addEventListener('scroll', function () {
    if (window.scrollY > 400) {
      btn.classList.add('visible');
    } else {
      btn.classList.remove('visible');
    }
  });

  btn.addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}

// ============================================
// Scroll Animations (Intersection Observer)
// ============================================
function initAnimations() {
  const animatedElements = document.querySelectorAll('.post-card, .sidebar-widget, .download-link, .related-posts-grid .post-card');

  if (!animatedElements.length) return;

  const observer = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('fade-in-up');
          observer.unobserve(entry.target);
        }
      });
    },
    {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px',
    }
  );

  animatedElements.forEach(function (el) {
    el.style.opacity = '0';
    observer.observe(el);
  });
}

// ============================================
// Post Cards Interaction
// ============================================
function initPostCards() {
  const postCards = document.querySelectorAll('.post-card[data-url]');

  postCards.forEach(function (card) {
    card.addEventListener('click', function (e) {
      // Don't navigate if clicking a link inside the card
      if (e.target.closest('a')) return;

      const url = card.getAttribute('data-url');
      if (url) {
        window.location.href = url;
      }
    });

    // Keyboard accessibility
    card.setAttribute('tabindex', '0');
    card.setAttribute('role', 'article');

    card.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        const url = card.getAttribute('data-url');
        if (url) window.location.href = url;
      }
    });
  });
}

// ============================================
// Toast Notifications
// ============================================
const Toast = {
  container: null,

  init: function () {
    if (!this.container) {
      this.container = document.createElement('div');
      this.container.className = 'toast-container';
      document.body.appendChild(this.container);
    }
  },

  show: function (message, type, duration) {
    this.init();
    type = type || 'info';
    duration = duration || 3000;

    const icons = { success: '✅', error: '❌', info: 'ℹ️' };

    const toast = document.createElement('div');
    toast.className = 'toast ' + type;
    toast.innerHTML =
      '<span class="toast-icon">' + (icons[type] || icons.info) + '</span>' +
      '<span class="toast-message">' + message + '</span>' +
      '<span class="toast-close" role="button" aria-label="Close">✕</span>';

    this.container.appendChild(toast);

    toast.querySelector('.toast-close').addEventListener('click', function () {
      Toast.remove(toast);
    });

    setTimeout(function () {
      Toast.remove(toast);
    }, duration);
  },

  remove: function (toast) {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    setTimeout(function () {
      if (toast.parentNode) toast.parentNode.removeChild(toast);
    }, 300);
  },
};

// ============================================
// Pagination
// ============================================
function initPagination() {
  // Django handles server-side pagination
  // This handles smooth page transitions
  const pageLinks = document.querySelectorAll('.page-btn:not(.disabled):not(.active)');

  pageLinks.forEach(function (link) {
    link.addEventListener('click', function (e) {
      // Add loading state
      const postsGrid = document.querySelector('.posts-grid');
      if (postsGrid) {
        postsGrid.style.opacity = '0.5';
        postsGrid.style.transition = 'opacity 0.3s ease';
      }
    });
  });
}

// ============================================
// Image Lazy Loading Fallback
// ============================================
function initLazyImages() {
  const images = document.querySelectorAll('img[data-src]');

  if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          const img = entry.target;
          img.src = img.getAttribute('data-src');
          img.removeAttribute('data-src');
          imageObserver.unobserve(img);
        }
      });
    });

    images.forEach(function (img) {
      imageObserver.observe(img);
    });
  } else {
    // Fallback for older browsers
    images.forEach(function (img) {
      img.src = img.getAttribute('data-src');
    });
  }
}

// ============================================
// Copy to Clipboard
// ============================================
function copyToClipboard(text) {
  if (navigator.clipboard && window.isSecureContext) {
    navigator.clipboard.writeText(text).then(function () {
      Toast.show('Copied to clipboard!', 'success', 2000);
    });
  } else {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);
    Toast.show('Copied to clipboard!', 'success', 2000);
  }
}

// ============================================
// Search Filter (Client-side for sidebar)
// ============================================
function initSearch() {
  const searchInput = document.querySelector('#sidebar-search');
  if (!searchInput) return;

  searchInput.addEventListener('input', function () {
    const query = this.value.toLowerCase().trim();
    const items = document.querySelectorAll('.recent-post-item');

    items.forEach(function (item) {
      const title = item.querySelector('.recent-post-title');
      if (title) {
        const text = title.textContent.toLowerCase();
        item.style.display = text.includes(query) ? '' : 'none';
      }
    });
  });
}

// ============================================
// Initialize all on load
// ============================================
window.addEventListener('load', function () {
  initPagination();
  initLazyImages();
  initSearch();
});

// ============================================
// Expose utilities globally
// ============================================
window.KurotsukiSubs = {
  Toast: Toast,
  copyToClipboard: copyToClipboard,
};
