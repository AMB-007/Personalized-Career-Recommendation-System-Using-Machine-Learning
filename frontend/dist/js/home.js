/* home.js — Home page logic */

const PIPELINE = [
  { step:'01', icon:'🎓', title:'Education Profiling',       desc:'Class 7 to Professional Degrees — board, stream, degree & specialization detected automatically.' },
  { step:'02', icon:'📊', title:'Academic Performance',      desc:'Board-specific subject marks, CGPA, attendance percentage and semester-wise grade analysis.' },
  { step:'03', icon:'🧩', title:'Adaptive Aptitude Battery', desc:'Database-driven MCQs with real-time difficulty adaptation based on live performance scores.' },
  { step:'04', icon:'🧠', title:'Situational Psychometrics', desc:'Indirect scenarios measuring Leadership, Teamwork, Resilience, Curiosity & Decision-Making traits.' },
  { step:'05', icon:'🎯', title:'Interest Profiling',        desc:'Pairwise activity choices map 9 career domain interest scores — Technology to Law & Healthcare.' },
  { step:'06', icon:'🔬', title:'Skill Verification',        desc:'Only your selected skills are tested. Adaptive MCQs compute verified proficiency levels.' },
  { step:'07', icon:'🏆', title:'Portfolio & Certifications',desc:'Projects, GitHub links and recognized certifications score your practical readiness.' },
  { step:'08', icon:'🤖', title:'ML Career Prediction',      desc:'XGBoost model trained on 40K students, 272 career labels. Top 5 matches with XAI chips.' },
];

const PREVIEWS = {
  tech:     { label:'Technology & AI',    color:'#6366f1', top:'AI / ML Engineer',  score:94, readiness:88, why:['Strong Logical Aptitude (88%)','Verified Python Skills','High AI Interest Score'], matches:[['AI / ML Engineer',94],['Data Scientist',90],['Full-Stack Developer',85],['Cloud Architect',81],['Cyber Security Analyst',76]] },
  business: { label:'Business & Finance', color:'#f59e0b', top:'Business Analyst',  score:92, readiness:86, why:['Leadership Trait (85%)','Financial Aptitude Score','High Communication Rating'], matches:[['Business Analyst',92],['Financial Manager',88],['Product Manager',84],['Management Consultant',80],['Data Analyst',75]] },
  medical:  { label:'Healthcare',         color:'#10b981', top:'Doctor / MBBS',     score:91, readiness:84, why:['Biology Score (91%)','Healthcare Interest (82%)','Research Curiosity Trait'], matches:[['Doctor / MBBS',91],['Biomedical Engineer',86],['Pharmacist',81],['Clinical Researcher',78],['Health Tech Specialist',73]] },
  creative: { label:'Design & Creative',  color:'#ec4899', top:'UI/UX Designer',    score:89, readiness:82, why:['Creativity Trait (88%)','Spatial Aptitude Score','Design Interest Domain'], matches:[['UI/UX Designer',89],['Brand Manager',84],['Graphic Designer',81],['Animator',77],['Content Strategist',72]] },
};

const DOMAINS = [
  { icon:'💻', title:'Technology & AI',     careers:['AI Engineer','Data Scientist','Full-Stack Developer','Cloud Architect'],          salary:'$95K–$160K', growth:'+28%', color:'#6366f1' },
  { icon:'📊', title:'Business & Finance',  careers:['Business Analyst','Financial Manager','Product Manager','Management Consultant'], salary:'$80K–$140K', growth:'+18%', color:'#f59e0b' },
  { icon:'🧬', title:'Healthcare',          careers:['Doctor / MBBS','Biomedical Engineer','Pharmacist','Clinical Researcher'],          salary:'$90K–$160K', growth:'+21%', color:'#10b981' },
  { icon:'⚙️', title:'Engineering',         careers:['Mechanical Engineer','Civil Engineer','Aerospace Engineer','Automobile Engineer'], salary:'$75K–$130K', growth:'+14%', color:'#f97316' },
  { icon:'🎨', title:'Design & Media',      careers:['UI/UX Designer','Animator','Graphic Designer','Brand Manager'],                   salary:'$65K–$120K', growth:'+16%', color:'#ec4899' },
  { icon:'⚖️', title:'Law & Public Service',careers:['Lawyer','IAS Officer','Army Officer','Judge'],                                    salary:'$60K–$130K', growth:'+10%', color:'#8b5cf6' },
];

