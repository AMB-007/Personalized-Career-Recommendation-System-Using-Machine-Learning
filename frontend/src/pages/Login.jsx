import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';

const Login = () => {
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: '', password: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const res = await axios.post('http://127.0.0.1:5000/api/auth/login', form);
      const { token, user } = res.data;
      localStorage.setItem('authToken', token);
      localStorage.setItem('token', token);
      localStorage.setItem('userInfo', JSON.stringify(user));
      localStorage.setItem('user', JSON.stringify(user));
      if (user.role === 'admin') {
        navigate('/admin');
      } else {
        navigate('/dashboard');
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Invalid email or password.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '2rem' }}>
      <div style={{ width: '100%', maxWidth: '460px', background: 'var(--bg-card)', borderRadius: 'var(--radius-2xl)', border: '1px solid var(--border-color)', padding: '2.5rem' }}>
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <div style={{ fontSize: '2.5rem', marginBottom: '0.5rem' }}>🎯</div>
          <h1 style={{ fontSize: '1.75rem', fontWeight: '800', color: 'var(--text-heading)' }}>Welcome Back</h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>Sign in to continue your career assessment</p>
        </div>

        {error && (
          <div style={{ background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.3)', color: '#ef4444', padding: '0.75rem 1rem', borderRadius: 'var(--radius-lg)', marginBottom: '1.25rem', fontSize: '0.9rem' }}>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          <div className="form-group">
            <label>Email Address</label>
            <input type="email" name="email" value={form.email} onChange={handleChange} placeholder="you@example.com" required />
          </div>
          <div className="form-group">
            <label>Password</label>
            <input type="password" name="password" value={form.password} onChange={handleChange} placeholder="Enter your password" required />
          </div>
          <button type="submit" className="primary-btn" disabled={loading} style={{ padding: '0.9rem', fontWeight: '800', fontSize: '1rem' }}>
            {loading ? '⏳ Signing In...' : '🔐 Sign In'}
          </button>
        </form>

        <div style={{ textAlign: 'center', marginTop: '1.5rem' }}>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
            Don&apos;t have an account?{' '}
            <Link to="/register" style={{ color: 'var(--color-primary-light)', fontWeight: '700', textDecoration: 'none' }}>Create Account</Link>
          </p>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginTop: '0.5rem' }}>
            Admin?{' '}
            <Link to="/admin-login" style={{ color: 'var(--color-primary-light)', fontWeight: '600', textDecoration: 'none' }}>Admin Login</Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;
