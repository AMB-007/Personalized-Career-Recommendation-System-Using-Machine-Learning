/**
 * CareerAI — Shared Application Utilities
 * Handles: Theme, Auth, Navbar rendering, API helpers
 */

const API_BASE = 'http://127.0.0.1:5000';

/* ── THEME ──────────────────────────────────────────────────── */
const ThemeManager = {
  get() { return localStorage.getItem('theme') || 'dark'; },
  set(theme) {
    localStorage.setItem('theme', theme);
    document.documentElement.setAttribute('data-theme', theme);
    document.getElementById('theme-icon') && (document.getElementById('theme-icon').textContent = theme === 'dark' ? '☀️' : '🌙');
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
    const headers = { 'Content-Type': 'application/json' };
    if (auth) headers['Authorization'] = `Bearer ${Auth.getToken()}`;
    const res = await fetch(`${API_BASE}${path}`, { headers });
    return res.json();
  },
  async post(path, body, auth = false) {
    const headers = { 'Content-Type': 'application/json' };
    if (auth) headers['Authorization'] = `Bearer ${Auth.getToken()}`;
    const res = await fetch(`${API_BASE}${path}`, {
      method: 'POST',
      headers,
      body: JSON.stringify(body)
    });
    return res.json();
  },
  async put(path, body, auth = false) {
    const headers = { 'Content-Type': 'application/json' };
    if (auth) headers['Authorization'] = `Bearer ${Auth.getToken()}`;
    const res = await fetch(`${API_BASE}${path}`, {
      method: 'PUT',
      headers,
      body: JSON.stringify(body)
    });
    return res.json();
  },
  async del(path, auth = false) {
    const headers = { 'Content-Type': 'application/json' };
    if (auth) headers['Authorization'] = `Bearer ${Auth.getToken()}`;
    const res = await fetch(`${API_BASE}${path}`, { method: 'DELETE', headers });
    return res.json();
  }
};

/* ── NAVBAR ──────────────────────────────────────────────────── */
function renderNavbar(activePage = '') {
  const user = Auth.getUser();
  const isAdmin = Auth.isAdmin();
  const theme = ThemeManager.get();

  const navLinks = isAdmin ? `
    <a href="/admin.html" class="${activePage === 'admin' ? 'active' : ''}">👑 Admin Center</a>
    <a href="/index.html" class="${activePage === 'home' ? 'active' : ''}">🌐 Home</a>
  ` : (user ? `
    <a href="/index.html" class="${activePage === 'home' ? 'active' : ''}">Home</a>
    <a href="/dashboard.html" class="${activePage === 'dashboard' ? 'active' : ''}">Dashboard</a>
    <a href="/assessment.html" class="${activePage === 'assessment' ? 'active' : ''}">Take Assessment</a>
    <a href="/history.html" class="${activePage === 'history' ? 'active' : ''}">History</a>
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
        <div class="nav-right-mobile flex items-center gap-1">
          <button class="theme-btn" id="theme-btn" title="Toggle theme">
            <span id="theme-icon">${theme === 'dark' ? '☀️' : '🌙'}</span>
          </button>
          ${userSection}
        </div>
      </div>

      <div class="nav-right">
        <button class="theme-btn" id="theme-btn-desktop" title="Toggle theme">
          <span id="theme-icon-desktop">${theme === 'dark' ? '☀️' : '🌙'}</span>
        </button>
        ${userSection.replace(/id="notif-wrap"/,'id="notif-wrap-d"').replace(/id="notif-btn"/,'id="notif-btn-d"').replace(/id="notif-dropdown"/,'id="notif-dropdown-d"').replace(/id="user-wrap"/,'id="user-wrap-d"').replace(/id="user-avatar-btn"/,'id="user-avatar-btn-d"').replace(/id="user-dropdown"/,'id="user-dropdown-d"').replace(/id="logout-btn"/,'id="logout-btn-d"')}
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

  // Theme toggles
  ['theme-btn','theme-btn-desktop'].forEach(id => {
    document.getElementById(id)?.addEventListener('click', () => {
      ThemeManager.toggle();
      ['theme-icon','theme-icon-desktop'].forEach(ico => {
        const el = document.getElementById(ico);
        if (el) el.textContent = ThemeManager.get() === 'dark' ? '☀️' : '🌙';
      });
    });
  });

  // Notification dropdowns
  ['notif-btn','notif-btn-d'].forEach(id => {
    document.getElementById(id)?.addEventListener('click', (e) => {
      e.stopPropagation();
      const ddId = id.endsWith('-d') ? 'notif-dropdown-d' : 'notif-dropdown';
      const dd = document.getElementById(ddId);
      if (dd) dd.classList.toggle('hidden');
      // Close user menu
      ['user-dropdown','user-dropdown-d'].forEach(u => document.getElementById(u)?.classList.add('hidden'));
    });
  });

  // User menu dropdowns
  ['user-avatar-btn','user-avatar-btn-d'].forEach(id => {
    document.getElementById(id)?.addEventListener('click', (e) => {
      e.stopPropagation();
      const ddId = id.endsWith('-d') ? 'user-dropdown-d' : 'user-dropdown';
      const dd = document.getElementById(ddId);
      if (dd) dd.classList.toggle('hidden');
      ['notif-dropdown','notif-dropdown-d'].forEach(n => document.getElementById(n)?.classList.add('hidden'));
    });
  });

  // Logout
  ['logout-btn','logout-btn-d'].forEach(id => {
    document.getElementById(id)?.addEventListener('click', (e) => {
      e.preventDefault();
      Auth.logout();
    });
  });

  // Close dropdowns on outside click
  document.addEventListener('click', () => {
    ['notif-dropdown','notif-dropdown-d','user-dropdown','user-dropdown-d'].forEach(id => {
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
});
