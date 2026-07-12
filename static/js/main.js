/* ===================================================
   FashionAI — Main JavaScript
   Features: dark mode, nav scroll, hamburger,
   image upload preview, favorites AJAX, search
   =================================================== */

document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initNavbar();
  initSearch();
  initUpload();
  initFavorites();
  initAnimations();
  initScrollReveal();
  initCounters();
  autoHideToasts();
});

/* -------- Dark Mode -------- */
function initTheme() {
  const toggle = document.getElementById('themeToggle');
  const html = document.documentElement;
  const saved = localStorage.getItem('theme') || 'light';
  html.setAttribute('data-theme', saved);

  toggle?.addEventListener('click', () => {
    const current = html.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
    toggle.style.transform = 'rotate(360deg)';
    setTimeout(() => { toggle.style.transform = ''; }, 400);
  });
}

/* -------- Navbar -------- */
function initNavbar() {
  const navbar = document.getElementById('navbar');
  const hamburger = document.getElementById('hamburger');
  const navLinks = document.getElementById('navLinks');

  // Scroll shadow
  window.addEventListener('scroll', () => {
    navbar?.classList.toggle('scrolled', window.scrollY > 20);
  });

  // Hamburger toggle
  hamburger?.addEventListener('click', () => {
    hamburger.classList.toggle('open');
    navLinks?.classList.toggle('open');
  });

  // Close on backdrop click
  document.addEventListener('click', (e) => {
    if (!navbar?.contains(e.target)) {
      hamburger?.classList.remove('open');
      navLinks?.classList.remove('open');
    }
  });
}

/* -------- Global Search -------- */
function initSearch() {
  const searchToggle = document.getElementById('searchToggle');
  const navSearch = document.getElementById('navSearch');
  const searchInput = document.getElementById('globalSearch');
  const searchResults = document.getElementById('searchResults');

  searchToggle?.addEventListener('click', () => {
    navSearch?.classList.toggle('open');
    if (navSearch?.classList.contains('open')) {
      searchInput?.focus();
    } else {
      searchResults?.classList.remove('show');
    }
  });

  let debounceTimer;
  searchInput?.addEventListener('input', () => {
    clearTimeout(debounceTimer);
    const q = searchInput.value.trim();
    if (q.length < 2) {
      searchResults?.classList.remove('show');
      return;
    }
    debounceTimer = setTimeout(() => fetchSearch(q), 300);
  });

  document.addEventListener('click', (e) => {
    if (!navSearch?.contains(e.target)) {
      searchResults?.classList.remove('show');
      navSearch?.classList.remove('open');
    }
  });
}

async function fetchSearch(query) {
  const searchResults = document.getElementById('searchResults');
  try {
    const res = await fetch(`/api/search/?q=${encodeURIComponent(query)}`);
    const data = await res.json();
    renderSearchResults(data.results || []);
  } catch (e) {
    console.error('Search error', e);
  }
}

function renderSearchResults(results) {
  const container = document.getElementById('searchResults');
  if (!container) return;
  if (results.length === 0) {
    container.innerHTML = '<div class="search-result-item"><span style="color:var(--text-muted)">No outfits found</span></div>';
  } else {
    container.innerHTML = results.map(o => `
      <div class="search-result-item" onclick="window.location='/recommend/'">
        <div class="search-result-img" style="background:var(--bg-tertiary);display:flex;align-items:center;justify-content:center;font-size:20px;">👗</div>
        <div class="search-result-info">
          <div class="search-result-name">${escHtml(o.name)}</div>
          <div class="search-result-meta">${escHtml(o.occasion)} · ${o.match_percentage}% match</div>
        </div>
      </div>
    `).join('');
  }
  container.classList.add('show');
}

/* -------- Image Upload Preview -------- */
function initUpload() {
  const zone = document.getElementById('uploadZone');
  const input = document.getElementById('outfitImageInput');
  const preview = document.getElementById('uploadPreview');

  if (!zone || !input) return;

  zone.addEventListener('click', () => input.click());

  input.addEventListener('change', () => {
    const file = input.files[0];
    if (file) showPreview(file, preview, zone);
  });

  zone.addEventListener('dragover', (e) => {
    e.preventDefault();
    zone.classList.add('drag-over');
  });
  zone.addEventListener('dragleave', () => zone.classList.remove('drag-over'));
  zone.addEventListener('drop', (e) => {
    e.preventDefault();
    zone.classList.remove('drag-over');
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
      const dt = new DataTransfer();
      dt.items.add(file);
      input.files = dt.files;
      showPreview(file, preview, zone);
    }
  });
}

function showPreview(file, preview, zone) {
  const reader = new FileReader();
  reader.onload = (e) => {
    if (preview) {
      preview.src = e.target.result;
      preview.classList.add('show');
    }
    const title = zone?.querySelector('.upload-title');
    if (title) title.textContent = file.name;
  };
  reader.readAsDataURL(file);
}

