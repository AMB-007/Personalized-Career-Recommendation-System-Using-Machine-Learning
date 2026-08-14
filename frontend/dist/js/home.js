/* ============================================================
   home.js — CareerAI Home Page Logic
   ============================================================ */

/* ── DATA ───────────────────────────────────────────────────── */

const PREVIEWS = {
  tech:     { top:'AI / ML Engineer',      score:94, readiness:88, color:'#4f46e5', matches:[['AI / ML Engineer',94],['Data Scientist',90],['Full-Stack Developer',85],['Cloud Architect',81],['Cyber Security Analyst',76]], why:['Strong Logical Aptitude','Verified Python Skills','High AI Interest'] },
  business: { top:'Business Analyst',      score:92, readiness:86, color:'#d97706', matches:[['Business Analyst',92],['Financial Manager',88],['Product Manager',84],['Management Consultant',80],['Data Analyst',75]], why:['Leadership Trait (85%)','Financial Aptitude','High Communication'] },
  medical:  { top:'Doctor / MBBS',         score:91, readiness:84, color:'#059669', matches:[['Doctor / MBBS',91],['Biomedical Engineer',86],['Pharmacist',81],['Clinical Researcher',78],['Health Tech Specialist',73]], why:['Biology Score (91%)','Healthcare Interest','Research Curiosity'] },
  creative: { top:'UI/UX Designer',        score:89, readiness:82, color:'#ec4899', matches:[['UI/UX Designer',89],['Brand Manager',84],['Graphic Designer',81],['Animator',77],['Content Strategist',72]], why:['Creativity Trait (88%)','Spatial Aptitude','Design Interest'] },
};

const FEATURES = [
  { icon:'🎯', title:'Top 5 Career Matches',       desc:'Ranked career recommendations based on your unique profile — not generic advice. Each match shows confidence percentage.' },
  { icon:'💰', title:'Salary & Job Market Info',    desc:'See average salary range, top hiring companies, and job market growth rate for each recommended career.' },
  { icon:'🗺️', title:'Personalized Learning Roadmap', desc:'Step-by-step plan: what skills to build, which certifications to earn, and how to land your first job.' },
  { icon:'🔍', title:'Skills Gap Analysis',         desc:'Know exactly which skills you have and which ones you need to develop for your target career.' },
  { icon:'📊', title:'Career Readiness Score',      desc:'A 0–100% score showing how career-ready you are today, based on academics, aptitude, and verified skills.' },
  { icon:'🤖', title:'AI Explainability (XAI)',     desc:"Understand why each career was recommended. SHAP attribution shows exactly what factors influenced the AI's decision." },
];

const DOMAINS = [
  { icon:'💻', bg:'#eef2ff', iconColor:'#4f46e5', title:'Technology & AI',      roles:'AI Engineer · Data Scientist · Full-Stack Developer · Cloud Architect · Cybersecurity Analyst', salary:'₹6–20 LPA', growth:'+28%/yr' },
  { icon:'📊', bg:'#fef3c7', iconColor:'#d97706', title:'Business & Finance',   roles:'Business Analyst · Financial Manager · Product Manager · Management Consultant · Data Analyst', salary:'₹5–18 LPA', growth:'+18%/yr' },
  { icon:'🧬', bg:'#d1fae5', iconColor:'#059669', title:'Healthcare & Medical', roles:'Doctor · Biomedical Engineer · Pharmacist · Clinical Researcher · Health Tech Specialist', salary:'₹6–22 LPA', growth:'+21%/yr' },
  { icon:'⚙️', bg:'#ffedd5', iconColor:'#ea580c', title:'Engineering',          roles:'Mechanical · Civil · Aerospace · Electronics · Chemical · Automobile Engineer', salary:'₹4–16 LPA', growth:'+14%/yr' },
  { icon:'🎨', bg:'#fce7f3', iconColor:'#db2777', title:'Design & Creative',    roles:'UI/UX Designer · Animator · Graphic Designer · Brand Manager · Content Creator', salary:'₹4–14 LPA', growth:'+16%/yr' },
  { icon:'⚖️', bg:'#ede9fe', iconColor:'#7c3aed', title:'Law & Public Service', roles:'Lawyer · IAS Officer · Army Officer · Policy Analyst · Magistrate · Judge', salary:'₹5–20 LPA', growth:'+10%/yr' },
];

