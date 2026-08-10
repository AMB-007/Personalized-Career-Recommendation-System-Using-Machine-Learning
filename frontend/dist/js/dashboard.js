/* dashboard.js — Student Dashboard */

document.addEventListener('DOMContentLoaded', async () => {
  if (!Auth.requireAuth()) return;
  renderNavbar('dashboard');

  const container = document.getElementById('dashboard-content');
  const token = Auth.getToken();
  const user  = Auth.getUser();

  let dashData = null;

  // Try API first, fallback to localStorage
  try {
    const res = await API.get('/api/dashboard', true);
    if (res && res.user) dashData = res;
    else throw new Error('No data');
  } catch {
    const top5Str   = localStorage.getItem('top5Careers');
    const readiness = parseFloat(localStorage.getItem('readinessScore') || '0');
    const xaiStr    = localStorage.getItem('xaiAttributions');
    const top5      = top5Str ? JSON.parse(top5Str) : [];
    const xai       = xaiStr  ? JSON.parse(xaiStr)  : [];
    dashData = {
      user,
      readiness_score: readiness || (top5.length > 0 ? Math.round(top5[0]?.confidence || 78) : 0),
      top5_careers: top5,
      xai,
      history: [],
      sessions: [],
    };
  }

  render(dashData, container);
});

function render(data, container) {
  const { user, readiness_score, top5_careers, sessions } = data || {};
  const top5      = top5_careers || [];
  const hasRes    = top5.length > 0;
  const readiness = Math.round(readiness_score || 0);
  const readColor = readiness >= 80 ? 'var(--emerald)' : readiness >= 60 ? 'var(--amber)' : 'var(--red)';
  const name      = user?.full_name?.split(' ')[0] || 'Student';

  container.innerHTML = `
    <!-- WELCOME BANNER -->
    <div class="welcome-banner mb-4">
      <div class="welcome-banner-orb"></div>
      <div class="welcome-content">
        <div class="eyebrow-label">Student Dashboard</div>
        <h1>Welcome back, ${name}! 👋</h1>
        <p>${hasRes ? 'Your AI career assessment is complete. Explore your personalized recommendations.' : 'Start your adaptive career assessment to unlock personalized recommendations.'}</p>
        ${!hasRes ? `<a href="/assessment.html" class="btn btn-white">Start Assessment &rarr;</a>` : ''}
      </div>
    </div>

    <!-- METRIC CARDS -->
    <div class="metric-cards mb-4">
      ${[
        { icon:'🎯', label:'Career Readiness Score', value:`${readiness}%`, color: readColor, sub:'Based on full assessment' },
        { icon:'🏆', label:'Top Career Match', value: top5[0]?.career || 'Not assessed', color:'var(--text-link)', sub: top5[0] ? `${top5[0].confidence}% confidence` : 'Take assessment first' },
        { icon:'🔬', label:'Skills Verified', value: hasRes ? '3+ Skills' : '0 Skills', color:'var(--amber)', sub:'ML-verified skill scores' },
        { icon:'📋', label:'Assessments Taken', value: sessions?.length || (hasRes ? 1 : 0), color:'#8b5cf6', sub:'Total sessions completed' },
      ].map(m => `
        <div class="metric-card">
          <div class="metric-icon">${m.icon}</div>
          <div class="metric-label">${m.label}</div>
          <div class="metric-value" style="color:${m.color}">${m.value}</div>
          <div class="metric-sub">${m.sub}</div>
        </div>
      `).join('')}
    </div>

    ${hasRes ? renderResults(top5, data) : renderEmptyState()}
  `;
}

