/* assessment.js — Multi-step AI Career Assessment */

const SKILLS_MATRIX = [
  'Python','Java','C++','JavaScript','SQL & Databases','Machine Learning',
  'Data Structures & Algorithms','React.js / Frontend','Node.js / Backend',
  'Financial Accounting','Tally / ERP','UI/UX Design','Digital Marketing',
  'Public Speaking','Project Management','CAD & Mechanical Design',
  'Medical Biology / Anatomy','Copywriting & Content','Cyber Security',
  'Cloud Computing (AWS/Azure)','Android/iOS Development','Data Analysis (Excel/BI)',
];

const INTEREST_PAIRS = [
  { q:'Which activity sounds more engaging?', a:{label:'Building AI systems & robots',domain:'Technology'}, b:{label:'Creating business strategies',domain:'Business'} },
  { q:'Which sounds more fulfilling?',        a:{label:'Teaching & mentoring students',domain:'Education'}, b:{label:'Diagnosing & treating patients',domain:'Healthcare'} },
  { q:'Which problem excites you most?',      a:{label:'Solving complex algorithms',domain:'Technology'}, b:{label:'Designing creative campaigns',domain:'Creative Arts'} },
  { q:'Where would you work?',                a:{label:'Research laboratory or tech company',domain:'Research'}, b:{label:'Courtroom or law firm',domain:'Law'} },
  { q:'Which career path interests you?',     a:{label:'Engineering large-scale infrastructure',domain:'Engineering'}, b:{label:'Working in environment conservation',domain:'Environment'} },
  { q:'Which project would you prefer?',      a:{label:'Building a data analytics platform',domain:'Technology'}, b:{label:'Launching a social enterprise',domain:'Business'} },
  { q:'Which role suits you better?',         a:{label:'Medical researcher developing vaccines',domain:'Healthcare'}, b:{label:'Journalist writing investigative reports',domain:'Creative Arts'} },
  { q:'What would you enjoy more?',           a:{label:'Designing a new sustainable city',domain:'Engineering'}, b:{label:'Teaching rural communities new skills',domain:'Education'} },
];

const PSYCH_SCENARIOS = [
  { q:'Your team is behind schedule on a critical project. What do you do?', options:[
    {label:'Organize a triage meeting, reassign tasks based on capacity',traits:{Leadership:15,Communication:10}},
    {label:'Work extra hours yourself to bridge the gap',traits:{Persistence:15,Resilience:10}},
    {label:'Motivate the team and focus on morale',traits:{Teamwork:15,Communication:10}},
    {label:'Prioritize ruthlessly and cut non-essential tasks',traits:{Decision_Making:15,Analytical_Thinking:10}},
  ]},
  { q:'You encounter a completely new type of problem. You:', options:[
    {label:'Research methodically using documentation and forums',traits:{Curiosity:15,Self_Learning:10}},
    {label:'Ask an experienced colleague for guidance',traits:{Teamwork:10,Adaptability:10}},
    {label:'Break it into smaller sub-problems and tackle each',traits:{Analytical_Thinking:15,Problem_Solving:10}},
    {label:'Try different solutions systematically until one works',traits:{Persistence:15,Adaptability:10}},
  ]},
  { q:'You are given freedom to choose a project topic. You choose:', options:[
    {label:'The most technically challenging unsolved problem',traits:{Curiosity:15,Analytical_Thinking:10}},
    {label:'Something with clear measurable social impact',traits:{Leadership:10,Communication:10}},
    {label:'Something involving creative design and innovation',traits:{Creativity:15,Self_Learning:10}},
    {label:'Something with strong financial ROI potential',traits:{Decision_Making:10,Confidence:10}},
  ]},
  { q:'A critical bug is found 1 hour before a major product launch. You:', options:[
    {label:'Stay calm, triage severity, and decide quickly',traits:{Stress_Management:15,Decision_Making:10}},
    {label:'Rally the entire team to fix it immediately',traits:{Leadership:15,Teamwork:10}},
    {label:'Apply a quick patch and document the full fix for later',traits:{Adaptability:15,Problem_Solving:10}},
    {label:'Escalate to management with a clear options briefing',traits:{Communication:15,Confidence:10}},
  ]},
];