const PIPELINE = [
  { step:'01', icon:'🎓', title:'Education Profiling',        desc:'Set your class, board, stream, degree & specialization. Questions are customized to your exact level.' },
  { step:'02', icon:'📈', title:'Academic Performance',       desc:'Enter subject marks, CGPA and attendance. Your academic strength is a key input for career matching.' },
  { step:'03', icon:'🧩', title:'Adaptive Aptitude Test',     desc:'MCQs that change difficulty based on your live performance — gets harder if you answer correctly.' },
  { step:'04', icon:'🧠', title:'Situational Psychometrics',  desc:'Real-life scenarios that reveal your leadership, teamwork, resilience, and decision-making style.' },
  { step:'05', icon:'🎯', title:'Interest Profiling',         desc:'Choose between activities to map your interest scores across 9 career domains — fast and accurate.' },
  { step:'06', icon:'🔬', title:'Skill Verification',         desc:'Only your selected skills are tested. Get a verified proficiency level for each skill.' },
  { step:'07', icon:'🏆', title:'Portfolio & Certifications', desc:'Add your projects, GitHub links, and certificates to boost your Career Readiness Score.' },
  { step:'08', icon:'🤖', title:'AI Career Prediction',       desc:'XGBoost model trained on 40,000 student records generates your Top 5 career matches with confidence scores.' },
];

const ELIGIBILITY = [
  { icon:'📚', label:'School — Class 7 to 10', boards:'CBSE · ICSE · State Boards', note:'Early career awareness' },
  { icon:'🏫', label:'Class 11 & 12',          boards:'Science · Commerce · Humanities', note:'Stream-specific guidance' },
  { icon:'🎓', label:'Undergraduate',           boards:'B.Tech · B.Sc · B.Com · BBA · MBBS · LLB', note:'Specialization selection' },
  { icon:'🏅', label:'Postgraduate',            boards:'M.Tech · MBA · M.Sc · CA · PhD', note:'Advanced career planning' },
];

const TESTIMONIALS = [
  { name:'Arjun M.', initials:'A', level:'BTech CSE — Final Year', text:'The aptitude test actually adapted to my level! Questions got harder as I went. My Top 5 careers matched exactly what I had been thinking about — but now I have salary data and a roadmap.' },
  { name:'Priya S.', initials:'P', level:'Class 12 Science — CBSE', text:'I was confused between Engineering and Medicine. This test made it clear. The psychometric scenarios felt very real and the AI explained why each career was recommended for me.' },
  { name:'Rahul K.', initials:'R', level:'MBA Graduate', text:'Feels like a professional career assessment platform. The skill verification MCQs gave me an actual score. The career readiness index showed me exactly where I need to improve.' },
];

const FAQS = [
  { q:'Who is this for?',                  a:'Any student from Class 7 to Professional Degrees (B.Tech, MBBS, MBA, M.Tech, LLB, CA, etc.). The assessment automatically detects your level and adjusts all questions accordingly.' },
  { q:'How long does the assessment take?', a:'About 10 minutes. You can save your progress and continue later if needed. There is no time limit on the assessment itself.' },
  { q:'Why do I get Top 5 careers instead of just 1?', a:'Career planning is not black-and-white. You get 5 ranked career matches with confidence percentages so you can compare salary, growth rate, required degree, and top companies before making a decision.' },
  { q:'What is the Career Readiness Score?', a:'A composite score from 0 to 100 that measures how ready you are for the job market today. It factors in academic performance (20%), logical aptitude (25%), verified skills (20%), psychometric traits (15%), and projects/certifications (20%).' },
  { q:'Is this free?',                     a:'Yes, completely free. No credit card required. Create an account and start your assessment immediately.' },
  { q:'How is this different from a basic career quiz?', a:'A basic quiz asks "what do you like?" and returns a category. CareerAI runs a 9-stage adaptive pipeline — aptitude battery, situational psychometrics, skill verification MCQs, and a machine learning model trained on 40,000 student records across 272 careers.' },
];

/* ── RENDER FUNCTIONS ────────────────────────────────────────── */