const TESTIMONIALS = [
  { name:'Arjun M.', level:'BTech CSE — Undergraduate', text:'The adaptive aptitude test genuinely changed difficulty based on my answers. The Top 5 careers with salary and roadmap were exactly what I needed.', rating:5 },
  { name:'Priya S.', level:'Class 10 Student — CBSE', text:'It asked questions specific to my board subjects! The psychometric scenarios felt real and the career suggestions made complete sense.', rating:5 },
  { name:'Rahul K.', level:'MBA Graduate — Postgraduate', text:'Professional platform. The skill verification for Finance and Excel gave me a real score. Feels like Mercer Mettl but for career guidance.', rating:5 },
];

const FAQS = [
  { q:'What education levels are supported?', a:'Class 7 through Professional Degrees — including Class 8–10, Higher Secondary (all streams), Diploma, ITI, B.Tech, B.Sc, B.Com, BBA, MBBS, LLB, MBA, M.Tech, CA, and more. Questions adapt per level.' },
  { q:'Why Top 5 careers instead of 1?', a:'Enterprise career platforms like SHL and CareerExplorer show ranked matches with confidence percentages and explainability. You get 5 validated career paths with salary, required degree, top companies, and XAI attribution chips.' },
  { q:'How is this different from a simple quiz?', a:'It is a multi-stage pipeline: adaptive aptitude battery, indirect situational psychometrics, pairwise interest profiling, skill verification MCQs, and an XGBoost ML model trained on 40,000 student records across 272 careers.' },
  { q:'What is the Career Readiness Index?', a:'A composite score (0–100%) computed from Academic Performance (20%), Logical Aptitude (25%), Verified Skills (20%), Psychometric Traits (15%), Projects & Certifications (20%). Think of it as your employability readiness signal.' },
  { q:'Can admins manage the question bank?', a:'Yes. The Admin portal lets you add, edit, delete and paginate questions across education levels, boards, streams, degrees and categories. Each question maps to difficulty, weight, and expected time.' },
];

/* ── RENDER PIPELINE ─────────────────────────────────────────── */
function renderPipeline() {
  const grid = document.getElementById('pipeline-grid');
  if (!grid) return;
  grid.innerHTML = PIPELINE.map(p => `
    <div class="pipeline-card card-hover">
      <span class="pipeline-step">${p.step}</span>
      <div class="pipeline-icon">${p.icon}</div>
      <h3>${p.title}</h3>
      <p>${p.desc}</p>
    </div>
  `).join('');
}

/* ── PREVIEW CARD ────────────────────────────────────────────── */
let activePreview = 'tech';

function renderPreview(key) {
  activePreview = key;
  const p = PREVIEWS[key];
  const content = document.getElementById('preview-content');
  if (!content) return;
  content.innerHTML = `
    <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:0.85rem">
      <div>
        <div style="font-size:0.72rem;color:var(--text-muted);font-weight:700;text-transform:uppercase;letter-spacing:0.04em">Top Career Match #1</div>
        <div style="font-size:1.1rem;font-weight:900;color:var(--text-h);margin-top:0.2rem">${p.top}</div>
      </div>
      <div style="background:${p.color};color:#fff;padding:0.35rem 0.75rem;border-radius:8px;font-weight:900;font-size:0.9rem">${p.score}%</div>
    </div>
    <div style="display:flex;flex-wrap:wrap;gap:0.35rem;margin-bottom:1rem">
      ${p.why.map(w => `<span style="background:rgba(16,185,129,0.12);color:#059669;padding:0.2rem 0.55rem;border-radius:5px;font-size:0.72rem;font-weight:700">✓ ${w}</span>`).join('')}
    </div>
    <div style="border-top:1px solid var(--border);padding-top:0.85rem">
      <div style="display:flex;justify-content:space-between;margin-bottom:0.6rem">
        <span style="font-size:0.72rem;font-weight:700;color:var(--text-muted);text-transform:uppercase">Top 5 Ranked Careers</span>
        <span style="font-size:0.72rem;font-weight:800;color:#10b981">Readiness: ${p.readiness}%</span>
      </div>
      ${p.matches.map(([career,conf],i) => `
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.45rem">
          <span style="font-size:0.82rem;font-weight:${i===0?'900':'600'};color:${i===0?'var(--text-h)':'var(--text-muted)'}">#${i+1} ${career}</span>
          <div style="display:flex;align-items:center;gap:0.5rem">
            <div style="width:60px;height:4px;background:var(--border);border-radius:99px;overflow:hidden">
              <div style="height:100%;width:${conf}%;background:${p.color};border-radius:99px"></div>
            </div>
            <span style="font-size:0.78rem;font-weight:800;color:${p.color};min-width:32px">${conf}%</span>
          </div>
        </div>
      `).join('')}
    </div>
    <div style="margin-top:1rem;padding:0.6rem 0.85rem;background:var(--bg-card-subtle);border-radius:8px;font-size:0.75rem;color:var(--text-muted);font-weight:600;text-align:center">
      ⚡ XGBoost · 40K dataset · 272 career labels · SHAP XAI
    </div>
  `;

  // Update tab styles
  document.querySelectorAll('#preview-tabs .tab-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.key === key);
  });
}