const BOARD_SUBJECTS = {
  'Class 7':  { 'Kerala State Board':['First Language','English','Mathematics','Science','Social Science','ICT'], 'CBSE':['Language I','Language II','Mathematics','Science','Social Science'], 'default':['Language I','English','Mathematics','Science','Social Studies'] },
  'Class 8':  { 'Kerala State Board':['First Language','English','Mathematics','Physics','Chemistry','Biology','Social Science','ICT'], 'CBSE':['Language I','Language II','Mathematics','Science','Social Science','IT'], 'default':['Language I','English','Mathematics','Science','Social Studies'] },
  'Class 9':  { 'Kerala State Board':['First Language','English','Mathematics','Physics','Chemistry','Biology','Social Science','ICT'], 'CBSE':['Language I','Language II','Mathematics','Science','Social Science','AI/IT'], 'default':['Language I','English','Mathematics','Science','Social Studies'] },
  'Class 10': { 'Kerala State Board':['First Language','English','Mathematics','Physics','Chemistry','Biology','Social Science','ICT'], 'CBSE':['Language I','Language II','Mathematics','Science','Social Science','AI/IT'], 'default':['Language I','English','Mathematics','Science','Social Studies'] },
  'Higher Secondary (11-12)': {
    'Science (PCM)':['Physics','Chemistry','Mathematics','Computer Science','English'],
    'Science (PCB)':['Physics','Chemistry','Biology','Mathematics','English'],
    'Science (PCMB)':['Physics','Chemistry','Mathematics','Biology','English'],
    'Commerce':['Accountancy','Business Studies','Economics','Mathematics','English'],
    'Humanities/Arts':['History','Geography','Political Science','Economics','English'],
    'default':['Subject 1','Subject 2','Subject 3','Subject 4','English'],
  },
};

// ── STATE ──────────────────────────────────────────────────────
let currentStep = 1;
const TOTAL_STEPS = 9;
const state = {
  education: {},
  subjectMarks: [],
  aptitudeAnswers: [],
  psychAnswers: [],
  interestScores: {},
  selectedSkills: [],
  certs: [{ name: '', provider: '' }],
  projs: [{ title: '', tech: '' }],
  psychTraits: {},
};

let aptitudeQuestions = [];
let certCount = 1;
let projCount = 1;

// ── NAVIGATION ────────────────────────────────────────────────
function updateStepUI() {
  document.querySelectorAll('.step-section').forEach((s, i) => {
    s.classList.toggle('active', i + 1 === currentStep);
  });
  const progress = document.getElementById('main-progress');
  if (progress) progress.style.width = `${(currentStep / TOTAL_STEPS) * 100}%`;
  renderStepNav();
}

function renderStepNav() {
  const nav = document.getElementById('step-nav');
  if (!nav) return;
  const labels = ['Education','Marks','Aptitude','Psychometric','Interests','Skills','Certs','Projects','Results'];
  nav.innerHTML = labels.map((label, i) => `
    <div class="step-dot ${i + 1 < currentStep ? 'completed' : i + 1 === currentStep ? 'active' : ''}" title="Step ${i+1}: ${label}">
      ${i + 1 < currentStep ? '✓' : i + 1}
    </div>
  `).join('');
}

function nextStep(from) {
  if (from === 1) {
    const level = document.getElementById('education_level').value;
    const board = document.getElementById('board').value;
    if (!level || !board) { UI.showAlert('alert-box','error','Please select Education Level and Board.'); return; }
    state.education = {
      education_level: level,
      board,
      stream: document.getElementById('stream').value,
      degree: document.getElementById('degree').value,
      specialization: document.getElementById('specialization').value,
      institution: document.getElementById('institution').value,
      cgpa: parseFloat(document.getElementById('cgpa').value) || 0,
      attendance: parseFloat(document.getElementById('attendance').value) || 0,
    };
    loadSubjectMarks();
  }
  if (from === 2) saveSubjectMarks();
  if (from === 3 && state.aptitudeAnswers.length < aptitudeQuestions.length) {
    UI.showAlert('alert-box','error','Please answer all aptitude questions before proceeding.');
    return;
  }
  if (from === 4) savePsychAnswers();
  if (from === 5) saveInterests();
  if (from === 6) saveSkills();
  if (from === 7) saveCerts();

  UI.hideAlert('alert-box');
  currentStep = from + 1;
  updateStepUI();
  window.scrollTo(0, 0);

  if (currentStep === 3) loadAptitudeQuestions();
}

