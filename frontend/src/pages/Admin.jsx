import { useState, useEffect } from 'react';
import axios from 'axios';

const API = 'http://127.0.0.1:5000';

const Admin = () => {
  const [activeTab, setActiveTab]   = useState('overview');
  const [analytics, setAnalytics]   = useState(null);
  const [users, setUsers]           = useState([]);
  const [questions, setQuestions]   = useState([]);
  const [totalQ, setTotalQ]         = useState(0);
  const [qPage, setQPage]           = useState(1);
  const [loading, setLoading]       = useState(false);
  const [retraining, setRetraining] = useState(false);
  const [newQ, setNewQ]             = useState({ question_text: '', category: 'Logical Reasoning', difficulty: 'Medium', education_level: 'All', board: 'All', stream: 'All', degree: 'All', option_a: '', option_b: '', option_c: '', option_d: '', correct_answer: 'A', weight: 1.0, expected_time: 60, status: 'Active' });

  const token  = localStorage.getItem('authToken') || localStorage.getItem('token');
  const headers = { Authorization: `Bearer ${token}` };

  const userStr = localStorage.getItem('userInfo') || localStorage.getItem('user');
  const user    = userStr ? JSON.parse(userStr) : null;

  useEffect(() => {
    if (user?.role !== 'admin') {
      window.location.href = '/admin-login';
      return;
    }
    fetchAnalytics();
  }, []);

  useEffect(() => {
    if (activeTab === 'users')     fetchUsers();
    if (activeTab === 'questions') fetchQuestions();
  }, [activeTab, qPage]);

  const fetchAnalytics = async () => {
    try {
      const res = await axios.get(`${API}/api/admin/analytics`, { headers });
      setAnalytics(res.data);
    } catch (e) {
      console.error(e);
      setAnalytics({ total_students: 0, total_assessments: 0, total_questions: 0, top_careers: [], daily_trend: [] });
    }
  };

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const res = await axios.get(`${API}/api/admin/users`, { headers });
      setUsers(res.data.users || []);
    } catch { setUsers([]); } finally { setLoading(false); }
  };

  const fetchQuestions = async () => {
    setLoading(true);
    try {
      const res = await axios.get(`${API}/api/admin/questions?page=${qPage}&limit=20`, { headers });
      setQuestions(res.data.questions || []);
      setTotalQ(res.data.total || 0);
    } catch { setQuestions([]); } finally { setLoading(false); }
  };

  const deleteUser = async (uid) => {
    if (!confirm('Delete this user?')) return;
    try { await axios.delete(`${API}/api/admin/users/${uid}`, { headers }); fetchUsers(); } catch { alert('Error deleting user.'); }
  };

  const addQuestion = async () => {
    try {
      await axios.post(`${API}/api/admin/questions`, newQ, { headers });
      alert('Question added!');
      setNewQ({ question_text: '', category: 'Logical Reasoning', difficulty: 'Medium', education_level: 'All', board: 'All', stream: 'All', degree: 'All', option_a: '', option_b: '', option_c: '', option_d: '', correct_answer: 'A', weight: 1.0, expected_time: 60, status: 'Active' });
      fetchQuestions();
    } catch { alert('Error adding question.'); }
  };

  const deleteQuestion = async (qid) => {
    if (!confirm('Delete this question?')) return;
    try { await axios.delete(`${API}/api/admin/questions/${qid}`, { headers }); fetchQuestions(); } catch { alert('Error.'); }
  };

  const handleRetrain = async () => {
    setRetraining(true);
    try {
      await axios.post(`${API}/api/admin/retrain`, {}, { headers });
      alert('Model retraining started! Check server logs for progress.');
    } catch { alert('Retraining failed. Check server.'); } finally { setRetraining(false); }
  };

  const tabStyle = (t) => ({
    padding: '0.6rem 1.25rem',
    background: activeTab === t ? 'var(--primary-gradient)' : 'var(--bg-card-subtle)',
    color: activeTab === t ? '#fff' : 'var(--text-muted)',
    border: '1px solid var(--border-color)',
    borderRadius: 'var(--radius-lg)',
    cursor: 'pointer',
    fontWeight: '700',
    fontSize: '0.85rem',
    whiteSpace: 'nowrap',
  });

  const cardStyle = { background: 'var(--bg-card)', padding: '1.5rem', borderRadius: 'var(--radius-xl)', border: '1px solid var(--border-color)' };

  return (
    <div style={{ maxWidth: '1300px', margin: '0 auto', padding: '2rem 1.5rem' }}>
      {/* ADMIN HEADER */}
      <div style={{ background: 'var(--primary-gradient)', borderRadius: 'var(--radius-2xl)', padding: '2rem 2.5rem', marginBottom: '2rem' }}>
        <span style={{ fontSize: '0.8rem', fontWeight: '700', color: 'rgba(255,255,255,0.7)', textTransform: 'uppercase' }}>Admin Control Center</span>
        <h1 style={{ color: '#fff', fontSize: '2rem', fontWeight: '900', margin: '0.3rem 0 0.25rem' }}>System Administration 👑</h1>
        <p style={{ color: 'rgba(255,255,255,0.8)', fontSize: '0.9rem' }}>Manage users, question banks, ML model, and system analytics.</p>
      </div>

      {/* TABS */}
      <div style={{ display: 'flex', gap: '0.5rem', overflowX: 'auto', paddingBottom: '0.5rem', marginBottom: '2rem' }}>
        {[['overview','📊 Overview'],['users','👥 Users'],['questions','❓ Questions'],['model','🤖 ML Model']].map(([t, l]) => (
          <button key={t} type="button" onClick={() => setActiveTab(t)} style={tabStyle(t)}>{l}</button>
        ))}
      </div>

      {/* OVERVIEW TAB */}
      {activeTab === 'overview' && (
        <div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1.25rem', marginBottom: '2rem' }}>
            {[
              { icon: '👥', label: 'Total Students', val: analytics?.total_students ?? '—', color: '#6366f1' },
              { icon: '📋', label: 'Total Assessments', val: analytics?.total_assessments ?? '—', color: '#10b981' },
              { icon: '❓', label: 'Active Questions', val: analytics?.total_questions ?? '—', color: '#f59e0b' },
              { icon: '🎯', label: 'Career Labels', val: 272, color: '#8b5cf6' },
            ].map((m, i) => (
              <div key={i} style={{ ...cardStyle, borderTop: `3px solid ${m.color}` }}>
                <div style={{ fontSize: '1.5rem' }}>{m.icon}</div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: '700', textTransform: 'uppercase', margin: '0.35rem 0 0.2rem' }}>{m.label}</div>
                <div style={{ fontSize: '2rem', fontWeight: '900', color: m.color }}>{m.val}</div>
              </div>
            ))}
          </div>

          {analytics?.top_careers?.length > 0 && (
            <div style={cardStyle}>
              <h3 style={{ fontWeight: '800', color: 'var(--text-heading)', marginBottom: '1.25rem' }}>Top 10 Predicted Careers</h3>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.65rem' }}>
                {analytics.top_careers.map((c, ci) => (
                  <div key={ci} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '0.65rem 0.85rem', background: 'var(--bg-card-subtle)', borderRadius: 'var(--radius-lg)' }}>
                    <span style={{ fontWeight: '700', color: 'var(--text-primary)', fontSize: '0.9rem' }}>#{ci+1} {c.top1_career}</span>
                    <span style={{ fontWeight: '900', color: 'var(--color-primary-light)' }}>{c.count} assessments</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* USERS TAB */}
      {activeTab === 'users' && (
        <div style={cardStyle}>
          <h3 style={{ fontWeight: '800', color: 'var(--text-heading)', marginBottom: '1.5rem' }}>Student Accounts ({users.length})</h3>
          {loading ? <p>Loading...</p> : (
            <div style={{ overflowX: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.87rem' }}>
                <thead>
                  <tr style={{ background: 'var(--bg-card-subtle)', textAlign: 'left' }}>
                    {['ID','Name','Email','Role','Assessments','Joined','Actions'].map(h => (
                      <th key={h} style={{ padding: '0.75rem', fontWeight: '700', color: 'var(--text-muted)', fontSize: '0.8rem', textTransform: 'uppercase' }}>{h}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {users.map(u => (
                    <tr key={u.id} style={{ borderBottom: '1px solid var(--border-color)' }}>
                      <td style={{ padding: '0.75rem', color: 'var(--text-muted)' }}>#{u.id}</td>
                      <td style={{ padding: '0.75rem', fontWeight: '700', color: 'var(--text-heading)' }}>{u.full_name}</td>
                      <td style={{ padding: '0.75rem', color: 'var(--text-muted)' }}>{u.email}</td>
                      <td style={{ padding: '0.75rem' }}>
                        <span style={{ padding: '0.2rem 0.55rem', background: u.role === 'admin' ? 'rgba(239,68,68,0.15)' : 'rgba(16,185,129,0.15)', color: u.role === 'admin' ? '#ef4444' : 'var(--color-emerald)', borderRadius: '4px', fontSize: '0.75rem', fontWeight: '700' }}>
                          {u.role}
                        </span>
                      </td>
                      <td style={{ padding: '0.75rem', fontWeight: '700' }}>{u.assessments || 0}</td>
                      <td style={{ padding: '0.75rem', color: 'var(--text-muted)' }}>{u.created_at ? new Date(u.created_at).toLocaleDateString() : '—'}</td>
                      <td style={{ padding: '0.75rem' }}>
                        {u.role !== 'admin' && (
                          <button onClick={() => deleteUser(u.id)} style={{ padding: '0.3rem 0.65rem', background: 'rgba(239,68,68,0.1)', color: '#ef4444', border: '1px solid rgba(239,68,68,0.3)', borderRadius: '6px', cursor: 'pointer', fontSize: '0.8rem', fontWeight: '700' }}>
                            Delete
                          </button>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      {/* QUESTIONS TAB */}
      {activeTab === 'questions' && (
        <div>
          {/* ADD QUESTION FORM */}
          <div style={{ ...cardStyle, marginBottom: '1.5rem' }}>
            <h3 style={{ fontWeight: '800', color: 'var(--text-heading)', marginBottom: '1.25rem' }}>+ Add New Question</h3>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1rem' }}>
              <div className="form-group" style={{ gridColumn: '1 / -1' }}>
                <label>Question Text *</label>
                <textarea value={newQ.question_text} onChange={e => setNewQ(q => ({ ...q, question_text: e.target.value }))} rows={3} style={{ width: '100%', resize: 'vertical' }} />
              </div>
              {[
                ['Category', 'category', ['Logical Reasoning','Numerical Reasoning','Science Aptitude','Algorithms','Database Systems','Machine Learning','Psychometric','Career Interest','Skill Verification','Mathematics','Financial Accounting']],
                ['Difficulty', 'difficulty', ['Easy','Medium','Hard']],
                ['Education Level', 'education_level', ['All','Class 7','Class 8','Class 9','Class 10','Higher Secondary','Undergraduate','Postgraduate']],
                ['Board', 'board', ['All','CBSE','Kerala State Board','ICSE']],
                ['Stream', 'stream', ['All','Science (PCM)','Science (PCB)','Commerce','Humanities/Arts']],
                ['Correct Answer', 'correct_answer', ['A','B','C','D']],
              ].map(([l, k, opts]) => (
                <div key={k} className="form-group">
                  <label>{l}</label>
                  <select value={newQ[k]} onChange={e => setNewQ(q => ({ ...q, [k]: e.target.value }))}>
                    {opts.map(o => <option key={o}>{o}</option>)}
                  </select>
                </div>
              ))}
              {['option_a','option_b','option_c','option_d'].map(opt => (
                <div key={opt} className="form-group">
                  <label>Option {opt.slice(-1).toUpperCase()}</label>
                  <input type="text" value={newQ[opt]} onChange={e => setNewQ(q => ({ ...q, [opt]: e.target.value }))} />
                </div>
              ))}
            </div>
            <button type="button" className="primary-btn" onClick={addQuestion} style={{ marginTop: '1rem' }}>
              + Add Question to Bank
            </button>
          </div>

          {/* QUESTION LIST */}
          <div style={cardStyle}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem', flexWrap: 'wrap', gap: '0.75rem' }}>
              <h3 style={{ fontWeight: '800', color: 'var(--text-heading)' }}>Question Bank ({totalQ} questions)</h3>
              <div style={{ display: 'flex', gap: '0.5rem' }}>
                <button type="button" onClick={() => setQPage(p => Math.max(1, p - 1))} disabled={qPage === 1} className="secondary-btn" style={{ padding: '0.45rem 0.85rem', fontSize: '0.82rem' }}>Prev</button>
                <span style={{ padding: '0.45rem 0.85rem', color: 'var(--text-muted)', fontSize: '0.82rem' }}>Page {qPage}</span>
                <button type="button" onClick={() => setQPage(p => p + 1)} disabled={questions.length < 20} className="secondary-btn" style={{ padding: '0.45rem 0.85rem', fontSize: '0.82rem' }}>Next</button>
              </div>
            </div>
            {loading ? <p>Loading...</p> : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                {questions.map(q => (
                  <div key={q.id} style={{ padding: '1rem', background: 'var(--bg-card-subtle)', borderRadius: 'var(--radius-lg)', border: '1px solid var(--border-color)', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '1rem' }}>
                    <div style={{ flex: 1 }}>
                      <p style={{ fontWeight: '700', color: 'var(--text-heading)', fontSize: '0.88rem', margin: '0 0 0.35rem' }}>{q.question_text?.substring(0, 120)}...</p>
                      <div style={{ display: 'flex', gap: '0.4rem', flexWrap: 'wrap' }}>
                        {[q.category, q.difficulty, q.education_level].map((t, ti) => (
                          <span key={ti} style={{ padding: '0.15rem 0.45rem', background: 'var(--badge-bg)', color: 'var(--badge-text)', borderRadius: '4px', fontSize: '0.72rem', fontWeight: '700' }}>{t}</span>
                        ))}
                      </div>
                    </div>
                    <button onClick={() => deleteQuestion(q.id)} style={{ padding: '0.35rem 0.65rem', background: 'rgba(239,68,68,0.1)', color: '#ef4444', border: '1px solid rgba(239,68,68,0.3)', borderRadius: '6px', cursor: 'pointer', fontSize: '0.8rem', fontWeight: '700', flexShrink: 0 }}>
                      Delete
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {/* ML MODEL TAB */}
      {activeTab === 'model' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          <div style={cardStyle}>
            <h3 style={{ fontWeight: '800', color: 'var(--text-heading)', marginBottom: '1rem' }}>🤖 ML Model Status</h3>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginBottom: '1.5rem' }}>
              {[
                { label: 'Model Type', val: 'LightGBM Classifier' },
                { label: 'Training Samples', val: '35,000 rows' },
                { label: 'Career Labels', val: '272 unique careers' },
                { label: 'Feature Columns', val: '38 features' },
                { label: 'Dataset', val: 'career_recommendation_dataset.csv' },
                { label: 'Top-5 Accuracy', val: '25.44%' },
              ].map((item, i) => (
                <div key={i} style={{ padding: '1rem', background: 'var(--bg-card-subtle)', borderRadius: 'var(--radius-lg)', border: '1px solid var(--border-color)' }}>
                  <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', fontWeight: '700', textTransform: 'uppercase', marginBottom: '0.25rem' }}>{item.label}</div>
                  <div style={{ fontWeight: '800', color: 'var(--text-heading)' }}>{item.val}</div>
                </div>
              ))}
            </div>
            <button type="button" className="primary-btn" onClick={handleRetrain} disabled={retraining} style={{ padding: '0.85rem 2rem', fontWeight: '800' }}>
              {retraining ? '⏳ Retraining Started...' : '🔄 Retrain ML Model'}
            </button>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.82rem', marginTop: '0.75rem' }}>
              Retraining runs <code>train_model.py</code> in background using the updated dataset. Monitor server logs.
            </p>
          </div>

          <div style={cardStyle}>
            <h3 style={{ fontWeight: '800', color: 'var(--text-heading)', marginBottom: '1rem' }}>📦 Model Artifacts</h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
              {['career_model_lightgbm.joblib (48 MB)','label_encoder.pkl','feature_encoder.pkl','feature_columns.pkl','scaler.pkl'].map((f, i) => (
                <div key={i} style={{ padding: '0.65rem 1rem', background: 'rgba(16,185,129,0.08)', color: 'var(--color-emerald)', borderRadius: 'var(--radius-lg)', fontWeight: '700', fontSize: '0.88rem', fontFamily: 'monospace' }}>
                  ✓ {f}
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Admin;