/* Hero career preview */
function renderPreview(key) {
  const p = PREVIEWS[key];
  const body = document.getElementById('hero-preview-body');
  if (!body) return;

  body.innerHTML = `
    <div style="margin-bottom:0.85rem">
      <div style="font-size:0.72rem;color:var(--text-muted);font-weight:700;text-transform:uppercase;letter-spacing:0.04em;margin-bottom:0.25rem">Top Match</div>
      <div style="font-size:1.05rem;font-weight:900;color:var(--text-h)">${p.top}</div>
      <div style="display:flex;gap:0.4rem;flex-wrap:wrap;margin-top:0.5rem">
        ${p.why.map(w => `<span style="background:var(--emerald-light);color:var(--emerald);font-size:0.7rem;font-weight:700;padding:0.15rem 0.5rem;border-radius:4px">✓ ${w}</span>`).join('')}
      </div>
    </div>
    <div style="border-top:1px solid var(--border);padding-top:0.85rem">
      <div style="font-size:0.72rem;font-weight:700;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.04em;margin-bottom:0.6rem">All 5 Career Matches</div>
      ${p.matches.map(([career, conf], i) => `
        <div class="rp-career-row">
          <span class="career-name" style="${i===0?'color:var(--primary)':''}">#${i+1} ${career}</span>
          <div class="career-bar">
            <div class="rp-bar-track">
              <div class="rp-bar-fill" style="width:${conf}%;background:${i===0?'var(--primary)':p.color}"></div>
            </div>
            <span class="rp-pct" style="color:${i===0?'var(--primary)':p.color}">${conf}%</span>
          </div>
        </div>
      `).join('')}
    </div>
  `;

  document.querySelectorAll('#preview-tabs .tab-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.key === key);
  });
}

/* Features grid */
function renderFeatures() {
  const grid = document.getElementById('features-grid');
  if (!grid) return;
  grid.innerHTML = FEATURES.map(f => `
    <div class="why-card">
      <div class="why-icon">${f.icon}</div>
      <div>
        <h4>${f.title}</h4>
        <p>${f.desc}</p>
      </div>
    </div>
  `).join('');
}

/* Career domains */
function renderDomains() {
  const grid = document.getElementById('domains-grid');
  if (!grid) return;
  grid.innerHTML = DOMAINS.map(d => `
    <div class="career-domain-card">
      <div class="career-domain-icon" style="background:${d.bg};color:${d.iconColor}">${d.icon}</div>
      <h4>${d.title}</h4>
      <div class="domain-roles">${d.roles}</div>
      <div class="domain-meta">
        <div class="domain-salary">Avg: ${d.salary}</div>
        <div class="domain-growth">↑ ${d.growth}</div>
      </div>
    </div>
  `).join('');
}

/* Pipeline */
function renderPipeline() {
  const grid = document.getElementById('pipeline-grid');
  if (!grid) return;
  grid.innerHTML = PIPELINE.map(p => `
    <div class="pipeline-card card-hover reveal">
      <span class="pipeline-step">${p.step}</span>
      <div class="pipeline-icon">${p.icon}</div>
      <h3>${p.title}</h3>
      <p>${p.desc}</p>
    </div>
  `).join('');
}

/* Eligibility */
function renderEligibility() {
  const grid = document.getElementById('eligibility-grid');
  if (!grid) return;
  grid.innerHTML = ELIGIBILITY.map(e => `
    <div class="card" style="text-align:center;padding:1.75rem">
      <div style="font-size:2.2rem;margin-bottom:0.85rem">${e.icon}</div>
      <h4 style="font-family:var(--font-heading);font-weight:800;color:var(--text-h);font-size:0.96rem;margin-bottom:0.4rem">${e.label}</h4>
      <p style="font-size:0.8rem;color:var(--text-muted);margin-bottom:0.65rem;line-height:1.6">${e.boards}</p>
      <span class="badge badge-primary">${e.note}</span>
    </div>
  `).join('');
}

