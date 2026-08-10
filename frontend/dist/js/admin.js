/* admin.js — Admin Control Center */

let activeTab   = 'overview';
let analytics   = null;
let users       = [];
let questions   = [];
let totalQ      = 0;
let qPage       = 1;
let retraining  = false;
let certCount   = 1;

const newQ = {
  question_text: '', category: 'Logical Reasoning', difficulty: 'Medium',
  education_level: 'All', board: 'All', stream: 'All', degree: 'All',
  option_a: '', option_b: '', option_c: '', option_d: '',
  correct_answer: 'A', weight: 1.0, expected_time: 60, status: 'Active'
};

document.addEventListener('DOMContentLoaded', async () => {
  if (!Auth.requireAdmin()) return;
  renderNavbar('admin');
  renderShell();
  await fetchAnalytics();
  renderTab('overview');
});

/* ── SHELL ───────────────────────────────────────────────────── */
function renderShell() {
  const container = document.getElementById('admin-content');
  container.innerHTML = `
    <!-- Admin Header -->
    <div class="admin-header mb-4">
      <span>Admin Control Center</span>
      <h1>System Administration 👑</h1>
      <p>Manage users, question banks, ML model, and system analytics.</p>
    </div>

    <!-- Tabs -->
    <div class="tabs mb-4" id="admin-tabs">
      ${[['overview','📊 Overview'],['users','👥 Users'],['questions','❓ Questions'],['model','🤖 ML Model']].map(([t,l]) => `
        <button class="tab-btn ${t === 'overview' ? 'active' : ''}" data-tab="${t}">${l}</button>
      `).join('')}
    </div>

    <div id="alert-box" class="hidden mb-3"></div>

    <!-- Tab Content -->
    <div id="tab-content"></div>
  `;

  document.getElementById('admin-tabs').addEventListener('click', e => {
    const btn = e.target.closest('[data-tab]');
    if (!btn) return;
    document.querySelectorAll('#admin-tabs .tab-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    renderTab(btn.dataset.tab);
  });
}

/* ── FETCH ───────────────────────────────────────────────────── */
async function fetchAnalytics() {
  try {
    analytics = await API.get('/api/admin/analytics', true);
  } catch {
    analytics = { total_students:0, total_assessments:0, total_questions:0, top_careers:[], daily_trend:[] };
  }
}

async function fetchUsers() {
  try {
    const res = await API.get('/api/admin/users', true);
    users = res.users || [];
  } catch { users = []; }
}

async function fetchQuestions() {
  try {
    const res = await API.get(`/api/admin/questions?page=${qPage}&limit=20`, true);
    questions = res.questions || [];
    totalQ    = res.total || 0;
  } catch { questions = []; }
}

/* ── RENDER TABS ─────────────────────────────────────────────── */
async function renderTab(tab) {
  activeTab = tab;
  const content = document.getElementById('tab-content');
  content.innerHTML = UI.spinner();

  if (tab === 'overview') { renderOverview(content); }
  else if (tab === 'users') { await fetchUsers(); renderUsers(content); }
  else if (tab === 'questions') { await fetchQuestions(); renderQuestions(content); }
  else if (tab === 'model') { renderModel(content); }
}

/* ── OVERVIEW ────────────────────────────────────────────────── */
function renderOverview(container) {
  const a = analytics || {};
  container.innerHTML = `
    <div class="analytics-cards mb-4">
      ${[
        { icon:'👥', label:'Total Students', val: a.total_students ?? '—', color:'#6366f1' },
        { icon:'📋', label:'Total Assessments', val: a.total_assessments ?? '—', color:'#10b981' },
        { icon:'❓', label:'Active Questions', val: a.total_questions ?? '—', color:'#f59e0b' },
        { icon:'🎯', label:'Career Labels', val: 272, color:'#8b5cf6' },
      ].map(m => `
        <div class="analytics-card" style="border-top-color:${m.color}">
          <div class="icon">${m.icon}</div>
          <div class="a-label">${m.label}</div>
          <div class="a-value" style="color:${m.color}">${m.val}</div>
        </div>
      `).join('')}
    </div>

    ${a.top_careers?.length > 0 ? `
      <div class="card card-2xl">
        <h3 style="font-weight:800;color:var(--text-h);margin-bottom:1.25rem">Top 10 Predicted Careers</h3>
        ${a.top_careers.slice(0,10).map((c,ci) => `
          <div style="display:flex;justify-content:space-between;align-items:center;padding:0.65rem 0.85rem;background:var(--bg-card-subtle);border-radius:var(--radius-lg);margin-bottom:0.5rem">
            <span style="font-weight:700;color:var(--text-p);font-size:0.9rem">#${ci+1} ${c.top1_career}</span>
            <span style="font-weight:900;color:var(--text-link)">${c.count} assessments</span>
          </div>
        `).join('')}
      </div>
    ` : '<div class="card"><div class="empty-state"><div class="empty-icon">📊</div><h3>No Assessment Data Yet</h3><p>Analytics will appear once students complete assessments.</p></div></div>'}
  `;
}

/* ── USERS ───────────────────────────────────────────────────── */
function renderUsers(container) {
  container.innerHTML = `
    <div class="card card-2xl">
      <h3 style="font-weight:800;color:var(--text-h);margin-bottom:1.5rem">Student Accounts (${users.length})</h3>
      ${users.length === 0 ? '<div class="empty-state"><div class="empty-icon">👥</div><h3>No Users Yet</h3></div>' : `
        <div class="table-wrap">
          <table>
            <thead><tr>
              ${['ID','Name','Email','Role','Assessments','Joined','Actions'].map(h => `<th>${h}</th>`).join('')}
            </tr></thead>
            <tbody>
              ${users.map(u => `
                <tr>
                  <td style="color:var(--text-muted)">#${u.id}</td>
                  <td style="font-weight:700;color:var(--text-h)">${u.full_name}</td>
                  <td style="color:var(--text-muted)">${u.email}</td>
                  <td><span class="badge ${u.role === 'admin' ? 'badge-red' : 'badge-emerald'}">${u.role}</span></td>
                  <td style="font-weight:700">${u.assessments || 0}</td>
                  <td style="color:var(--text-muted)">${u.created_at ? new Date(u.created_at).toLocaleDateString() : '—'}</td>
                  <td>
                    ${u.role !== 'admin' ? `<button class="btn btn-danger btn-sm" onclick="deleteUser(${u.id})">Delete</button>` : '<span style="color:var(--text-muted)">—</span>'}
                  </td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      `}
    </div>
  `;
}

async function deleteUser(uid) {
  if (!confirm('Delete this user? This cannot be undone.')) return;
  try {
    await API.del(`/api/admin/users/${uid}`, true);
    UI.showAlert('alert-box', 'success', 'User deleted successfully.');
    await fetchUsers();
    renderUsers(document.getElementById('tab-content'));
  } catch {
    UI.showAlert('alert-box', 'error', 'Error deleting user.');
  }
}

/* ── QUESTIONS ───────────────────────────────────────────────── */
function renderQuestions(container) {
  container.innerHTML = `
    <!-- ADD QUESTION FORM -->
    <div class="card card-2xl mb-4">
      <h3 style="font-weight:800;color:var(--text-h);margin-bottom:1.25rem">+ Add New Question</h3>
      <div class="form-grid mb-3">
        <div class="form-group" style="grid-column:1/-1">
          <label>Question Text *</label>
          <textarea id="nq-text" rows="3" style="width:100%;resize:vertical;background:var(--input-bg);border:1px solid var(--input-border);border-radius:var(--radius-md);color:var(--text-h);padding:0.75rem;font-family:inherit;font-size:0.95rem"></textarea>
        </div>
        ${[
          ['Category','nq-cat',['Logical Reasoning','Numerical Reasoning','Science Aptitude','Algorithms','Database Systems','Machine Learning','Psychometric','Career Interest','Skill Verification','Mathematics','Financial Accounting']],
          ['Difficulty','nq-diff',['Easy','Medium','Hard']],
          ['Education Level','nq-level',['All','Class 7','Class 8','Class 9','Class 10','Higher Secondary','Undergraduate','Postgraduate']],
          ['Board','nq-board',['All','CBSE','Kerala State Board','ICSE']],
          ['Stream','nq-stream',['All','Science (PCM)','Science (PCB)','Commerce','Humanities/Arts']],
          ['Correct Answer','nq-correct',['A','B','C','D']],
        ].map(([label,id,opts]) => `
          <div class="form-group">
            <label>${label}</label>
            <select id="${id}">${opts.map(o=>`<option value="${o}">${o}</option>`).join('')}</select>
          </div>
        `).join('')}
        ${['A','B','C','D'].map(l => `
          <div class="form-group">
            <label>Option ${l} *</label>
            <input type="text" id="nq-opt${l}" placeholder="Option ${l}" />
          </div>
        `).join('')}
      </div>
      <div id="add-q-alert" class="hidden mb-2"></div>
      <button class="btn btn-primary" id="add-q-btn" onclick="addQuestion()">+ Add Question to Bank</button>
    </div>

    <!-- QUESTION LIST -->
    <div class="card card-2xl">
      <div class="flex justify-between items-center mb-4 wrap gap-2">
        <h3 style="font-weight:800;color:var(--text-h)">Question Bank (${totalQ} questions)</h3>
        <div class="flex gap-1">
          <button class="btn btn-secondary btn-sm" onclick="changeQPage(-1)" ${qPage === 1 ? 'disabled' : ''}>Prev</button>
          <span style="padding:0.45rem 0.85rem;color:var(--text-muted);font-size:0.82rem">Page ${qPage}</span>
          <button class="btn btn-secondary btn-sm" onclick="changeQPage(1)" ${questions.length < 20 ? 'disabled' : ''}>Next</button>
        </div>
      </div>
      <div id="q-list">
        ${questions.map(q => `
          <div style="padding:1rem;background:var(--bg-card-subtle);border-radius:var(--radius-lg);border:1px solid var(--border);display:flex;justify-content:space-between;align-items:flex-start;gap:1rem;margin-bottom:0.75rem">
            <div style="flex:1">
              <p style="font-weight:700;color:var(--text-h);font-size:0.88rem;margin:0 0 0.35rem">${(q.question_text||'').substring(0,120)}${q.question_text?.length > 120 ? '...' : ''}</p>
              <div class="flex gap-1 wrap">
                ${[q.category,q.difficulty,q.education_level].filter(Boolean).map(t=>`<span class="badge badge-primary">${t}</span>`).join('')}
              </div>
            </div>
            <button class="btn btn-danger btn-sm" style="flex-shrink:0" onclick="deleteQuestion(${q.id})">Delete</button>
          </div>
        `).join('')}
        ${questions.length === 0 ? '<div class="empty-state"><div class="empty-icon">❓</div><h3>No Questions Found</h3></div>' : ''}
      </div>
    </div>
  `;
}

async function addQuestion() {
  const text = document.getElementById('nq-text')?.value.trim();
  if (!text) { UI.showAlert('add-q-alert','error','Question text is required.'); return; }

  const payload = {
    question_text: text,
    category:        document.getElementById('nq-cat')?.value,
    difficulty:      document.getElementById('nq-diff')?.value,
    education_level: document.getElementById('nq-level')?.value,
    board:           document.getElementById('nq-board')?.value,
    stream:          document.getElementById('nq-stream')?.value,
    option_a:        document.getElementById('nq-optA')?.value,
    option_b:        document.getElementById('nq-optB')?.value,
    option_c:        document.getElementById('nq-optC')?.value,
    option_d:        document.getElementById('nq-optD')?.value,
    correct_answer:  document.getElementById('nq-correct')?.value,
    weight: 1.0, expected_time: 60, status: 'Active',
  };

  UI.setLoading('add-q-btn', true, 'Adding...', '+ Add Question to Bank');
  try {
    await API.post('/api/admin/questions', payload, true);
    UI.showAlert('alert-box', 'success', 'Question added to bank!');
    UI.showAlert('add-q-alert', 'success', 'Question added successfully!');
    await fetchQuestions();
    renderQuestions(document.getElementById('tab-content'));
  } catch {
    UI.showAlert('add-q-alert', 'error', 'Error adding question.');
  } finally {
    UI.setLoading('add-q-btn', false, '', '+ Add Question to Bank');
  }
}

async function deleteQuestion(qid) {
  if (!confirm('Delete this question?')) return;
  try {
    await API.del(`/api/admin/questions/${qid}`, true);
    UI.showAlert('alert-box', 'success', 'Question deleted.');
    await fetchQuestions();
    renderQuestions(document.getElementById('tab-content'));
  } catch {
    UI.showAlert('alert-box', 'error', 'Error deleting question.');
  }
}

async function changeQPage(delta) {
  qPage = Math.max(1, qPage + delta);
  await fetchQuestions();
  renderQuestions(document.getElementById('tab-content'));
}

/* ── ML MODEL ────────────────────────────────────────────────── */
function renderModel(container) {
  container.innerHTML = `
    <div class="flex gap-3" style="flex-direction:column">
      <div class="card card-2xl">
        <h3 style="font-weight:800;color:var(--text-h);margin-bottom:1.25rem">🤖 ML Model Status</h3>
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:1rem;margin-bottom:1.5rem">
          ${[
            { label:'Model Type', val:'XGBoost Classifier' },
            { label:'Training Samples', val:'40,000 rows' },
            { label:'Career Labels', val:'30 unique careers' },
            { label:'Feature Columns', val:'61 features' },
            { label:'Dataset', val:'career_dataset.csv' },
            { label:'Training Accuracy', val:'98.38%' },
          ].map(item => `
            <div style="padding:1rem;background:var(--bg-card-subtle);border-radius:var(--radius-lg);border:1px solid var(--border)">
              <div style="font-size:0.72rem;color:var(--text-muted);font-weight:700;text-transform:uppercase;margin-bottom:0.25rem">${item.label}</div>
              <div style="font-weight:800;color:var(--text-h)">${item.val}</div>
            </div>
          `).join('')}
        </div>
        <div id="retrain-alert" class="hidden mb-3"></div>
        <button class="btn btn-primary" id="retrain-btn" onclick="handleRetrain()">🔄 Retrain ML Model</button>
        <p style="color:var(--text-muted);font-size:0.82rem;margin-top:0.75rem">
          Retraining runs <code style="background:var(--bg-card-subtle);padding:0.15rem 0.4rem;border-radius:4px">train_model.py</code> in background. Monitor server logs.
        </p>
      </div>

      <div class="card card-2xl">
        <h3 style="font-weight:800;color:var(--text-h);margin-bottom:1rem">📦 Model Artifacts</h3>
        ${['career_model.pkl','label_encoder.pkl','ordinal_encoder.pkl','feature_columns.pkl','scaler.pkl','shap_explainer.pkl'].map(f => `
          <div class="green-file mb-2">✓ ${f}</div>
        `).join('')}
      </div>
    </div>
  `;
}

async function handleRetrain() {
  if (retraining) return;
  retraining = true;
  UI.setLoading('retrain-btn', true, '⏳ Retraining Started...', '🔄 Retrain ML Model');
  try {
    await API.post('/api/admin/retrain', {}, true);
    UI.showAlert('retrain-alert', 'success', 'Model retraining started! Check server logs for progress.');
    UI.showAlert('alert-box', 'success', 'Model retraining triggered successfully.');
  } catch {
    UI.showAlert('retrain-alert', 'error', 'Retraining failed. Check server.');
  } finally {
    retraining = false;
    UI.setLoading('retrain-btn', false, '', '🔄 Retrain ML Model');
  }
}