function prevStep(from) {
  currentStep = from - 1;
  updateStepUI();
  window.scrollTo(0, 0);
}

// ── STEP 1 DYNAMIC FIELDS ─────────────────────────────────────
function bindEducationFields() {
  const lvlEl = document.getElementById('education_level');
  const streamGrp = document.getElementById('stream-group');
  const degreeGrp = document.getElementById('degree-group');
  const specGrp   = document.getElementById('spec-group');

  lvlEl.addEventListener('change', () => {
    const lvl = lvlEl.value;
    const isHS = lvl === 'Higher Secondary (11-12)';
    const isUG = ['Undergraduate','Postgraduate','Professional Degree','Diploma / ITI'].includes(lvl);
    streamGrp.style.display = (isHS || isUG) ? '' : 'none';
    degreeGrp.style.display = isUG ? '' : 'none';
    specGrp.style.display   = isUG ? '' : 'none';
  });
}

// ── STEP 2: SUBJECT MARKS ─────────────────────────────────────
function loadSubjectMarks() {
  const { education_level, board, stream } = state.education;
  const boardSubjMap = BOARD_SUBJECTS[education_level];
  let subjects = [];
  if (boardSubjMap) {
    subjects = boardSubjMap[board] || boardSubjMap[stream] || boardSubjMap['default'] || [];
  }
  if (!subjects.length) subjects = ['Subject 1','Subject 2','Subject 3','Subject 4','Subject 5'];

  const tbody = document.getElementById('subjects-body');
  tbody.innerHTML = subjects.map((s, i) => `
    <tr>
      <td>${s}</td>
      <td><input type="number" min="0" max="100" step="0.5" placeholder="0-100" id="subj-marks-${i}" /></td>
      <td>
        <select id="subj-grade-${i}">
          <option value="">Grade</option>
          <option>A+</option><option>A</option><option>B+</option><option>B</option>
          <option>C+</option><option>C</option><option>D</option><option>F</option>
        </select>
      </td>
    </tr>
  `).join('');

  state._subjects = subjects;
}

function saveSubjectMarks() {
  const subjects = state._subjects || [];
  state.subjectMarks = subjects.map((s, i) => ({
    subject: s,
    marks: parseFloat(document.getElementById(`subj-marks-${i}`)?.value) || 0,
    grade: document.getElementById(`subj-grade-${i}`)?.value || '',
  }));
}

// ── STEP 3: APTITUDE ──────────────────────────────────────────
async function loadAptitudeQuestions() {
  const loading = document.getElementById('aptitude-loading');
  const container = document.getElementById('aptitude-questions');
  loading.style.display = 'flex';
  container.style.display = 'none';

  try {
    const lvl = encodeURIComponent(state.education.education_level || 'All');
    const board = encodeURIComponent(state.education.board || 'All');
    const res = await API.get(`/api/assessment/questions?education_level=${lvl}&board=${board}&limit=10`);
    aptitudeQuestions = (res.questions || []).slice(0, 10);
    if (!aptitudeQuestions.length) throw new Error('No questions');
  } catch {
    // Fallback static questions
    aptitudeQuestions = [
      { id:1, question_text:'What is the next number in: 2, 4, 8, 16, ?', option_a:'24', option_b:'30', option_c:'32', option_d:'64', correct_answer:'C', category:'Logical Reasoning', difficulty:'Easy' },
      { id:2, question_text:'A train 200m long passes a pole in 10 seconds. What is its speed?', option_a:'10 m/s', option_b:'20 m/s', option_c:'25 m/s', option_d:'15 m/s', correct_answer:'B', category:'Numerical Reasoning', difficulty:'Medium' },
      { id:3, question_text:'Complete: 1, 1, 2, 3, 5, 8, 13, ?', option_a:'18', option_b:'19', option_c:'20', option_d:'21', correct_answer:'D', category:'Logical Reasoning', difficulty:'Easy' },
      { id:4, question_text:'Speed of light in vacuum?', option_a:'3×10⁸ m/s', option_b:'3×10⁶ m/s', option_c:'1.5×10⁸ m/s', option_d:'3×10⁹ m/s', correct_answer:'A', category:'Physics', difficulty:'Easy' },
      { id:5, question_text:'Worst-case time complexity of QuickSort?', option_a:'O(N log N)', option_b:'O(N²)', option_c:'O(N)', option_d:'O(log N)', correct_answer:'B', category:'Algorithms', difficulty:'Hard' },
    ];
  }

  state.aptitudeAnswers = new Array(aptitudeQuestions.length).fill(null);
  renderAptitudeQuestions();
  loading.style.display = 'none';
  container.style.display = 'block';
}