/* Testimonials */
function renderTestimonials() {
  const grid = document.getElementById('testimonials-grid');
  if (!grid) return;
  grid.innerHTML = TESTIMONIALS.map(t => `
    <div class="testimonial-card">
      <div class="t-stars">★★★★★</div>
      <p class="t-text">"${t.text}"</p>
      <div class="t-author">
        <div class="t-avatar">${t.initials}</div>
        <div>
          <div class="t-name">${t.name}</div>
          <div class="t-level">${t.level}</div>
        </div>
      </div>
    </div>
  `).join('');
}

/* FAQ */
function renderFAQ() {
  const list = document.getElementById('faq-list');
  if (!list) return;
  list.innerHTML = FAQS.map((faq, i) => `
    <div class="faq-item${i === 0 ? ' open' : ''}" data-i="${i}">
      <button class="faq-btn">
        <span class="faq-question">${faq.q}</span>
        <span class="faq-icon">+</span>
      </button>
      <div class="faq-answer"${i === 0 ? ' style="display:block"' : ''}>${faq.a}</div>
    </div>
  `).join('');

  list.querySelectorAll('.faq-item').forEach(item => {
    item.querySelector('.faq-btn').addEventListener('click', () => {
      const wasOpen = item.classList.contains('open');
      list.querySelectorAll('.faq-item').forEach(i => { i.classList.remove('open'); i.querySelector('.faq-answer').style.display = 'none'; });
      if (!wasOpen) {
        item.classList.add('open');
        item.querySelector('.faq-answer').style.display = 'block';
      }
    });
  });
}

/* Animated stat counters */
function animateCounter(el, target, suffix, duration = 1600) {
  const start = performance.now();
  const step = (now) => {
    const progress = Math.min((now - start) / duration, 1);
    const eased    = 1 - Math.pow(1 - progress, 3);
    const current  = Math.round(target * eased);
    el.textContent = current + suffix;
    if (progress < 1) requestAnimationFrame(step);
  };
  requestAnimationFrame(step);
}

/* ── INIT ────────────────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  renderNavbar('home');

  const user = Auth.getUser();

  /* CTA buttons */
  const startBtn     = document.getElementById('start-btn');
  const startBtn2    = document.getElementById('start-btn-2');
  const ctaStartBtn  = document.getElementById('cta-start-btn');
  const ctaLoginLink = document.getElementById('cta-login-link');
  const ctaDesc      = document.getElementById('cta-desc');

  const handleStart = () => { window.location.href = user ? '/assessment.html' : '/register.html'; };

  if (user) {
    [startBtn, startBtn2, ctaStartBtn].forEach(b => { if (b) b.textContent = 'Continue Assessment →'; });
    if (ctaLoginLink) ctaLoginLink.style.display = 'none';
    if (ctaDesc) ctaDesc.textContent = `Welcome back, ${user.full_name?.split(' ')[0] || 'there'}! Pick up where you left off.`;
  }

  [startBtn, startBtn2, ctaStartBtn].forEach(b => b?.addEventListener('click', handleStart));

  /* Preview tabs */
  document.getElementById('preview-tabs')?.addEventListener('click', e => {
    const btn = e.target.closest('[data-key]');
    if (btn) renderPreview(btn.dataset.key);
  });

  /* Render all sections */
  renderPreview('tech');
  renderFeatures();
  renderDomains();
  renderPipeline();
  renderEligibility();
  renderTestimonials();
  renderFAQ();

  /* Pipeline card reveal stagger */
  document.querySelectorAll('.pipeline-card').forEach((card, i) => {
    card.style.transitionDelay = `${i * 0.06}s`;
  });

  /* Animated counters */
  const statsSection = document.getElementById('stats-section');
  if (statsSection) {
    let animated = false;
    new IntersectionObserver(entries => {
      if (entries[0].isIntersecting && !animated) {
        animated = true;
        document.querySelectorAll('.stat-number[data-target]').forEach(el => {
          animateCounter(el, parseInt(el.dataset.target, 10), el.dataset.suffix || '');
        });
      }
    }, { threshold: 0.3 }).observe(statsSection);
  }

  /* Scroll-reveal for .reveal elements (re-run for dynamically added elements) */
  const revealObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('revealed');
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -30px 0px' });

  setTimeout(() => {
    document.querySelectorAll('.reveal:not(.revealed)').forEach(el => revealObserver.observe(el));
  }, 100);
});
