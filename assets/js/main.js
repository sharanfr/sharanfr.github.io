/* =============================================
   THEME SYSTEM
   ============================================= */
const DARK_THEMES = ['void', 'signal'];
const LIGHT_THEMES = ['paper', 'ink'];

let lastDark = localStorage.getItem('lastDark') || 'void';
let lastLight = localStorage.getItem('lastLight') || 'ink';

function applyTheme(name) {
  document.documentElement.setAttribute('data-theme', name);
  localStorage.setItem('theme', name);

  if (DARK_THEMES.includes(name)) {
    lastDark = name;
    localStorage.setItem('lastDark', name);
  } else {
    lastLight = name;
    localStorage.setItem('lastLight', name);
  }

  // Update toggle icon
  const toggle = document.getElementById('theme-toggle');
  const isDark = DARK_THEMES.includes(name);
  toggle.innerHTML = isDark
    ? '<i class="bi bi-moon-stars-fill"></i>'
    : '<i class="bi bi-sun-fill"></i>';

  // Update active dot
  document.querySelectorAll('.scheme-dot').forEach(dot => {
    dot.classList.toggle('active', dot.dataset.theme === name);
  });
}

// Init from localStorage or default
const saved = localStorage.getItem('theme') || 'ink';
applyTheme(saved);

// Palette dot clicks
document.querySelectorAll('.scheme-dot').forEach(dot => {
  dot.addEventListener('click', () => applyTheme(dot.dataset.theme));
});

// Dark / Light toggle
document.getElementById('theme-toggle').addEventListener('click', () => {
  const current = document.documentElement.getAttribute('data-theme');
  const isDark = DARK_THEMES.includes(current);
  applyTheme(isDark ? lastLight : lastDark);
});

/* =============================================
   SCROLL FADE-IN
   ============================================= */
const fadeObserver = new IntersectionObserver(
  entries => entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); }),
  { threshold: 0.08, rootMargin: '0px 0px -40px 0px' }
);

document.querySelectorAll('section, .project-item, .edu-item, .contact-item, .skill-group')
  .forEach(el => { el.classList.add('fade-in'); fadeObserver.observe(el); });

/* =============================================
   ACTIVE NAV HIGHLIGHT ON SCROLL
   ============================================= */
const navLinks = document.querySelectorAll('.nav-links a');

const sectionObserver = new IntersectionObserver(
  entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        const id = e.target.getAttribute('id');
        navLinks.forEach(link => {
          link.style.color = link.getAttribute('href') === `#${id}`
            ? 'var(--heading)' : '';
        });
      }
    });
  },
  { threshold: 0.35 }
);

document.querySelectorAll('section[id]').forEach(s => sectionObserver.observe(s));

/* =============================================
   SCROLL PROGRESS BAR
   ============================================= */
const progressBar = document.getElementById('scroll-progress');
const backToTop   = document.getElementById('back-to-top');

window.addEventListener('scroll', () => {
  const scrolled = window.scrollY;
  const max = document.documentElement.scrollHeight - window.innerHeight;
  const ratio = scrolled / max;

  // progress bar
  progressBar.style.width = `${ratio * 100}%`;

  // back to top — show after 40% scrolled
  backToTop.classList.toggle('visible', ratio > 0.4);
}, { passive: true });

backToTop.addEventListener('click', () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
});

/* =============================================
   LIVE IST CLOCK
   ============================================= */
function updateClock() {
  const clock = document.getElementById('nav-clock');
  if (!clock) return;
  const now = new Date();
  const ist = new Date(now.toLocaleString('en-US', { timeZone: 'Asia/Kolkata' }));
  const h = String(ist.getHours()).padStart(2, '0');
  const m = String(ist.getMinutes()).padStart(2, '0');
  const s = String(ist.getSeconds()).padStart(2, '0');
  clock.textContent = `${h}:${m}:${s} IST`;
}
updateClock();
setInterval(updateClock, 1000);

/* =============================================
   KEYBOARD SHORTCUT — T to toggle theme
   ============================================= */
