/* history.js — Assessment History Page */

document.addEventListener('DOMContentLoaded', async () => {
  if (!Auth.requireAuth()) return;
  renderNavbar('history');

  const user = Auth.getUser();
  const container = document.getElementById('history-content');

  let history = [];
  let error = '';

  try {
    const res = await API.get('/api/history', true);
    if (res.status === 'success') {
      history = res.history || [];
    } else {
      throw new Error(res.error || 'Failed');
    }
  } catch (e) {
    error = 'Failed to load assessment history. Please check your connection.';
    console.error(e);
  }

  render(history, error, user, container);
});

function render(history, error, user, container) {
  const maxScore  = history.length ? Math.max(...history.map(h => h.readiness_score || Math.round(h.top1_confidence || 0))) : 0;
  const latestCar = history.length ? (history[0].top1_career || history[0].recommended_career || 'None') : 'None';
  const name      = user?.full_name || 'Student';

  container.innerHTML = `
    <!-- HEADER -->
    <div class="welcome-banner mb-4">
      <div class="welcome-banner-orb"></div>
      <div class="welcome-content">
        <div class="eyebrow-label">Assessment Archive</div>
        <h1>Career Assessment History</h1>
        <p>Past AI-recommended career tracks and verified evaluation results for <strong>${name}</strong></p>
        <a href="/assessment.html" class="btn btn-white mt-2">+ Take New Assessment</a>
      </div>
    </div>

    ${history.length > 0 ? `
      <!-- STATS -->
      <div class="metric-cards mb-4">
        <div class="metric-card">
          <div class="metric-icon">📋</div>
          <div class="metric-label">Total Assessments</div>
          <div class="metric-value" style="color:var(--primary)">${history.length}</div>
        </div>
        <div class="metric-card">
          <div class="metric-icon">🏆</div>
          <div class="metric-label">Latest Recommended Career</div>
          <div class="metric-value" style="font-size:1rem;color:var(--text-link)">${latestCar}</div>
        </div>
        <div class="metric-card">
          <div class="metric-icon">📈</div>
          <div class="metric-label">Top Verified Score</div>
          <div class="metric-value" style="color:var(--emerald)">${maxScore}%</div>
        </div>
      </div>
    ` : ''}

    ${error ? `<div class="alert alert-error mb-4">${error}</div>` : ''}

    ${history.length === 0 && !error ? renderEmpty() : `
      <div class="history-grid">${history.map(renderCard).join('')}</div>
    `}
  `;
}

function renderCard(item) {
  const dateStr = item.predicted_at || item.assessment_date || item.created_at;
  const dateObj = dateStr ? new Date(dateStr) : null;
  const formatted = dateObj && !isNaN(dateObj)
    ? dateObj.toLocaleDateString('en-US', { month:'short', day:'numeric', year:'numeric' }) + ' at ' + dateObj.toLocaleTimeString([], { hour:'2-digit', minute:'2-digit' })
    : 'Recent';

  const career   = item.top1_career || item.recommended_career || 'Career Analysis';
  const score    = item.readiness_score || Math.round(item.top1_confidence || 0);
  const isPassed = score >= 70;
  const scoreColor = isPassed ? 'var(--emerald)' : 'var(--amber)';
  const trait    = item.riasec_trait || '';
  const level    = item.education_level || 'General';

  return `
    <div class="history-card">
      <div class="history-card-header">
        <span style="font-size:0.82rem;color:var(--text-muted);font-weight:600">📅 ${formatted}</span>
        <span class="badge badge-primary">${level}</span>
      </div>
      <div class="history-card-body">
        <div style="font-size:0.75rem;color:var(--text-muted);font-weight:700;text-transform:uppercase;letter-spacing:0.04em;margin-bottom:0.35rem">AI Recommended Direction</div>
        <h3 style="font-size:1.1rem;font-weight:800;color:var(--text-h);margin-bottom:1rem">${career}</h3>
        <div class="flex gap-2 mb-2 wrap">
          ${trait ? `<div><span style="font-size:0.72rem;color:var(--text-muted)">RIASEC Trait</span><br><span class="badge badge-primary" style="margin-top:0.2rem">${trait}</span></div>` : ''}
          <div><span style="font-size:0.72rem;color:var(--text-muted)">Verified Score</span><br>
            <strong style="font-size:1.1rem;font-weight:900;color:${scoreColor}">${score}%</strong>
          </div>
        </div>
        <div class="progress-bar mt-2">
          <div class="progress-fill ${isPassed ? 'emerald' : 'amber'}" style="width:${Math.min(100,Math.max(5,score))}%"></div>
        </div>
      </div>
      <div class="history-card-footer">
        <button class="btn btn-primary w-full" onclick="viewDashboard('${career}','${trait}',${score})">
          View Full Dashboard →
        </button>
      </div>
    </div>
  `;
}

function renderEmpty() {
  return `
    <div class="card">
      <div class="empty-state">
        <div class="empty-icon">📊</div>
        <h3>No Past Assessments Found</h3>
        <p>You haven't completed any AI Career Assessments yet. Take your first 10-minute assessment to unlock personalized recommendations!</p>
        <a href="/assessment.html" class="btn btn-primary btn-lg mt-3">Start Your Assessment →</a>
      </div>
    </div>
  `;
}

function viewDashboard(career, trait, score) {
  localStorage.setItem('finalRecommendedCareer', career);
  localStorage.setItem('recommendedCareer', career);
  localStorage.setItem('riasecTrait', trait);
  localStorage.setItem('verifiedScore', score);
  window.location.href = '/dashboard.html';
}