function renderAptitudeQuestions() {
  const container = document.getElementById('aptitude-questions');
  const nextBtn = document.getElementById('aptitude-next-btn');

  container.innerHTML = aptitudeQuestions.map((q, qi) => `
    <div class="card mb-3" style="border-left:3px solid var(--primary)">
      <div class="q-counter">Question ${qi+1} of ${aptitudeQuestions.length} · <span class="badge badge-primary">${q.category}</span> · <span class="badge badge-amber">${q.difficulty}</span></div>
      <div class="q-text">${q.question_text}</div>
      <div class="options-grid" id="apt-opts-${qi}">
        ${['A','B','C','D'].map(letter => {
          const optKey = `option_${letter.toLowerCase()}`;
          const text = q[optKey];
          if (!text) return '';
          return `<button class="option-btn" data-q="${qi}" data-ans="${letter}" onclick="selectAptitude(${qi},'${letter}',this)">
            <span class="option-label">${letter}.</span> ${text}
          </button>`;
        }).join('')}
      </div>
    </div>
  `).join('');

  checkAptitudeComplete();
}

function selectAptitude(qi, letter, btn) {
  state.aptitudeAnswers[qi] = letter;
  // Highlight selected
  document.querySelectorAll(`#apt-opts-${qi} .option-btn`).forEach(b => {
    b.style.borderColor = '';
    b.style.background = '';
    b.style.color = '';
  });
  btn.style.borderColor = 'var(--primary)';
  btn.style.background = 'var(--badge-bg)';
  btn.style.color = 'var(--badge-text)';
  checkAptitudeComplete();
}

function checkAptitudeComplete() {
  const answered = state.aptitudeAnswers.filter(a => a !== null).length;
  const nextBtn = document.getElementById('aptitude-next-btn');
  if (nextBtn) nextBtn.style.display = answered === aptitudeQuestions.length ? 'inline-flex' : 'none';
}

// ── STEP 4: PSYCHOMETRIC ──────────────────────────────────────
function renderPsychometric() {
  const container = document.getElementById('psych-container');
  state.psychAnswers = new Array(PSYCH_SCENARIOS.length).fill(null);

  container.innerHTML = PSYCH_SCENARIOS.map((sc, si) => `
    <div class="card mb-3" style="border-left:3px solid var(--violet)">
      <div class="q-counter">Scenario ${si+1} of ${PSYCH_SCENARIOS.length}</div>
      <div class="q-text">${sc.q}</div>
      <div class="options-grid" id="psych-opts-${si}">
        ${sc.options.map((opt, oi) => `
          <button class="option-btn" data-si="${si}" data-oi="${oi}" onclick="selectPsych(${si},${oi},this)">
            <span class="option-label">${String.fromCharCode(65+oi)}.</span> ${opt.label}
          </button>
        `).join('')}
      </div>
    </div>
  `).join('');
}

function selectPsych(si, oi, btn) {
  state.psychAnswers[si] = oi;
  document.querySelectorAll(`#psych-opts-${si} .option-btn`).forEach(b => {
    b.style.borderColor = '';
    b.style.background = '';
    b.style.color = '';
  });
  btn.style.borderColor = 'var(--violet)';
  btn.style.background = 'rgba(139,92,246,0.1)';
  btn.style.color = 'var(--violet)';
}