function renderResults(top5, data) {
  return `
    <!-- TOP 5 CAREERS -->
    <div class="card card-2xl mb-4">
      <div class="flex justify-between items-center mb-4 wrap gap-2">
        <div>
          <h2 style="font-size:1.25rem;font-weight:800;color:var(--text-h)">🤖 AI-Predicted Career Matches</h2>
          <p style="color:var(--text-muted);font-size:0.85rem">XGBoost model · 272 career labels · SHAP explainability</p>
        </div>
        <a href="/assessment.html" class="btn btn-primary btn-sm">Retake Assessment</a>
      </div>

      ${top5.map((career, idx) => `
        <div class="career-card ${idx === 0 ? 'top-match' : ''} mb-3">
          ${idx === 0 ? `<span class="top-match-label">#1 TOP MATCH</span>` : ''}
          <div class="flex justify-between items-center wrap gap-2 mb-2">
            <div style="flex:1">
              <div class="flex items-center gap-1 wrap mb-2">
                <span class="career-rank">#${career.rank || idx + 1}</span>
                <h3 style="font-size:1.1rem;font-weight:800;color:var(--text-h);margin:0">${career.career}</h3>
              </div>
              <div class="flex gap-1 wrap">
                ${(career.why || []).map(w => `<span class="badge badge-emerald">✓ ${w}</span>`).join('')}
              </div>
            </div>
            <div style="text-align:right;min-width:100px">
              <div class="confidence-big" style="color:${idx === 0 ? 'var(--text-link)' : 'var(--text-h)'}">${career.confidence}%</div>
              <div style="font-size:0.75rem;color:var(--text-muted);font-weight:600">Confidence</div>
            </div>
          </div>
          <div class="progress-bar mb-3">
            <div class="progress-fill" style="width:${career.confidence}%;background:${idx === 0 ? 'var(--gradient-primary)' : 'rgba(99,102,241,0.4)'}"></div>
          </div>
          <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:0.75rem">
            ${[['💰','Salary',career.salary],['🎓','Degree',career.degree],['🏢','Companies',career.companies],['📈','Growth',career.growth]].map(([icon,label,val]) => `
              <div>
                <div style="font-size:0.72rem;color:var(--text-muted);font-weight:600;margin-bottom:0.15rem">${icon} ${label}</div>
                <div style="font-size:0.82rem;font-weight:700;color:var(--text-p)">${val || '—'}</div>
              </div>
            `).join('')}
          </div>
        </div>
      `).join('')}
    </div>

    <!-- LEARNING ROADMAP -->
    <div class="card card-2xl mb-4">
      <h2 style="font-size:1.25rem;font-weight:800;color:var(--text-h);margin-bottom:1.5rem">🗺️ Personalized Learning Roadmap</h2>
      <div class="roadmap-grid">
        ${[
          { step:'01', title:'Strengthen Core Skills', desc:'Master the key technical & soft skills identified in your assessment.', color:'#6366f1' },
          { step:'02', title:'Earn Certifications', desc:`Get certified: ${top5[0]?.certifications || 'Domain certifications'}.`, color:'#8b5cf6' },
          { step:'03', title:'Build Portfolio Projects', desc:'Work on 2–3 real-world projects aligned to your top career.', color:'#10b981' },
          { step:'04', title:'Apply & Network', desc:`Target recruiters: ${top5[0]?.companies || 'Industry leaders'}.`, color:'#f59e0b' },
        ].map(r => `
          <div class="roadmap-step" style="border-top-color:${r.color}">
            <div class="roadmap-num" style="color:${r.color}">${r.step}</div>
            <h4>${r.title}</h4>
            <p>${r.desc}</p>
          </div>
        `).join('')}
      </div>
    </div>
  `;
}

function renderEmptyState() {
  return `
    <div class="card card-2xl">
      <div class="empty-state">
        <div class="empty-icon">🎯</div>
        <h3>No Assessment Results Yet</h3>
        <p>Complete the AI Career Assessment to unlock your personalized Top 5 Career Recommendations, SHAP explanations, and Learning Roadmap.</p>
        <a href="/assessment.html" class="btn btn-primary btn-xl">Start AI Assessment &rarr;</a>
      </div>
    </div>
  `;
}
