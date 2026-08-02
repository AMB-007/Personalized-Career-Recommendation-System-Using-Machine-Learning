import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const UserSettings = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [formData, setFormData] = useState({
    full_name: '',
    email: '',
    age: 18,
    gender: 'Female',
    country: 'India',
    state: 'Kerala',
    district: 'Ernakulam',
    institution: '',
    language: 'English',
    new_password: '',
    confirm_new_password: ''
  });

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    const userStr = localStorage.getItem('user');
    if (!userStr) {
      navigate('/login');
      return;
    }

    const userData = JSON.parse(userStr);
    setUser(userData);

    const savedExtra = JSON.parse(localStorage.getItem('userExtraDetails') || '{}');
    setFormData({
      full_name: userData.full_name || '',
      email: userData.email || '',
      age: userData.age || 18,
      gender: savedExtra.gender || 'Female',
      country: savedExtra.country || 'India',
      state: savedExtra.state || 'Kerala',
      district: savedExtra.district || 'Ernakulam',
      institution: savedExtra.institution || 'State / CBSE Institution',
      language: savedExtra.language || 'English',
      new_password: '',
      confirm_new_password: ''
    });
  }, [navigate]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');
    setError('');

    if (formData.new_password && formData.new_password !== formData.confirm_new_password) {
      setError('New passwords do not match.');
      setLoading(false);
      return;
    }

    try {
      if (user?.id) {
        await axios.put(`http://127.0.0.1:5000/api/auth/profile/${user.id}`, {
          full_name: formData.full_name,
          age: formData.age
        }).catch(e => console.log('Remote profile note:', e));

        const updatedUser = {
          ...user,
          full_name: formData.full_name,
          age: formData.age
        };
        localStorage.setItem('user', JSON.stringify(updatedUser));
        setUser(updatedUser);
      }

      localStorage.setItem('userExtraDetails', JSON.stringify({
        gender: formData.gender,
        country: formData.country,
        state: formData.state,
        district: formData.district,
        institution: formData.institution,
        language: formData.language
      }));

      setMessage('Profile settings updated successfully!');
    } catch (err) {
      console.error(err);
      setError('Failed to update profile settings.');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteAccount = () => {
    if (window.confirm('CAUTION: Are you sure you want to delete your account? All assessment history will be permanently deleted.')) {
      localStorage.clear();
      navigate('/register');
    }
  };

  if (!user) return null;

  const isAdmin = user.role === 'admin' || user.email?.includes('admin');

  return (
    <div className="settings-container" style={{ maxWidth: '850px', margin: '0 auto' }}>
      <div className="settings-card" style={{ background: 'var(--bg-card)', padding: '2rem', borderRadius: 'var(--radius-2xl)', border: '1px solid var(--border-color)' }}>
        <div className="settings-header" style={{ display: 'flex', alignItems: 'center', gap: '1.25rem', marginBottom: '1.5rem', borderBottom: '1px solid var(--border-color)', paddingBottom: '1.5rem' }}>
          <div className="avatar-large" style={{ fontSize: '2.5rem', width: '70px', height: '70px', background: 'var(--badge-bg)', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            {isAdmin ? '👑' : '👤'}
          </div>
          <div>
            <h2 style={{ fontSize: '1.6rem', fontWeight: '800', color: 'var(--text-heading)' }}>Candidate Profile Settings</h2>
            <p className="subtitle" style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>
              Manage your personal demographics, institution, language preferences, and security.
            </p>
          </div>
        </div>

        {message && <div className="success-banner" style={{ marginBottom: '1rem' }}>✨ {message}</div>}
        {error && <div className="error-banner" style={{ marginBottom: '1rem' }}>{error}</div>}

        <form onSubmit={handleSubmit} className="settings-form">
          <h4 style={{ fontSize: '1.05rem', fontWeight: '800', color: 'var(--text-heading)', marginBottom: '1rem' }}>Personal Demographics</h4>

          <div className="form-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '1.25rem' }}>
            <div className="form-group">
              <label>Full Name *</label>
              <input type="text" name="full_name" value={formData.full_name} onChange={handleChange} required />
            </div>

            <div className="form-group">
              <label>Email Address (Read-Only)</label>
              <input type="email" value={formData.email} disabled className="disabled-input" style={{ opacity: 0.7 }} />
            </div>

            <div className="form-group">
              <label>Age (Years) *</label>
              <input type="number" name="age" min="8" max="100" value={formData.age} onChange={handleChange} required />
            </div>

            <div className="form-group">
              <label>Gender *</label>
              <select name="gender" value={formData.gender} onChange={handleChange}>
                <option value="Female">Female</option>
                <option value="Male">Male</option>
                <option value="Other">Other / Non-Binary</option>
              </select>
            </div>

            <div className="form-group">
              <label>Country *</label>
              <input type="text" name="country" value={formData.country} onChange={handleChange} required />
            </div>

            <div className="form-group">
              <label>State / Region *</label>
              <input type="text" name="state" value={formData.state} onChange={handleChange} required />
            </div>

            <div className="form-group">
              <label>District / City *</label>
              <input type="text" name="district" value={formData.district} onChange={handleChange} required />
            </div>

            <div className="form-group">
              <label>School / College / Institution *</label>
              <input type="text" name="institution" value={formData.institution} onChange={handleChange} required />
            </div>

            <div className="form-group">
              <label>Medium of Instruction / Language *</label>
              <select name="language" value={formData.language} onChange={handleChange}>
                <option value="English">English</option>
                <option value="Malayalam">Malayalam</option>
                <option value="Hindi">Hindi</option>
                <option value="Tamil">Tamil</option>
                <option value="Other">Other Language</option>
              </select>
            </div>
          </div>

          <h4 style={{ fontSize: '1.05rem', fontWeight: '800', color: 'var(--text-heading)', marginTop: '2rem', marginBottom: '1rem' }}>Account Security &amp; Password</h4>
          <div className="form-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '1.25rem' }}>
            <div className="form-group">
              <label>New Password (Optional)</label>
              <input type="password" name="new_password" value={formData.new_password} onChange={handleChange} placeholder="Leave blank to keep current" />
            </div>

            <div className="form-group">
              <label>Confirm New Password</label>
              <input type="password" name="confirm_new_password" value={formData.confirm_new_password} onChange={handleChange} placeholder="Confirm new password" />
            </div>
          </div>

          <div style={{ marginTop: '2rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
            <div style={{ display: 'flex', gap: '1rem' }}>
              <button type="submit" className="primary-btn" disabled={loading} style={{ padding: '0.8rem 1.75rem', fontWeight: '800' }}>
                {loading ? 'Saving Changes...' : 'Save Profile Settings'}
              </button>
              <button type="button" className="secondary-btn" onClick={() => navigate('/dashboard')}>
                Back to Dashboard
              </button>
            </div>

            <button type="button" onClick={handleDeleteAccount} style={{ background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.3)', color: '#ef4444', padding: '0.8rem 1.25rem', borderRadius: 'var(--radius-md)', fontWeight: '700', cursor: 'pointer' }}>
              🗑 Delete Account
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default UserSettings;
