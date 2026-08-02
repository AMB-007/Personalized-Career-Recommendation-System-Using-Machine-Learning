import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';

const Register = () => {
  const navigate = useNavigate();
  const [form, setForm] = useState({ full_name: '', email: '', password: '', confirm_password: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    if (form.password !== form.confirm_password) { setError('Passwords do not match'); return; }
    if (form.password.length < 6) { setError('Password must be at least 6 characters'); return; }

    setLoading(true);
    try {
      const res = await axios.post('http://127.0.0.1:5000/api/auth/register', form);
      const { token, user } = res.data;
      localStorage.setItem('authToken', token);
      localStorage.setItem('userInfo', JSON.stringify(user));
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.error || 'Registration failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '2rem' }}>
      <div className="auth-card" style={{ width: '100%', maxWidth: '480px', background: 'var(--bg-card)', borderRadius: 'var(--radius-2xl)', border: '1px solid var(--border-color)', padding: '2.5rem' }}>
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <div style={{ fontSize: '2.5rem', marginBottom: '0.5rem' }}>🎯</div>
          <h1 style={{ fontSize: '1.75rem', fontWeight: '800', color: 'var(--text-heading)' }}>Create Account</h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginTop: '0.25rem' }}>
            Start your AI career assessment journey
          </p>
        </div>

        {error && (
          <div style={{ background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.3)', color: '#ef4444', padding: '0.75rem 1rem', borderRadius: 'var(--radius-lg)', marginBottom: '1.5rem', fontSize: '0.9rem' }}>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          <div className="form-group">
            <label>Full Name *</label>
            <input type="text" name="full_name" value={form.full_name} onChange={handleChange} placeholder="Your full name" required />
          </div>
          <div className="form-group">
            <label>Email Address *</label>
            <input type="email" name="email" value={form.email} onChange={handleChange} placeholder="you@example.com" required />
          </div>
          <div className="form-group">
            <label>Password *</label>
            <input type="password" name="password" value={form.password} onChange={handleChange} placeholder="Minimum 6 characters" required />
          </div>
          <div className="form-group">
            <label>Confirm Password *</label>
            <input type="password" name="confirm_password" value={form.confirm_password} onChange={handleChange} placeholder="Re-enter your password" required />
          </div>

          <button type="submit" className="primary-btn" disabled={loading} style={{ padding: '0.9rem', fontWeight: '800', fontSize: '1rem', marginTop: '0.5rem' }}>
            {loading ? '⏳ Creating Account...' : '🚀 Create Account & Start Assessment'}
          </button>
        </form>

        <p style={{ textAlign: 'center', marginTop: '1.5rem', color: 'var(--text-muted)', fontSize: '0.9rem' }}>
          Already have an account?{' '}
          <Link to="/login" style={{ color: 'var(--color-primary-light)', fontWeight: '700', textDecoration: 'none' }}>Sign In</Link>
        </p>
      </div>
    </div>
  );
};

export default Register;
