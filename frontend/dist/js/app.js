/**
 * CareerAI — Shared Application Utilities
 * Handles: Theme, Auth, Navbar rendering, API helpers
 */

const API_BASE = window.location.hostname === '127.0.0.1' || window.location.hostname === 'localhost' 
  ? 'http://127.0.0.1:5000' 
  : ''; // Use relative paths or replace with production URL

/* ── TOAST NOTIFICATIONS ─────────────────────────────────────── */
const Toast = {
  container: null,
  init() {
    if (!document.querySelector('.toast-container')) {
      this.container = document.createElement('div');
      this.container.className = 'toast-container';
      document.body.appendChild(this.container);
    } else {
      this.container = document.querySelector('.toast-container');
    }
  },
  show(message, type = 'info') {
    if (!this.container) this.init();
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    // Add icon based on type
    let icon = 'ℹ️';
    if (type === 'success') icon = '✅';
    if (type === 'error') icon = '⚠️';
    
    toast.innerHTML = `<span>${icon}</span> <span>${message}</span>`;
    this.container.appendChild(toast);
    
    setTimeout(() => {
      toast.classList.add('hiding');
      setTimeout(() => { if (toast.parentNode) toast.remove(); }, 300);
    }, 3500);
  }
};

/* ── THEME ──────────────────────────────────────────────────── */
const ThemeManager = {
  get() { return localStorage.getItem('theme') || 'light'; },
  set(theme) {
    localStorage.setItem('theme', theme);
    document.documentElement.setAttribute('data-theme', theme);
    const icon = document.getElementById('theme-icon-desktop');
    if (icon) icon.textContent = theme === 'dark' ? '☀️' : '🌙';
  },
  toggle() { this.set(this.get() === 'dark' ? 'light' : 'dark'); },
  init() { this.set(this.get()); }
};


/* ── AUTH ────────────────────────────────────────────────────── */
const Auth = {
  getToken() { return localStorage.getItem('authToken') || localStorage.getItem('token'); },
  getUser() {
    const s = localStorage.getItem('userInfo') || localStorage.getItem('user');
    return s ? JSON.parse(s) : null;
  },
  isLoggedIn() { return !!this.getToken() && !!this.getUser(); },
  isAdmin() {
    const u = this.getUser();
    return u && (u.role === 'admin' || (u.email && u.email.includes('admin')));
  },
  logout() {
    ['user','userInfo','authToken','token','top5Careers','finalRecommendedCareer','readinessScore','xaiAttributions'].forEach(k => localStorage.removeItem(k));
    window.location.href = '/login.html';
  },
  requireAuth() {
    if (!this.isLoggedIn()) { window.location.href = '/login.html'; return false; }
    return true;
  },
  requireAdmin() {
    if (!this.isLoggedIn() || !this.isAdmin()) { window.location.href = '/admin-login.html'; return false; }
    return true;
  }
};