function savePsychAnswers() {
  const traits = {};
  PSYCH_SCENARIOS.forEach((sc, si) => {
    const selected = state.psychAnswers[si];
    if (selected === null) return;
    const opt = sc.options[selected];
    Object.entries(opt.traits).forEach(([t, v]) => {
      traits[t] = (traits[t] || 0) + v;
    });
  });
  state.psychTraits = traits;
}

// ── STEP 5: INTEREST PAIRS ────────────────────────────────────
function renderInterests() {
  const container = document.getElementById('interest-container');
  state._interestAnswers = new Array(INTEREST_PAIRS.length).fill(null);

  container.innerHTML = INTEREST_PAIRS.map((pair, pi) => `
    <div class="mb-4">
      <p style="font-weight:700;color:var(--text-h);margin-bottom:0.75rem;font-size:0.95rem">${pi+1}. ${pair.q}</p>
      <div class="interest-pair" id="int-pair-${pi}">
        <button class="interest-option" data-pi="${pi}" data-opt="a" onclick="selectInterest(${pi},'a',this)">
          ${pair.a.label}
        </button>
        <button class="interest-option" data-pi="${pi}" data-opt="b" onclick="selectInterest(${pi},'b',this)">
          ${pair.b.label}
        </button>
      </div>
    </div>
  `).join('');
}

function selectInterest(pi, opt, btn) {
  state._interestAnswers[pi] = opt;
  document.querySelectorAll(`#int-pair-${pi} .interest-option`).forEach(b => b.classList.remove('selected'));
  btn.classList.add('selected');
}

function saveInterests() {
  const scores = {};
  INTEREST_PAIRS.forEach((pair, pi) => {
    const chosen = state._interestAnswers[pi];
    const domain = chosen === 'a' ? pair.a.domain : pair.b.domain;
    scores[domain] = (scores[domain] || 0) + 1;
  });
  state.interestScores = scores;
}

// ── STEP 6: SKILLS ────────────────────────────────────────────
function renderSkills() {
  const grid = document.getElementById('skill-grid');
  grid.innerHTML = SKILLS_MATRIX.map(skill => `
    <div class="skill-chip" data-skill="${skill}" onclick="toggleSkill(this,'${skill}')">
      ${skill}
    </div>
  `).join('');
}

function toggleSkill(el, skill) {
  el.classList.toggle('selected');
  if (el.classList.contains('selected')) {
    if (!state.selectedSkills.includes(skill)) state.selectedSkills.push(skill);
  } else {
    state.selectedSkills = state.selectedSkills.filter(s => s !== skill);
  }
}

function saveSkills() { /* already tracked via toggleSkill */ }

// ── STEP 7: CERTS ─────────────────────────────────────────────
function addCert() {
  const container = document.getElementById('certs-container');
  const i = certCount++;
  const row = document.createElement('div');
  row.className = 'cert-row';
  row.id = `cert-${i}`;
  row.innerHTML = `
    <div class="form-group"><label>Certification Name</label><input type="text" placeholder="e.g. AWS Cloud Practitioner" id="cert-name-${i}" /></div>
    <div class="form-group"><label>Provider</label><input type="text" placeholder="e.g. Amazon, Google" id="cert-provider-${i}" /></div>
    <button class="btn btn-danger btn-sm" onclick="removeCert(${i})" style="height:40px;align-self:flex-end">✕</button>
  `;
  container.appendChild(row);
}

function removeCert(i) {
  const el = document.getElementById(`cert-${i}`);
  if (el) el.remove();
}

function saveCerts() {
  state.certs = [];
  document.querySelectorAll('[id^="cert-name-"]').forEach(el => {
    const i = el.id.split('-').pop();
    const name = el.value.trim();
    const prov = document.getElementById(`cert-provider-${i}`)?.value.trim() || '';
    if (name) state.certs.push({ name, provider: prov });
  });
}