document.addEventListener('keydown', (e) => {
  if (e.key === 't' || e.key === 'T') {
    // ignore if user is typing in an input
    if (['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) return;
    document.getElementById('theme-toggle').click();
  }
});

/* =============================================
   EMAIL COPY TO CLIPBOARD
   ============================================= */
function copyEmail(btn) {
  const email = btn.dataset.email;
  const label = btn.querySelector('.social-label');
  navigator.clipboard.writeText(email).then(() => {
    const original = label.textContent;
    label.textContent = 'copied!';
    btn.style.borderColor = 'var(--heading)';
    btn.style.color = 'var(--heading)';
    setTimeout(() => {
      label.textContent = original;
      btn.style.borderColor = '';
      btn.style.color = '';
    }, 1800);
  });
}

/* =============================================
   DISCORD COPY TO CLIPBOARD
   ============================================= */
function copyDiscord(btn) {
  const username = btn.dataset.discord;
  const label = btn.querySelector('.social-label');
  navigator.clipboard.writeText(username).then(() => {
    const original = label.textContent;
    label.textContent = 'copied!';
    btn.style.borderColor = 'var(--heading)';
    btn.style.color = 'var(--heading)';
    setTimeout(() => {
      label.textContent = original;
      btn.style.borderColor = '';
      btn.style.color = '';
    }, 1800);
  });
}

/* =============================================
   TYPEWRITER — hero quote, runs once on load
   ============================================= */
(function typewriterQuote() {
  const el = document.querySelector('.hero-quote');
  if (!el) return;

  // respect reduce-motion — skip animation
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const fullText = el.textContent.trim();
  el.textContent = '';

  let i = 0;
  setTimeout(() => {
    const timer = setInterval(() => {
      i++;
      el.textContent = fullText.slice(0, i) + (i < fullText.length ? '|' : '');
      if (i >= fullText.length) clearInterval(timer);
    }, 32); // 32ms per char ≈ fast but readable
  }, 500); // 500ms initial delay — let page settle first
})();

/* =============================================
   CURSOR DOT — follows mouse, grows on hover
   ============================================= */
(function initCursorDot() {
  if (!window.matchMedia('(hover: hover) and (pointer: fine)').matches) return;

  const dot = document.getElementById('cursor-dot');
  if (!dot) return;

  document.addEventListener('mousemove', e => {
    dot.style.left = e.clientX + 'px';
    dot.style.top  = e.clientY + 'px';
    dot.classList.add('visible');
  }, { passive: true });

  document.addEventListener('mouseleave', () => dot.classList.remove('visible'));
  document.addEventListener('mouseenter', () => dot.classList.add('visible'));

  const sel = 'a, button, .scheme-dot, .social-item, .project-link, .interest-item, label';
  document.querySelectorAll(sel).forEach(el => {
    el.addEventListener('mouseenter', () => dot.classList.add('hovering'));
    el.addEventListener('mouseleave', () => dot.classList.remove('hovering'));
  });
})();

/* =============================================
   CERT LIGHTBOX
   ============================================= */
function openCert(url, certTitle) {
  const modal = document.getElementById('cert-modal');
  const frame = document.getElementById('cert-modal-frame');
  const title = document.getElementById('cert-modal-title');
  // use passed title, or derive from filename as fallback
  title.textContent = certTitle || url.split('/').pop().replace(/\.pdf$/i, '').replace(/-/g, ' ');
  frame.src = url;
  modal.classList.add('active');
  document.body.style.overflow = 'hidden';
}

function closeCert() {
  const modal = document.getElementById('cert-modal');
  const frame = document.getElementById('cert-modal-frame');
  modal.classList.remove('active');
  document.body.style.overflow = '';
  setTimeout(() => { frame.src = ''; }, 300);
}

document.getElementById('cert-modal-close')
  .addEventListener('click', closeCert);
document.getElementById('cert-modal-backdrop')
  .addEventListener('click', closeCert);
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') closeCert();
});