/* ── DOMAIN EXPLORER ─────────────────────────────────────────── */
let activeDomain = 0;

function renderDomainTabs() {
  const tabs = document.getElementById('domain-tabs');
  if (!tabs) return;
  tabs.innerHTML = DOMAINS.map((d, i) => `
    <button class="domain-tab-btn${i === 0 ? ' active' : ''}" data-idx="${i}" style="${i === 0 ? `border-color:${d.color};color:${d.color};background:${d.color}18` : ''}">
      ${d.icon} ${d.title}
    </button>
  `).join('');

  tabs.querySelectorAll('.domain-tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      activeDomain = parseInt(btn.dataset.idx);
      tabs.querySelectorAll('.domain-tab-btn').forEach((b, i) => {
        const d = DOMAINS[i];
        b.className = 'domain-tab-btn' + (i === activeDomain ? ' active' : '');
        b.style = i === activeDomain ? `border-color:${d.color};color:${d.color};background:${d.color}18` : '';
      });
      renderDomainDetail();
    });
  });
}

function renderDomainDetail() {
  const d = DOMAINS[activeDomain];
  const detail = document.getElementById('domain-detail');
  if (!detail) return;
  detail.style.borderColor = d.color + '30';
  detail.innerHTML = `
    <div>
      <div style="font-size:2.5rem;margin-bottom:0.75rem">${d.icon}</div>
      <h3 style="font-size:1.4rem;font-weight:900;color:var(--text-h);margin-bottom:0.5rem">${d.title}</h3>
      <div style="display:flex;gap:1.5rem;margin-bottom:1.5rem">
        <div>
          <div style="font-size:0.72rem;color:var(--text-muted);font-weight:700;text-transform:uppercase">Avg Salary</div>
          <div style="font-weight:800;color:${d.color};font-size:1rem">${d.salary}</div>
        </div>
        <div>
          <div style="font-size:0.72rem;color:var(--text-muted);font-weight:700;text-transform:uppercase">Growth</div>
          <div style="font-weight:800;color:#10b981;font-size:1rem">${d.growth} annually</div>
        </div>
      </div>
      <a href="/register.html" class="btn btn-primary" style="background:${d.color};box-shadow:none">Explore Careers in ${d.title} →</a>
    </div>
    <div>
      <div style="font-size:0.75rem;font-weight:700;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.04em;margin-bottom:0.85rem">Sample Careers Predicted</div>
      ${d.careers.map(c => `
        <div style="display:flex;align-items:center;gap:0.65rem;padding:0.7rem 1rem;background:var(--bg-card);border-radius:10px;border:1px solid var(--border);margin-bottom:0.6rem">
          <span style="width:8px;height:8px;border-radius:50%;background:${d.color};flex-shrink:0;display:inline-block"></span>
          <span style="font-weight:700;color:var(--text-h);font-size:0.9rem">${c}</span>
        </div>
      `).join('')}
    </div>
  `;
}

/* ── TESTIMONIALS ─────────────────────────────────────────────── */
function renderTestimonials() {
  const grid = document.getElementById('testimonials-grid');
  if (!grid) return;
  grid.innerHTML = TESTIMONIALS.map(t => `
    <div class="card" style="display:flex;flex-direction:column;gap:1rem">
      <div>★★★★★</div>
      <p style="color:var(--text-muted);font-size:0.9rem;line-height:1.7;font-style:italic">"${t.text}"</p>
      <div>
        <div style="font-weight:800;color:var(--text-h);font-size:0.9rem">${t.name}</div>
        <div style="font-size:0.78rem;color:var(--text-muted);margin-top:0.15rem">${t.level}</div>
      </div>
    </div>
  `).join('');
}