/* ── API HELPERS ─────────────────────────────────────────────── */
const API = {
  async get(path, auth = false) {
    try {
      const headers = { 'Content-Type': 'application/json' };
      if (auth) headers['Authorization'] = `Bearer ${Auth.getToken()}`;
      const res = await fetch(`${API_BASE}${path}`, { headers });
      if (res.status === 401) { Auth.logout(); throw new Error("Session expired. Please log in again."); }
      if (!res.ok) throw new Error(`HTTP Error ${res.status}`);
      return await res.json();
    } catch (err) {
      Toast.show(err.message || 'Failed to fetch data.', 'error');
      throw err;
    }
  },
  async post(path, body, auth = false) {
    try {
      const headers = { 'Content-Type': 'application/json' };
      if (auth) headers['Authorization'] = `Bearer ${Auth.getToken()}`;
      const res = await fetch(`${API_BASE}${path}`, {
        method: 'POST',
        headers,
        body: JSON.stringify(body)
      });
      if (res.status === 401) { Auth.logout(); throw new Error("Session expired. Please log in again."); }
      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.error || errorData.message || `HTTP Error ${res.status}`);
      }
      return await res.json();
    } catch (err) {
      Toast.show(err.message || 'Failed to submit data.', 'error');
      throw err;
    }
  },
  async put(path, body, auth = false) {
    try {
      const headers = { 'Content-Type': 'application/json' };
      if (auth) headers['Authorization'] = `Bearer ${Auth.getToken()}`;
      const res = await fetch(`${API_BASE}${path}`, {
        method: 'PUT',
        headers,
        body: JSON.stringify(body)
      });
      if (res.status === 401) { Auth.logout(); throw new Error("Session expired. Please log in again."); }
      if (!res.ok) throw new Error(`HTTP Error ${res.status}`);
      return await res.json();
    } catch (err) {
      Toast.show(err.message || 'Failed to update data.', 'error');
      throw err;
    }
  },
  async del(path, auth = false) {
    try {
      const headers = { 'Content-Type': 'application/json' };
      if (auth) headers['Authorization'] = `Bearer ${Auth.getToken()}`;
      const res = await fetch(`${API_BASE}${path}`, { method: 'DELETE', headers });
      if (res.status === 401) { Auth.logout(); throw new Error("Session expired. Please log in again."); }
      if (!res.ok) throw new Error(`HTTP Error ${res.status}`);
      return await res.json();
    } catch (err) {
      Toast.show(err.message || 'Failed to delete data.', 'error');
      throw err;
    }
  }
};