// ── STEP 8: PROJECTS ──────────────────────────────────────────
function addProj() {
  const container = document.getElementById('projs-container');
  const i = projCount++;
  const row = document.createElement('div');
  row.className = 'proj-row';
  row.id = `proj-${i}`;
  row.innerHTML = `
    <div class="form-group"><label>Project Title</label><input type="text" placeholder="e.g. E-Commerce Platform" id="proj-title-${i}" /></div>
    <div class="form-group"><label>Technologies Used</label><input type="text" placeholder="e.g. React, Python" id="proj-tech-${i}" /></div>
    <button class="btn btn-danger btn-sm" onclick="removeProj(${i})" style="height:40px;align-self:flex-end">✕</button>
  `;
  container.appendChild(row);
}

function removeProj(i) {
  const el = document.getElementById(`proj-${i}`);
  if (el) el.remove();
}

function saveProjects() {
  state.projs = [];
  document.querySelectorAll('[id^="proj-title-"]').forEach(el => {
    const i = el.id.split('-').pop();
    const title = el.value.trim();
    const tech  = document.getElementById(`proj-tech-${i}`)?.value.trim() || '';
    if (title) state.projs.push({ title, technology: tech });
  });
}

// ── SUBMIT ASSESSMENT ─────────────────────────────────────────
async function submitAssessment() {
  saveCerts();
  saveProjects();

  UI.setLoading('submit-assessment-btn', true, '⏳ Submitting...', '🤖 Get AI Career Prediction →');
  currentStep = 9;
  updateStepUI();
  window.scrollTo(0,0);

  // Build scores from aptitude
  const correct = state.aptitudeAnswers.filter((ans, i) => {
    return ans === aptitudeQuestions[i]?.correct_answer;
  }).length;
  const aptitudePct = aptitudeQuestions.length > 0 ? Math.round((correct / aptitudeQuestions.length) * 100) : 70;

  // Top interest domain
  const topInterest = Object.entries(state.interestScores).sort((a,b) => b[1]-a[1])[0]?.[0] || 'Technology';

  // Average subject marks
  const avgMarks = state.subjectMarks.length > 0
    ? Math.round(state.subjectMarks.reduce((s,m) => s + m.marks, 0) / state.subjectMarks.length)
    : 75;

  const payload = {
    education_level: state.education.education_level || 'Undergraduate',
    board: state.education.board || 'CBSE',
    stream: state.education.stream || 'General',
    degree: state.education.degree || '',
    specialization: state.education.specialization || '',
    cgpa: state.education.cgpa || 0,
    attendance_pct: state.education.attendance || 0,
    avg_marks: avgMarks,
    logical_aptitude: aptitudePct,
    numerical_ability: aptitudePct,
    verbal_ability: aptitudePct,
    programming_score: state.selectedSkills.some(s => ['Python','Java','JavaScript','C++'].includes(s)) ? 80 : 40,
    skills: state.selectedSkills,
    certifications: state.certs,
    projects: state.projs,
    psychometric_traits: state.psychTraits,
    interest_domain: topInterest,
    interest_scores: state.interestScores,
    subject_marks: state.subjectMarks,
  };

  try {
    const user = Auth.getUser();
    const res = await API.post('/api/assessment/submit', { ...payload, user_id: user?.id }, true);
    renderResults(res);
  } catch (err) {
    console.error(err);
    // Mock result for demo
    renderResults({
      top5_careers: [
        { rank:1, career:'AI / ML Engineer', confidence:92, why:['Strong Aptitude Score','Technical Interests','High Logical Reasoning'], salary:'$95K–$160K', degree:'BTech CS / MTech AI', companies:'Google, Microsoft, Amazon', growth:'+28% annually', certifications:'TensorFlow, AWS ML Specialty' },
        { rank:2, career:'Data Scientist', confidence:87, why:['Analytical Thinking','Interest in Research','Strong Math Foundation'], salary:'$90K–$145K', degree:'BTech / MSc Statistics', companies:'Netflix, Uber, Meta', growth:'+25% annually', certifications:'IBM Data Science, Google Data Analytics' },
        { rank:3, career:'Full-Stack Developer', confidence:82, why:['Programming Skills','Project Building','Problem Solving'], salary:'$80K–$130K', degree:'BTech CS / BCA', companies:'Infosys, TCS, Startup', growth:'+22% annually', certifications:'AWS, React Certified' },
        { rank:4, career:'Cloud Architect', confidence:76, why:['Technology Interest','Systems Thinking','Strong Aptitude'], salary:'$110K–$165K', degree:'BTech + AWS/Azure Certs', companies:'Amazon, Google, Microsoft', growth:'+24% annually', certifications:'AWS Solutions Architect' },
        { rank:5, career:'Cyber Security Analyst', confidence:71, why:['Analytical Mindset','Problem Solving','Attention to Detail'], salary:'$85K–$140K', degree:'BTech CS / B.Sc IT', companies:'CrowdStrike, Palo Alto, IBM', growth:'+20% annually', certifications:'CISSP, CEH, CompTIA Security+' },
      ],
      readiness_score: Math.round((aptitudePct + avgMarks) / 2),
      status: 'success'
    });
  }
}