/* ── FAQ ─────────────────────────────────────────────────────── */
function renderFAQ() {
  const list = document.getElementById('faq-list');
  if (!list) return;
  list.innerHTML = FAQS.map((faq, i) => `
    <div class="faq-item${i === 0 ? ' open' : ''}" data-i="${i}">
      <button class="faq-btn">
        <span class="faq-question">${faq.q}</span>
        <span class="faq-icon">+</span>
      </button>
      <div class="faq-answer" style="${i === 0 ? 'display:block' : ''}">${faq.a}</div>
    </div>
  `).join('');

  list.querySelectorAll('.faq-item').forEach(item => {
    item.querySelector('.faq-btn').addEventListener('click', () => {
      const wasOpen = item.classList.contains('open');
      list.querySelectorAll('.faq-item').forEach(i => i.classList.remove('open'));
      list.querySelectorAll('.faq-answer').forEach(a => a.style.display = 'none');
      if (!wasOpen) {
        item.classList.add('open');
        item.querySelector('.faq-answer').style.display = 'block';
      }
    });
  });
}

/* ── ANIMATED COUNTER ────────────────────────────────────────── */
function animateCounter(el, target, suffix, duration = 1800) {
  const start = performance.now();
  const isK = suffix === 'K';
  const displayTarget = isK ? target / 1000 : target;

  const step = (now) => {
    const elapsed = now - start;
    const progress = Math.min(elapsed / duration, 1);
    // Ease out cubic
    const eased = 1 - Math.pow(1 - progress, 3);
    const current = Math.round(displayTarget * eased);

    if (isK) {
      el.textContent = current >= 1 ? current + 'K' : Math.round(target * eased);
    } else {
      el.textContent = current + suffix;
    }
    if (progress < 1) requestAnimationFrame(step);
  };
  requestAnimationFrame(step);
}

/* ── INIT ────────────────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  renderNavbar('home');

  const user = Auth.getUser();

  // Start button
  const startBtn    = document.getElementById('start-btn');
  const ctaStartBtn = document.getElementById('cta-start-btn');
  const ctaLoginLink = document.getElementById('cta-login-link');
  const ctaDesc     = document.getElementById('cta-desc');

  if (user) {
    if (startBtn)     startBtn.textContent    = 'Continue Assessment →';
    if (ctaStartBtn)  ctaStartBtn.textContent = 'Continue Assessment →';
    if (ctaLoginLink) ctaLoginLink.style.display = 'none';
    if (ctaDesc)      ctaDesc.textContent = `Welcome back, ${user.full_name?.split(' ')[0]}! Continue your AI career assessment.`;
  }

  const handleStart = () => { window.location.href = user ? '/assessment.html' : '/register.html'; };
  startBtn?.addEventListener('click', handleStart);
  ctaStartBtn?.addEventListener('click', handleStart);

  // Preview tabs
  document.getElementById('preview-tabs')?.addEventListener('click', e => {
    const btn = e.target.closest('[data-key]');
    if (btn) renderPreview(btn.dataset.key);
  });

  renderPreview('tech');
  renderPipeline();
  renderDomainTabs();
  renderDomainDetail();
  renderTestimonials();
  renderFAQ();

  // Add staggered animation delays to pipeline cards
  document.querySelectorAll('.pipeline-card').forEach((card, i) => {
    card.classList.add('reveal');
    card.style.transitionDelay = `${i * 0.07}s`;
  });

  // Animated stat counters when stats section enters viewport
  const statsSection = document.getElementById('stats-section');
  if (statsSection) {
    let animated = false;
    const counterObserver = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting && !animated) {
          animated = true;
          document.querySelectorAll('.stat-number[data-target]').forEach(el => {
            const target = parseInt(el.dataset.target, 10);
            const suffix = el.dataset.suffix || '';
            animateCounter(el, target, suffix);
          });
        }
      });
    }, { threshold: 0.3 });
    counterObserver.observe(statsSection);
  }
});