/* ── NAVBAR ──────────────────────────────────────────────────── */
function renderNavbar(activePage = '') {
  const user = Auth.getUser();
  const isAdmin = Auth.isAdmin();
  const theme = ThemeManager.get();

  const isHome = activePage === 'home';
  const navLinks = isAdmin ? `
    <a href="/admin.html" class="${activePage === 'admin' ? 'active' : ''}">👑 Admin Center</a>
    <a href="/index.html" class="${activePage === 'home' ? 'active' : ''}">🌐 Home</a>
  ` : (user ? `
    <a href="/index.html"    class="${activePage === 'home'       ? 'active' : ''}">Home</a>
    <a href="/dashboard.html" class="${activePage === 'dashboard'  ? 'active' : ''}">Dashboard</a>
    <a href="/assessment.html" class="${activePage === 'assessment' ? 'active' : ''}">Take Assessment</a>
    <a href="/history.html"   class="${activePage === 'history'    ? 'active' : ''}">History</a>
  ` : isHome ? `
    <a href="/index.html"    class="active">Home</a>
    <a href="#how-it-works">How It Works</a>
    <a href="#domains">Careers</a>
    <a href="#faq">FAQ</a>
  ` : `
    <a href="/index.html" class="${activePage === 'home' ? 'active' : ''}">Home</a>
  `);

  const userSection = user ? `
    <div class="relative" id="notif-wrap">
      <button class="notif-btn" id="notif-btn" title="Notifications">
        🔔<span class="notif-badge">3</span>
      </button>
      <div class="dropdown dropdown-notif hidden" id="notif-dropdown">
        <div class="dropdown-header"><strong style="color:var(--text-h)">Notifications</strong></div>
        <div class="notif-item"><span class="notif-item-icon">🎯</span><div><p>Your assessment results are ready</p><span>2h ago</span></div></div>
        <div class="notif-item"><span class="notif-item-icon">📚</span><div><p>New certification path recommended</p><span>5h ago</span></div></div>
        <div class="notif-item"><span class="notif-item-icon">📈</span><div><p>Career market trend update available</p><span>1d ago</span></div></div>
      </div>
    </div>
    <div class="relative" id="user-wrap">
      <button class="user-avatar-btn" id="user-avatar-btn" title="${user.full_name || 'User'}">
        ${(user.full_name || user.name || 'U')[0].toUpperCase()}
      </button>
      <div class="dropdown dropdown-user hidden" id="user-dropdown">
        <div class="dropdown-header">
          <p>${user.full_name || user.name || 'User'}</p>
          <span>${user.email || ''}</span>
        </div>
        <a href="/settings.html" class="dropdown-link">⚙️ Profile Settings</a>
        <a href="/history.html" class="dropdown-link">📋 Assessment History</a>
        <a href="#" class="dropdown-link danger" id="logout-btn">🚪 Logout</a>
      </div>
    </div>
  ` : `
    <a href="/login.html" class="btn btn-secondary btn-sm">Login</a>
    <a href="/register.html" class="btn btn-primary btn-sm">Get Started</a>
  `;

  const navHTML = `
    <nav class="navbar" id="main-navbar">
      <a href="/index.html" class="nav-brand">
        <span class="nav-logo">✨ Career<span class="logo-ai">AI</span></span>
        <span class="brand-tag">ML-Powered</span>
      </a>

      <button class="hamburger" id="hamburger" aria-label="Menu" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>

      <div class="nav-links" id="nav-links">
        ${navLinks}
      </div>

      <div class="nav-right">
        <button class="theme-btn" id="theme-btn-desktop" title="Toggle theme">
          <span id="theme-icon-desktop">${theme === 'dark' ? '☀️' : '🌙'}</span>
        </button>
        ${userSection}
      </div>
    </nav>
  `;

  const target = document.getElementById('navbar-container');
  if (target) target.innerHTML = navHTML;
  else document.body.insertAdjacentHTML('afterbegin', navHTML);

  // Wire up events
  document.getElementById('hamburger')?.addEventListener('click', () => {
    const links = document.getElementById('nav-links');
    const expanded = links.classList.toggle('open');
    document.getElementById('hamburger').setAttribute('aria-expanded', expanded);
  });

  // Theme toggle
  document.getElementById('theme-btn-desktop')?.addEventListener('click', () => {
    ThemeManager.toggle();
    const ico = document.getElementById('theme-icon-desktop');
    if (ico) ico.textContent = ThemeManager.get() === 'dark' ? '☀️' : '🌙';
  });

  // Notification dropdown
  document.getElementById('notif-btn')?.addEventListener('click', (e) => {
    e.stopPropagation();
    const dd = document.getElementById('notif-dropdown');
    if (dd) dd.classList.toggle('hidden');
    document.getElementById('user-dropdown')?.classList.add('hidden');
  });

  // User menu dropdown
  document.getElementById('user-avatar-btn')?.addEventListener('click', (e) => {
    e.stopPropagation();
    const dd = document.getElementById('user-dropdown');
    if (dd) dd.classList.toggle('hidden');
    document.getElementById('notif-dropdown')?.classList.add('hidden');
  });

  // Logout
  document.getElementById('logout-btn')?.addEventListener('click', (e) => {
    e.preventDefault();
    Auth.logout();
  });

  // Close dropdowns on outside click
  document.addEventListener('click', () => {
    ['notif-dropdown','user-dropdown'].forEach(id => {
      document.getElementById(id)?.classList.add('hidden');
    });
  });
}

/* ── UI HELPERS ──────────────────────────────────────────────── */
const UI = {
  showAlert(containerId, type, message) {
    const el = document.getElementById(containerId);
    if (!el) return;
    el.innerHTML = `<div class="alert alert-${type}">${message}</div>`;
    el.classList.remove('hidden');
  },
  hideAlert(containerId) {
    const el = document.getElementById(containerId);
    if (el) { el.innerHTML = ''; el.classList.add('hidden'); }
  },
  setLoading(btnId, loading, loadingText = 'Loading...', originalText = '') {
    const btn = document.getElementById(btnId);
    if (!btn) return;
    btn.disabled = loading;
    btn.textContent = loading ? loadingText : (originalText || btn.dataset.originalText || 'Submit');
    if (!loading && originalText) btn.dataset.originalText = originalText;
  },
  spinner() {
    return `<div class="loading-state"><div class="spinner"></div><p>Loading...</p></div>`;
  }
};

/* ── INIT ON EVERY PAGE ──────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  ThemeManager.init();

  // Scroll-reveal animation for .reveal elements
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('revealed');
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

  document.querySelectorAll('.reveal').forEach((el, i) => {
    el.style.transitionDelay = `${i * 0.06}s`;
    revealObserver.observe(el);
  });
});