/* -------- Favorites AJAX -------- */
function initFavorites() {
  document.querySelectorAll('.fav-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      const outfitId = btn.dataset.outfitId;
      if (!outfitId) return;
      toggleFavorite(btn, outfitId);
    });
  });
}

async function toggleFavorite(btn, outfitId) {
  const csrf = getCsrf();
  if (!csrf) {
    window.location.href = '/accounts/login/?next=' + encodeURIComponent(window.location.pathname);
    return;
  }
  btn.disabled = true;
  try {
    const res = await fetch('/api/toggle-favorite/', {
      method: 'POST',
      headers: { 'X-CSRFToken': csrf, 'Content-Type': 'application/x-www-form-urlencoded' },
      body: `outfit_id=${outfitId}`,
    });
    const data = await res.json();
    if (data.status === 'added') {
      btn.textContent = '❤️';
      btn.classList.add('active');
      showToast('Added to favorites!', 'success');
    } else {
      btn.textContent = '🤍';
      btn.classList.remove('active');
      showToast('Removed from favorites', '');
    }
  } catch (err) {
    console.error(err);
  } finally {
    btn.disabled = false;
  }
}

/* -------- Scroll Animations -------- */
function initAnimations() {
  // Only animate elements that do NOT already have fade-in (i.e., static elements like step-card, tech-card etc.)
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('anim-visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  // Only target elements that don't already have fade-in applied at template level
  document.querySelectorAll('.step-card, .tech-card, .objective-item, .feature-card').forEach(el => {
    el.classList.add('anim-hidden');
    observer.observe(el);
  });
}

/* -------- Scroll Reveal (data-aos) -------- */
function initScrollReveal() {
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('aos-animate');
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0 });

  document.querySelectorAll('[data-aos]').forEach(el => {
    revealObserver.observe(el);
  });
}

/* -------- Animated Counters -------- */
function animateCounter(el, target, suffix = '', duration = 1800) {
  let start = 0;
  const step = (timestamp) => {
    if (!start) start = timestamp;
    const progress = Math.min((timestamp - start) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    const current = Math.floor(eased * target);
    el.textContent = current.toLocaleString();
    if (progress < 1) requestAnimationFrame(step);
    else el.textContent = target.toLocaleString();
  };
  requestAnimationFrame(step);
}

function initCounters() {
  // Hero trust row counters
  const trustObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        const target = parseInt(el.getAttribute('data-count'), 10);
        animateCounter(el, target);
        trustObserver.unobserve(el);
      }
    });
  }, { threshold: 0.5 });
  document.querySelectorAll('[data-count]').forEach(el => trustObserver.observe(el));

  // Stats section counters
  const statObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        const target = parseInt(el.getAttribute('data-target'), 10);
        const suffix = el.getAttribute('data-suffix') || '';
        const duration = target > 1000 ? 2200 : 1200;
        let start = 0;
        const step = (ts) => {
          if (!start) start = ts;
          const progress = Math.min((ts - start) / duration, 1);
          const eased = 1 - Math.pow(1 - progress, 3);
          const cur = Math.floor(eased * target);
          el.textContent = cur.toLocaleString() + (progress >= 1 ? suffix : '');
          if (progress < 1) requestAnimationFrame(step);
          else el.textContent = target.toLocaleString() + suffix;
        };
        requestAnimationFrame(step);
        statObserver.unobserve(el);
      }
    });
  }, { threshold: 0.4 });
  document.querySelectorAll('[data-target]').forEach(el => statObserver.observe(el));
}

/* -------- Toasts -------- */
function showToast(message, type = '') {
  const container = document.getElementById('toastContainer') || createToastContainer();
  const toast = document.createElement('div');
  toast.className = `toast${type ? ' toast-' + type : ''}`;
  toast.innerHTML = `<span>${escHtml(message)}</span><button onclick="this.parentElement.remove()">✕</button>`;
  container.appendChild(toast);
  setTimeout(() => toast.remove(), 4000);
}

function createToastContainer() {
  const div = document.createElement('div');
  div.id = 'toastContainer';
  div.className = 'toast-container';
  document.body.appendChild(div);
  return div;
}

function autoHideToasts() {
  document.querySelectorAll('.toast').forEach(t => {
    setTimeout(() => t.remove(), 4000);
  });
}

/* -------- Utilities -------- */
function getCsrf() {
  const cookie = document.cookie.split(';').find(c => c.trim().startsWith('csrftoken='));
  return cookie ? cookie.split('=')[1] : null;
}

function escHtml(str) {
  const div = document.createElement('div');
  div.appendChild(document.createTextNode(str || ''));
  return div.innerHTML;
}
