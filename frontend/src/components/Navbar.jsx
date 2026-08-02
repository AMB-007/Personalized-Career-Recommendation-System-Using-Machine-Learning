import { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useTheme } from '../context/ThemeContext';

const Navbar = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { theme, toggleTheme } = useTheme();
  const [menuOpen, setMenuOpen] = useState(false);
  const [showNotifications, setShowNotifications] = useState(false);
  const [showUserMenu, setShowUserMenu] = useState(false);

  // Support both 'userInfo' (new) and 'user' (legacy) keys
  const userStr = localStorage.getItem('userInfo') || localStorage.getItem('user');
  const user = userStr ? JSON.parse(userStr) : null;

  const handleLogout = () => {
    localStorage.removeItem('user');
    localStorage.removeItem('userInfo');
    localStorage.removeItem('authToken');
    localStorage.removeItem('token');
    localStorage.removeItem('top5Careers');
    localStorage.removeItem('finalRecommendedCareer');
    navigate('/login');
  };

  const closeMenu = () => {
    setMenuOpen(false);
    setShowNotifications(false);
    setShowUserMenu(false);
  };

  const isActive = (path) => location.pathname === path ? 'active-link' : '';
  const isAdmin  = user && (user.role === 'admin' || user.email?.includes('admin'));

  const notifications = [
    { icon: '🎯', text: 'Your assessment results are ready', time: '2h ago' },
    { icon: '📚', text: 'New certification path recommended', time: '5h ago' },
    { icon: '📈', text: 'Career market trend update available', time: '1d ago' },
  ];

  return (
    <nav className="nav-header" aria-label="Main navigation" style={{ position: 'sticky', top: 0, zIndex: 100 }}>
      {/* BRAND */}
      <div className="nav-brand">
        <Link to="/" onClick={closeMenu} className="nav-logo">
          <span className="logo-spark">✨</span> Career<span className="logo-ai">AI</span>
        </Link>
        <span className="brand-tag">ML-Powered Guidance</span>
      </div>

      {/* MOBILE HAMBURGER */}
      <button
        type="button"
        className="menu-toggle"
        aria-label="Toggle navigation"
        aria-expanded={menuOpen}
        onClick={() => setMenuOpen(o => !o)}
      >
        <span></span><span></span><span></span>
      </button>

      {/* NAV LINKS */}
      <div className={`nav-links ${menuOpen ? 'open' : ''}`}>
        {isAdmin ? (
          <>
            <Link to="/admin"      onClick={closeMenu} className={`admin-nav-link ${isActive('/admin')}`}>👑 Admin Center</Link>
            <Link to="/"           onClick={closeMenu} className={isActive('/')}>🌐 Home</Link>
          </>
        ) : (
          <>
            <Link to="/"           onClick={closeMenu} className={isActive('/')}>Home</Link>
            <Link to="/dashboard"  onClick={closeMenu} className={isActive('/dashboard')}>Dashboard</Link>
            <Link to="/assessment" onClick={closeMenu} className={isActive('/assessment')}>Take Assessment</Link>
            <Link to="/dashboard"  onClick={closeMenu} className={isActive('/dashboard')}>Career Report</Link>
            <Link to="/history"    onClick={closeMenu} className={isActive('/history')}>History</Link>
          </>
        )}

        {/* NOTIFICATIONS */}
        {user && (
          <div style={{ position: 'relative' }}>
            <button
              type="button"
              onClick={() => { setShowNotifications(s => !s); setShowUserMenu(false); }}
              style={{ background: 'transparent', border: 'none', color: 'var(--text-heading)', fontSize: '1.1rem', cursor: 'pointer', padding: '0.4rem' }}
            >
              🔔
              <span style={{ position: 'absolute', top: 0, right: 0, background: '#ef4444', color: '#fff', borderRadius: '50%', fontSize: '0.6rem', width: '14px', height: '14px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: '900' }}>
                {notifications.length}
              </span>
            </button>

            {showNotifications && (
              <div style={{ position: 'absolute', right: 0, top: '2.5rem', width: '320px', background: 'var(--bg-card)', border: '1px solid var(--border-color)', borderRadius: 'var(--radius-xl)', boxShadow: 'var(--shadow-xl)', zIndex: 200 }}>
                <div style={{ padding: '1rem 1.25rem', borderBottom: '1px solid var(--border-color)' }}>
                  <strong style={{ color: 'var(--text-heading)', fontSize: '0.95rem' }}>Notifications</strong>
                </div>
                {notifications.map((n, i) => (
                  <div key={i} style={{ padding: '0.85rem 1.25rem', borderBottom: '1px solid var(--border-color)', display: 'flex', gap: '0.75rem', alignItems: 'flex-start', cursor: 'pointer' }}>
                    <span style={{ fontSize: '1.2rem' }}>{n.icon}</span>
                    <div>
                      <p style={{ fontSize: '0.85rem', color: 'var(--text-primary)', margin: 0 }}>{n.text}</p>
                      <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{n.time}</span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* THEME TOGGLE */}
        <button
          type="button"
          onClick={toggleTheme}
          className="theme-toggle"
          title={theme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
        >
          {theme === 'dark' ? '☀️' : '🌙'}
        </button>

        {/* USER AVATAR + MENU */}
        {user ? (
          <div style={{ position: 'relative' }}>
            <button
              type="button"
              onClick={() => { setShowUserMenu(s => !s); setShowNotifications(false); }}
              style={{ background: 'var(--primary-gradient)', border: 'none', color: '#fff', borderRadius: '50%', width: '36px', height: '36px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: '800', fontSize: '0.85rem', cursor: 'pointer' }}
            >
              {(user.full_name || user.name || 'U')[0].toUpperCase()}
            </button>

            {showUserMenu && (
              <div style={{ position: 'absolute', right: 0, top: '2.75rem', width: '220px', background: 'var(--bg-card)', border: '1px solid var(--border-color)', borderRadius: 'var(--radius-xl)', boxShadow: 'var(--shadow-xl)', zIndex: 200 }}>
                <div style={{ padding: '1rem 1.25rem', borderBottom: '1px solid var(--border-color)' }}>
                  <p style={{ fontWeight: '700', color: 'var(--text-heading)', margin: 0, fontSize: '0.9rem' }}>{user.full_name || user.name}</p>
                  <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', margin: 0 }}>{user.email}</p>
                </div>
                <Link to="/settings" onClick={closeMenu} style={{ display: 'block', padding: '0.75rem 1.25rem', color: 'var(--text-primary)', textDecoration: 'none', fontSize: '0.9rem', borderBottom: '1px solid var(--border-color)' }}>
                  ⚙️ Profile Settings
                </Link>
                <Link to="/history" onClick={closeMenu} style={{ display: 'block', padding: '0.75rem 1.25rem', color: 'var(--text-primary)', textDecoration: 'none', fontSize: '0.9rem', borderBottom: '1px solid var(--border-color)' }}>
                  📋 Assessment History
                </Link>
                <button onClick={handleLogout} style={{ display: 'block', width: '100%', textAlign: 'left', padding: '0.75rem 1.25rem', background: 'none', border: 'none', color: '#ef4444', fontSize: '0.9rem', cursor: 'pointer', fontWeight: '600' }}>
                  🚪 Logout
                </button>
              </div>
            )}
          </div>
        ) : (
          <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center' }}>
            <Link to="/login"    onClick={closeMenu} className="secondary-btn" style={{ padding: '0.5rem 1rem', fontSize: '0.85rem' }}>Login</Link>
            <Link to="/register" onClick={closeMenu} className="primary-btn"   style={{ padding: '0.5rem 1rem', fontSize: '0.85rem' }}>Get Started</Link>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
