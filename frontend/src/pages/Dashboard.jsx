import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';

const Dashboard = () => {
  const navigate  = useNavigate();
  const [dashData, setDashData]     = useState(null);
  const [loading, setLoading]       = useState(true);
  const [activeTab, setActiveTab]   = useState('overview');

  // Load from API (if auth token exists) or localStorage fallback
  useEffect(() => {
    const loadDashboard = async () => {
      const token  = localStorage.getItem('authToken') || localStorage.getItem('token');
      const userStr = localStorage.getItem('userInfo') || localStorage.getItem('user');
      const user    = userStr ? JSON.parse(userStr) : null;

      if (token && user) {
        try {
          const res = await axios.get('http://127.0.0.1:5000/api/dashboard', {
            headers: { Authorization: `Bearer ${token}` }
          });
          setDashData(res.data);
        } catch {
          // fallback to localStorage
          loadFromLocalStorage(user);
        }
      } else {
        loadFromLocalStorage(user);
      }
      setLoading(false);
    };

    const loadFromLocalStorage = (user) => {
      const top5Str    = localStorage.getItem('top5Careers');
      const readiness  = parseFloat(localStorage.getItem('readinessScore') || '0');
      const xaiStr     = localStorage.getItem('xaiAttributions');
      const top5       = top5Str ? JSON.parse(top5Str) : [];
      const xai        = xaiStr  ? JSON.parse(xaiStr)  : [];
      setDashData({
        user: user || { full_name: 'Student', email: 'student@example.com' },
        readiness_score: readiness || (top5.length > 0 ? Math.round(top5[0]?.confidence || 78) : 78),
        top5_careers: top5,
        xai,
        history: [],
        sessions: [],
      });
    };

    loadDashboard();
  }, []);

  if (loading) {
    return (
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minHeight: '60vh', gap: '1rem' }}>
        <div style={{ fontSize: '3rem' }}>⏳</div>
        <p style={{ color: 'var(--text-muted)', fontWeight: '600' }}>Loading your career dashboard...</p>
      </div>
    );
  }

  const { user, readiness_score, top5_careers } = dashData || {};
  const top5 = top5_careers || [];
  const hasResults = top5.length > 0;

  const readinessColor =
    readiness_score >= 80 ? 'var(--color-emerald)' :
    readiness_score >= 60 ? '#f59e0b' : '#ef4444';

  return (
    <div className="dashboard-container" style={{ maxWidth: '1200px', margin: '0 auto', padding: '2rem 1.5rem' }}>

      {/* ── WELCOME BANNER ── */}
      <div style={{ background: 'var(--primary-gradient)', borderRadius: 'var(--radius-2xl)', padding: '2rem 2.5rem', marginBottom: '2rem', position: 'relative', overflow: 'hidden' }}>
        <div style={{ position: 'absolute', right: '-20px', top: '-20px', width: '200px', height: '200px', background: 'rgba(255,255,255,0.05)', borderRadius: '50%' }} />
        <div style={{ position: 'relative', zIndex: 1 }}>
          <span style={{ fontSize: '0.8rem', fontWeight: '700', color: 'rgba(255,255,255,0.7)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Student Dashboard</span>
          <h1 style={{ color: '#fff', fontSize: '2rem', fontWeight: '900', margin: '0.35rem 0' }}>
            Welcome back, {user?.full_name?.split(' ')[0] || 'Student'}! 👋
          </h1>
          <p style={{ color: 'rgba(255,255,255,0.85)', fontSize: '0.95rem', marginBottom: '1.25rem' }}>
            {hasResults ? 'Your AI career assessment is complete. Explore your personalized recommendations.' : 'Start your adaptive career assessment to unlock personalized recommendations.'}
          </p>
          {!hasResults && (
            <Link to="/assessment" className="primary-btn" style={{ background: '#fff', color: 'var(--color-primary)', fontWeight: '800', padding: '0.75rem 1.75rem', textDecoration: 'none', borderRadius: 'var(--radius-lg)', display: 'inline-block' }}>
              Start Assessment &rarr;
            </Link>
          )}
        </div>
      </div>

      {/* ── METRIC CARDS ── */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1.25rem', marginBottom: '2rem' }}>
        {[
          { icon: '🎯', label: 'Career Readiness Score', value: `${Math.round(readiness_score || 0)}%`, color: readinessColor, sub: 'Based on full assessment' },
          { icon: '🏆', label: 'Top Career Match', value: top5[0]?.career || 'Not assessed', color: 'var(--color-primary-light)', sub: top5[0] ? `${top5[0].confidence}% confidence` : 'Take assessment first' },
          { icon: '🔬', label: 'Skills Verified', value: `${top5.length > 0 ? '3+' : '0'} Skills`, color: '#f59e0b', sub: 'ML-verified skill scores' },
          { icon: '📋', label: 'Assessments Taken', value: dashData?.sessions?.length || (hasResults ? 1 : 0), color: '#8b5cf6', sub: 'Total sessions completed' },
        ].map((m, i) => (
          <div key={i} style={{ background: 'var(--bg-card)', padding: '1.5rem', borderRadius: 'var(--radius-xl)', border: '1px solid var(--border-color)' }}>
            <div style={{ fontSize: '1.5rem', marginBottom: '0.5rem' }}>{m.icon}</div>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: '700', textTransform: 'uppercase' }}>{m.label}</span>
            <div style={{ fontSize: '1.4rem', fontWeight: '900', color: m.color, margin: '0.25rem 0' }}>{m.value}</div>
            <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>{m.sub}</span>
          </div>
        ))}
      </div>

      {hasResults ? (
        <>
          {/* ── TOP 5 CAREER MATCHES ── */}
          <div style={{ background: 'var(--bg-card)', padding: '2rem', borderRadius: 'var(--radius-2xl)', border: '1px solid var(--border-color)', marginBottom: '2rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem', flexWrap: 'wrap', gap: '0.75rem' }}>
              <div>
                <h2 style={{ fontSize: '1.25rem', fontWeight: '800', color: 'var(--text-heading)' }}>🤖 AI-Predicted Career Matches</h2>
                <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>LightGBM model · 272 career labels · SHAP explainability</p>
              </div>
              <Link to="/assessment" style={{ padding: '0.6rem 1.25rem', background: 'var(--primary-gradient)', color: '#fff', borderRadius: 'var(--radius-lg)', fontWeight: '700', fontSize: '0.85rem', textDecoration: 'none' }}>
                Retake Assessment
              </Link>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              {top5.map((career, idx) => (
                <div key={idx} style={{ background: idx === 0 ? 'linear-gradient(135deg, rgba(99,102,241,0.08), rgba(139,92,246,0.08))' : 'var(--bg-card-subtle)', padding: '1.5rem', borderRadius: 'var(--radius-xl)', border: idx === 0 ? '1px solid rgba(99,102,241,0.3)' : '1px solid var(--border-color)', position: 'relative', overflow: 'hidden' }}>
                  {idx === 0 && (
                    <span style={{ position: 'absolute', top: '0.75rem', right: '0.75rem', background: 'var(--primary-gradient)', color: '#fff', padding: '0.25rem 0.65rem', borderRadius: 'var(--radius-full)', fontSize: '0.72rem', fontWeight: '800' }}>
                      #1 TOP MATCH
                    </span>
                  )}
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '0.75rem' }}>
                    <div style={{ flex: 1 }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', flexWrap: 'wrap' }}>
                        <span style={{ background: 'var(--badge-bg)', color: 'var(--badge-text)', padding: '0.2rem 0.6rem', borderRadius: 'var(--radius-full)', fontSize: '0.75rem', fontWeight: '800' }}>
                          #{career.rank || idx + 1}
                        </span>
                        <h3 style={{ fontSize: '1.1rem', fontWeight: '800', color: 'var(--text-heading)', margin: 0 }}>{career.career}</h3>
                      </div>
                      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.4rem', marginTop: '0.75rem' }}>
                        {(career.why || []).map((w, wi) => (
                          <span key={wi} style={{ background: 'rgba(16,185,129,0.1)', color: 'var(--color-emerald)', padding: '0.2rem 0.55rem', borderRadius: '4px', fontSize: '0.75rem', fontWeight: '700' }}>
                            {w}
                          </span>
                        ))}
                      </div>
                    </div>
                    <div style={{ textAlign: 'right', minWidth: '120px' }}>
                      <div style={{ fontSize: '2rem', fontWeight: '900', color: idx === 0 ? 'var(--color-primary-light)' : 'var(--text-heading)' }}>
                        {career.confidence}%
                      </div>
                      <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: '600' }}>Confidence</div>
                    </div>
                  </div>

                  {/* Confidence bar */}
                  <div style={{ marginTop: '1rem', height: '4px', background: 'var(--border-color)', borderRadius: '99px', overflow: 'hidden' }}>
                    <div style={{ height: '100%', width: `${career.confidence}%`, background: idx === 0 ? 'var(--primary-gradient)' : 'rgba(99,102,241,0.4)', borderRadius: '99px', transition: 'width 1s ease' }} />
                  </div>

                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))', gap: '0.75rem', marginTop: '1rem' }}>
                    {[
                      { icon: '💰', label: 'Salary', val: career.salary },
                      { icon: '🎓', label: 'Degree', val: career.degree },
                      { icon: '🏢', label: 'Companies', val: career.companies },
                      { icon: '📈', label: 'Growth', val: career.growth },
                    ].map((item, ii) => (
                      <div key={ii}>
                        <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', fontWeight: '600', marginBottom: '0.15rem' }}>{item.icon} {item.label}</div>
                        <div style={{ fontSize: '0.82rem', fontWeight: '700', color: 'var(--text-primary)' }}>{item.val || '—'}</div>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* ── LEARNING ROADMAP ── */}
          <div style={{ background: 'var(--bg-card)', padding: '2rem', borderRadius: 'var(--radius-2xl)', border: '1px solid var(--border-color)', marginBottom: '2rem' }}>
            <h2 style={{ fontSize: '1.25rem', fontWeight: '800', color: 'var(--text-heading)', marginBottom: '1.5rem' }}>🗺️ Personalized Learning Roadmap</h2>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem' }}>
              {[
                { step: '01', title: 'Strengthen Core Skills', desc: 'Master the key technical & soft skills identified in your assessment.', color: '#6366f1' },
                { step: '02', title: 'Earn Certifications', desc: `Get certified: ${top5[0]?.certifications || 'Domain certifications'}.`, color: '#8b5cf6' },
                { step: '03', title: 'Build Portfolio Projects', desc: 'Work on 2–3 real-world projects aligned to your top career.', color: '#10b981' },
                { step: '04', title: 'Apply & Network', desc: `Target recruiters: ${top5[0]?.companies || 'Industry leaders'}.`, color: '#f59e0b' },
              ].map((r, ri) => (
                <div key={ri} style={{ padding: '1.25rem', background: 'var(--bg-card-subtle)', borderRadius: 'var(--radius-xl)', border: '1px solid var(--border-color)', borderTop: `3px solid ${r.color}` }}>
                  <span style={{ fontWeight: '900', color: r.color, fontSize: '1.5rem' }}>{r.step}</span>
                  <h4 style={{ color: 'var(--text-heading)', fontWeight: '700', margin: '0.35rem 0', fontSize: '0.95rem' }}>{r.title}</h4>
                  <p style={{ color: 'var(--text-muted)', fontSize: '0.82rem', lineHeight: '1.5' }}>{r.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </>
      ) : (
        /* ── EMPTY STATE ── */
        <div style={{ background: 'var(--bg-card)', padding: '3rem', borderRadius: 'var(--radius-2xl)', border: '1px solid var(--border-color)', textAlign: 'center' }}>
          <div style={{ fontSize: '4rem', marginBottom: '1rem' }}>🎯</div>
          <h2 style={{ fontSize: '1.5rem', fontWeight: '800', color: 'var(--text-heading)', marginBottom: '0.5rem' }}>No Assessment Results Yet</h2>
          <p style={{ color: 'var(--text-muted)', maxWidth: '460px', margin: '0 auto 2rem', fontSize: '0.95rem' }}>
            Complete the AI Career Assessment to unlock your personalized Top 5 Career Recommendations, SHAP explanations, and Learning Roadmap.
          </p>
          <Link to="/assessment" className="primary-btn" style={{ padding: '0.9rem 2rem', fontWeight: '800', fontSize: '1rem', textDecoration: 'none', display: 'inline-block' }}>
            Start AI Assessment &rarr;
          </Link>
        </div>
      )}
    </div>
  );
};

export default Dashboard;