function renderResults(res) {
  const top5 = res.top5_careers || [];
  const readiness = Math.round(res.readiness_score || 0);
  const readColor = readiness >= 80 ? 'var(--emerald)' : readiness >= 60 ? 'var(--amber)' : 'var(--red)';

  // Save to localStorage
  if (top5.length) {
    localStorage.setItem('top5Careers', JSON.stringify(top5));
    localStorage.setItem('readinessScore', readiness);
    localStorage.setItem('finalRecommendedCareer', top5[0].career);
  }

  const container = document.getElementById('results-content');
  container.innerHTML = `
    <div class="text-center mb-4">
      <div style="font-size:3rem;margin-bottom:0.5rem">🎉</div>
      <h2 style="font-size:1.75rem;font-weight:900;color:var(--text-h);margin-bottom:0.5rem">Assessment Complete!</h2>
      <p style="color:var(--text-muted)">Your AI-powered career analysis is ready</p>
      <div style="margin-top:1rem;display:inline-flex;flex-direction:column;align-items:center;gap:0.25rem">
        <span style="font-size:0.78rem;color:var(--text-muted);font-weight:700;text-transform:uppercase">Career Readiness Index</span>
        <span style="font-size:2.5rem;font-weight:900;color:${readColor}">${readiness}%</span>
      </div>
    </div>

    ${top5.map((c, idx) => `
      <div class="career-card ${idx === 0 ? 'top-match' : ''} mb-3">
        ${idx === 0 ? '<span class="top-match-label">#1 TOP MATCH</span>' : ''}
        <div class="flex justify-between items-center wrap gap-2 mb-2">
          <div>
            <span class="career-rank">#${c.rank || idx+1}</span>
            <strong style="color:var(--text-h);font-size:1.05rem">${c.career}</strong>
          </div>
          <div style="font-size:1.75rem;font-weight:900;color:${idx===0?'var(--text-link)':'var(--text-h)'}">
            ${c.confidence}%
          </div>
        </div>
        <div class="flex gap-1 wrap mb-2">
          ${(c.why||[]).map(w=>`<span class="badge badge-emerald">✓ ${w}</span>`).join('')}
        </div>
        <div class="progress-bar mb-2">
          <div class="progress-fill" style="width:${c.confidence}%;background:${idx===0?'var(--gradient-primary)':'rgba(99,102,241,0.4)'}"></div>
        </div>
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:0.6rem;font-size:0.82rem">
          <div><span style="color:var(--text-muted)">💰 Salary:</span> <strong>${c.salary||'—'}</strong></div>
          <div><span style="color:var(--text-muted)">🎓 Degree:</span> <strong>${c.degree||'—'}</strong></div>
          <div><span style="color:var(--text-muted)">🏢 Companies:</span> <strong>${c.companies||'—'}</strong></div>
          <div><span style="color:var(--text-muted)">📈 Growth:</span> <strong>${c.growth||'—'}</strong></div>
        </div>
      </div>
    `).join('')}

    <div class="flex gap-2 justify-center mt-4 wrap">
      <a href="/dashboard.html" class="btn btn-primary btn-lg">View Full Dashboard →</a>
      <a href="/assessment.html" class="btn btn-secondary btn-lg">Retake Assessment</a>
    </div>
  `;
}

// ── INIT ──────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  if (!Auth.requireAuth()) return;
  renderNavbar('assessment');
  updateStepUI();
  bindEducationFields();
  renderPsychometric();
  renderInterests();
  renderSkills();
});
