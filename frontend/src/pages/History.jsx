import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';

const History = () => {
  const navigate = useNavigate();
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const userStr = localStorage.getItem('user');
  const user = userStr ? JSON.parse(userStr) : null;

  useEffect(() => {
    if (!user) {
      navigate('/login');
      return;
    }

    fetchHistory(user.id);
  }, []);

  const fetchHistory = async (userId) => {
    try {
      const response = await axios.get(`http://127.0.0.1:5000/api/assessment/history/${userId}`);
      if (response.data.status === 'success') {
        setHistory(response.data.history || []);
      }
    } catch (err) {
      console.error(err);
      setError('Failed to load assessment history.');
    } finally {
      setLoading(false);
    }
  };

  const handleViewDashboard = (item) => {
    localStorage.setItem('finalRecommendedCareer', item.recommended_career);
    localStorage.setItem('recommendedCareer', item.recommended_career);
    localStorage.setItem('riasecTrait', item.riasec_trait);
    localStorage.setItem('verifiedScore', item.verified_score);
    navigate('/dashboard');
  };

  const maxScore = history.length ? Math.max(...history.map(h => h.verified_score || 0)) : 0;
  const latestCareer = history.length ? history[0].recommended_career : 'None';

  return (
    <div className="history-page-wrapper">
      {/* 1. HEADER CARD */}
      <div className="history-header-card">
        <div className="header-info">
          <span className="section-eyebrow">ASSESSMENT ARCHIVE</span>
          <h2>Career Assessment History</h2>
          <p className="subtitle">
            Past AI-recommended career tracks and verified evaluation results for <strong>{user?.full_name}</strong>
          </p>
        </div>

        <button className="primary-btn new-assessment-btn" onClick={() => navigate('/assessment')}>
          <span>+ Take New Assessment</span>
        </button>
      </div>

      {/* 2. STATS STRIP */}
      {history.length > 0 && (
        <div className="history-stats-bar">
          <div className="stat-card">
            <span className="stat-num">{history.length}</span>
            <span className="stat-lbl">Assessments Completed</span>
          </div>
          <div className="stat-card">
            <span className="stat-num highlight">{latestCareer}</span>
            <span className="stat-lbl">Latest Recommended Track</span>
          </div>
          <div className="stat-card">
            <span className="stat-num green">{maxScore}%</span>
            <span className="stat-lbl">Top Verified Skill Score</span>
          </div>
        </div>
      )}

      {/* 3. CONTENT AREA */}
      {loading ? (
        <div className="history-loading-card">
          <p>⏳ Loading assessment history records...</p>
        </div>
      ) : error ? (
        <div className="error-banner">{error}</div>
      ) : history.length === 0 ? (
        <div className="empty-history-card">
          <div className="empty-icon">📊</div>
          <h3>No Past Assessments Found</h3>
          <p>You haven't completed any AI Career Assessments yet. Take your first 10-minute assessment to unlock personalized recommendations!</p>
          <button className="primary-btn" onClick={() => navigate('/assessment')} style={{ marginTop: '1rem', width: 'auto', padding: '0.85rem 1.75rem' }}>
            Start Your Assessment →
          </button>
        </div>
      ) : (
        <div className="history-cards-grid">
          {history.map((item) => {
            const dateObj = new Date(item.created_at);
            const dateFormatted = isNaN(dateObj) 
              ? 'Recent' 
              : `${dateObj.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })} at ${dateObj.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`;

            const isPassed = item.verified_score >= 70;

            return (
              <div key={item.id} className="history-record-card">
                <div className="record-header">
                  <span className="record-date">📅 {dateFormatted}</span>
                  <span className="tier-tag">{item.education_level || 'General'}</span>
                </div>

                <div className="record-body">
                  <span className="record-label">AI Recommended Direction</span>
                  <h3 className="record-title">{item.recommended_career}</h3>

                  <div className="record-metrics-row">
                    <div className="metric-cell">
                      <span>RIASEC Trait</span>
                      <strong className="trait-badge">{item.riasec_trait}</strong>
                    </div>

                    <div className="metric-cell">
                      <span>Verified Score</span>
                      <strong className={`score-badge ${isPassed ? 'green' : 'amber'}`}>
                        {item.verified_score}%
                      </strong>
                    </div>
                  </div>

                  <div className="score-progress-bar">
                    <div 
                      className={`progress-fill ${isPassed ? 'green' : 'amber'}`} 
                      style={{ width: `${Math.min(100, Math.max(5, item.verified_score))}%` }} 
                    />
                  </div>
                </div>

                <div className="record-footer">
                  <button 
                    className="view-dashboard-btn" 
                    onClick={() => handleViewDashboard(item)}
                  >
                    <span>View Full Dashboard</span>
                    <span className="arrow">→</span>
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default History;
