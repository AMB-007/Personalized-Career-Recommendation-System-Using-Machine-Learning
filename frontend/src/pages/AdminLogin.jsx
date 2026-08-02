import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';

const AdminLogin = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await axios.post('/api/auth/login', formData);
      if (response.data.status === 'success') {
        const user = response.data.user;
        
        // Verify admin privileges
        if (user.role === 'admin' || user.email?.includes('admin')) {
          localStorage.setItem('token', response.data.token);
          localStorage.setItem('user', JSON.stringify(user));
          navigate('/admin');
        } else {
          setError('Access Denied: Administrator privileges required for this portal.');
        }
      }
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.error || 'Authentication failed. Please check your credentials.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card admin-auth-card">
        <div style={{ textAlign: 'center', marginBottom: '1rem' }}>
          <span style={{ fontSize: '2.5rem' }}>🛡️</span>
        </div>
        <h2 style={{ textAlign: 'center', color: '#f59e0b' }}>Admin Portal Access</h2>
        <p className="auth-subtitle" style={{ textAlign: 'center' }}>
          Sign in with administrator credentials to manage the platform
        </p>

        {error && <div className="error-banner">{error}</div>}

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label>Admin Email:</label>
            <input 
              type="email" 
              name="email" 
              value={formData.email} 
              onChange={handleChange} 
              required 
              placeholder="admin@example.com"
            />
          </div>

          <div className="form-group">
            <label>Password:</label>
            <input 
              type="password" 
              name="password" 
              value={formData.password} 
              onChange={handleChange} 
              required 
              placeholder="••••••••"
            />
          </div>

          <button 
            type="submit" 
            className="primary-btn" 
            disabled={loading}
            style={{
              background: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
              borderColor: '#f59e0b'
            }}
          >
            {loading ? 'Authenticating Admin...' : 'Sign In to Admin Portal'}
          </button>
        </form>

        <p className="auth-footer" style={{ marginTop: '1.5rem', textAlign: 'center' }}>
          Standard user or student? <Link to="/login">Student Sign In</Link>
        </p>
      </div>
    </div>
  );
};

export default AdminLogin;
