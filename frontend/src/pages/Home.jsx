import { useState, useEffect, useRef } from 'react';
import { Link, useNavigate } from 'react-router-dom';

/* ─────────────────────────────────────────────────────────────────────────
   STATIC DATA
───────────────────────────────────────────────────────────────────────── */
const PIPELINE = [
  { step: '01', icon: '🎓', title: 'Education Profiling',       desc: 'Class 7 to Professional Degrees — board, stream, degree & specialization detected automatically.' },
  { step: '02', icon: '📊', title: 'Academic Performance',      desc: 'Board-specific subject marks, CGPA, attendance percentage and semester-wise grade analysis.' },
  { step: '03', icon: '🧩', title: 'Adaptive Aptitude Battery', desc: 'Database-driven MCQs with real-time difficulty adaptation based on live performance scores.' },
  { step: '04', icon: '🧠', title: 'Situational Psychometrics', desc: 'Indirect scenarios measuring Leadership, Teamwork, Resilience, Curiosity & Decision-Making traits.' },
  { step: '05', icon: '🎯', title: 'Interest Profiling',        desc: 'Pairwise activity choices map 9 career domain interest scores — Technology to Law & Healthcare.' },
  { step: '06', icon: '🔬', title: 'Skill Verification',        desc: 'Only your selected skills are tested. Adaptive MCQs compute verified proficiency levels.' },
  { step: '07', icon: '🏆', title: 'Portfolio & Certifications',desc: 'Projects, GitHub links and recognized certifications score your practical readiness.' },
  { step: '08', icon: '🤖', title: 'ML Career Prediction',      desc: 'LightGBM model trained on 35K students, 272 career labels. Top 5 matches with XAI chips.' },
];

const PREVIEWS = {
  tech: {
    label: 'Technology & AI',
    color: '#6366f1',
    top: 'AI / ML Engineer',
    score: 94,
    readiness: 88,
    why: ['Strong Logical Aptitude (88%)', 'Verified Python Skills', 'High AI Interest Score'],
    matches: [['AI / ML Engineer', 94], ['Data Scientist', 90], ['Full-Stack Developer', 85], ['Cloud Architect', 81], ['Cyber Security Analyst', 76]],
  },
  business: {
    label: 'Business & Finance',
    color: '#f59e0b',
    top: 'Business Analyst',
    score: 92,
    readiness: 86,
    why: ['Leadership Trait (85%)', 'Financial Aptitude Score', 'High Communication Rating'],
    matches: [['Business Analyst', 92], ['Financial Manager', 88], ['Product Manager', 84], ['Management Consultant', 80], ['Data Analyst', 75]],
  },
  medical: {
    label: 'Healthcare & Medical',
    color: '#10b981',
    top: 'Doctor / MBBS',
    score: 91,
    readiness: 84,
    why: ['Biology Score (91%)', 'Healthcare Interest (82%)', 'Research Curiosity Trait'],
    matches: [['Doctor / MBBS', 91], ['Biomedical Engineer', 86], ['Pharmacist', 81], ['Clinical Researcher', 78], ['Health Tech Specialist', 73]],
  },
  creative: {
    label: 'Design & Creative Arts',
    color: '#ec4899',
    top: 'UI/UX Designer',
    score: 89,
    readiness: 82,
    why: ['Creativity Trait (88%)', 'Spatial Aptitude Score', 'Design Interest Domain'],
    matches: [['UI/UX Designer', 89], ['Brand Manager', 84], ['Graphic Designer', 81], ['Animator', 77], ['Content Strategist', 72]],
  },
};

const STATS = [
  { number: '35K',  label: 'Training Dataset Records' },
  { number: '272',  label: 'Career Labels Predicted' },
  { number: '9',    label: 'Adaptive Assessment Steps' },
  { number: '100%', label: 'Explainable AI (XAI)' },
];

const DOMAINS = [
  { icon: '💻', title: 'Technology & AI',     careers: ['AI Engineer', 'Data Scientist', 'Full-Stack Developer', 'Cloud Architect'],          salary: '$95K–$160K',  growth: '+28%', color: '#6366f1' },
  { icon: '📊', title: 'Business & Finance',  careers: ['Business Analyst', 'Financial Manager', 'Product Manager', 'Management Consultant'], salary: '$80K–$140K',  growth: '+18%', color: '#f59e0b' },
  { icon: '🧬', title: 'Healthcare',           careers: ['Doctor / MBBS', 'Biomedical Engineer', 'Pharmacist', 'Clinical Researcher'],          salary: '$90K–$160K',  growth: '+21%', color: '#10b981' },
  { icon: '⚙️', title: 'Engineering',          careers: ['Mechanical Engineer', 'Civil Engineer', 'Aerospace Engineer', 'Automobile Engineer'], salary: '$75K–$130K',  growth: '+14%', color: '#f97316' },
  { icon: '🎨', title: 'Design & Media',       careers: ['UI/UX Designer', 'Animator', 'Graphic Designer', 'Brand Manager'],                   salary: '$65K–$120K',  growth: '+16%', color: '#ec4899' },
  { icon: '⚖️', title: 'Law & Public Service', careers: ['Lawyer', 'IAS Officer', 'Army Officer', 'Judge'],                                    salary: '$60K–$130K',  growth: '+10%', color: '#8b5cf6' },
];

const FAQS = [
  { q: 'What education levels are supported?', a: 'Class 7 through Professional Degrees — including Class 8–10, Higher Secondary (all streams), Diploma, ITI, B.Tech, B.Sc, B.Com, BBA, MBBS, LLB, MBA, M.Tech, CA, and more. Questions adapt per level.' },
  { q: 'Why Top 5 careers instead of 1?', a: 'Enterprise career platforms like SHL and CareerExplorer show ranked matches with confidence percentages and explainability. You get 5 validated career paths with salary, required degree, top companies, and XAI attribution chips.' },
  { q: 'How is this different from a simple quiz?', a: 'It is a multi-stage pipeline: adaptive aptitude battery, indirect situational psychometrics, pairwise interest profiling, skill verification MCQs, and a LightGBM ML model trained on 35,000 student records across 272 careers.' },
  { q: 'What is the Career Readiness Index?', a: 'A composite score (0–100%) computed from Academic Performance (20%), Logical Aptitude (25%), Verified Skills (20%), Psychometric Traits (15%), Projects & Certifications (20%). Think of it as your employability readiness signal.' },
  { q: 'Can admins manage the question bank?', a: 'Yes. The Admin portal lets you add, edit, delete and paginate questions across education levels, boards, streams, degrees and categories. Each question maps to difficulty, weight, and expected time.' },
];

const TESTIMONIALS = [
  { name: 'Arjun M.', level: 'BTech CSE — Undergraduate', text: 'The adaptive aptitude test genuinely changed difficulty based on my answers. The Top 5 careers with salary and roadmap were exactly what I needed.', rating: 5 },
  { name: 'Priya S.', level: 'Class 10 Student — CBSE', text: 'It asked questions specific to my board subjects! The psychometric scenarios felt real and the career suggestions made complete sense.', rating: 5 },
  { name: 'Rahul K.', level: 'MBA Graduate — Postgraduate', text: 'Professional platform. The skill verification for Finance and Excel gave me a real score. Feels like Mercer Mettl but for career guidance.', rating: 5 },
];

/* ─────────────────────────────────────────────────────────────────────────
   HOME COMPONENT
───────────────────────────────────────────────────────────────────────── */
const Home = () => {
  const navigate = useNavigate();
  const [activePreview, setActivePreview]     = useState('tech');
  const [activeDomain, setActiveDomain]       = useState(0);
  const [openFaq, setOpenFaq]                 = useState(0);
  const [visibleStats, setVisibleStats]       = useState(false);
  const statsRef = useRef(null);

  const userStr = localStorage.getItem('userInfo') || localStorage.getItem('user');
  const user    = userStr ? JSON.parse(userStr) : null;

  // Intersection observer for stats animation
  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => { if (entry.isIntersecting) setVisibleStats(true); },
      { threshold: 0.3 }
    );
    if (statsRef.current) observer.observe(statsRef.current);
    return () => observer.disconnect();
  }, []);

  const handleStart = () => navigate(user ? '/assessment' : '/register');

  const preview = PREVIEWS[activePreview];
  const domain  = DOMAINS[activeDomain];

  return (
    <div style={{ overflowX: 'hidden' }}>

      {/* ══════════════════════════════════════════════════════════════════
          1. HERO
      ══════════════════════════════════════════════════════════════════ */}
      <section style={{
        minHeight: '92vh', display: 'flex', alignItems: 'center',
        padding: '5rem 1.5rem 4rem',
        background: 'radial-gradient(ellipse 80% 60% at 50% -10%, rgba(99,102,241,0.18) 0%, transparent 70%), var(--bg-page)',
        position: 'relative', overflow: 'hidden',
      }}>
        {/* Background decorative blobs */}
        <div style={{ position: 'absolute', top: '10%', right: '5%', width: '480px', height: '480px', background: 'radial-gradient(circle, rgba(139,92,246,0.1) 0%, transparent 70%)', borderRadius: '50%', pointerEvents: 'none' }} />
        <div style={{ position: 'absolute', bottom: '5%', left: '0%', width: '380px', height: '380px', background: 'radial-gradient(circle, rgba(16,185,129,0.08) 0%, transparent 70%)', borderRadius: '50%', pointerEvents: 'none' }} />

        <div style={{ maxWidth: '1280px', margin: '0 auto', width: '100%', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '4rem', alignItems: 'center' }}>

          {/* LEFT: Headline */}
          <div>
            <div style={{ display: 'inline-flex', alignItems: 'center', gap: '0.5rem', background: 'var(--badge-bg)', border: '1px solid var(--badge-border)', color: 'var(--badge-text)', borderRadius: '999px', padding: '0.4rem 1rem', fontSize: '0.78rem', fontWeight: '800', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '1.5rem' }}>
              <span style={{ display: 'inline-block', width: '6px', height: '6px', borderRadius: '50%', background: '#10b981', animation: 'pulse 2s infinite' }} />
              AI-Powered Enterprise Career Platform
            </div>

            <h1 style={{ fontFamily: 'var(--heading-font)', fontSize: 'clamp(2.2rem, 5vw, 3.5rem)', fontWeight: '900', lineHeight: '1.1', color: 'var(--text-heading)', marginBottom: '1.25rem' }}>
              Discover Your{' '}
              <span style={{ background: 'linear-gradient(135deg, #6366f1, #8b5cf6, #ec4899)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', backgroundClip: 'text' }}>
                Ideal Career
              </span>
              {' '}with Adaptive AI Assessment
            </h1>

            <p style={{ fontSize: '1.1rem', color: 'var(--text-secondary)', lineHeight: '1.7', marginBottom: '2rem', maxWidth: '520px' }}>
              A production-grade 9-step psychometric pipeline — adaptive aptitude, situational scenarios, skill verification & LightGBM predictions across <strong>272 career labels</strong> for students from Class 7 to Professional Degrees.
            </p>

            <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap', marginBottom: '2.5rem' }}>
              <button onClick={handleStart} style={{ padding: '0.9rem 2rem', background: 'linear-gradient(135deg, #6366f1, #8b5cf6)', color: '#fff', border: 'none', borderRadius: '12px', fontWeight: '800', fontSize: '1rem', cursor: 'pointer', boxShadow: '0 8px 24px rgba(99,102,241,0.4)', transition: 'transform 0.2s, box-shadow 0.2s' }}
                onMouseEnter={e => { e.currentTarget.style.transform = 'translateY(-2px)'; e.currentTarget.style.boxShadow = '0 12px 32px rgba(99,102,241,0.5)'; }}
                onMouseLeave={e => { e.currentTarget.style.transform = 'translateY(0)'; e.currentTarget.style.boxShadow = '0 8px 24px rgba(99,102,241,0.4)'; }}
              >
                {user ? 'Continue Assessment →' : 'Start Free Assessment →'}
              </button>
              <a href="#pipeline" style={{ padding: '0.9rem 2rem', background: 'var(--bg-card)', color: 'var(--text-heading)', border: '1px solid var(--border-color)', borderRadius: '12px', fontWeight: '700', fontSize: '1rem', textDecoration: 'none', display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                Explore Pipeline ↓
              </a>
            </div>

            {/* Trust strip */}
            <div style={{ display: 'flex', gap: '1.5rem', flexWrap: 'wrap' }}>
              {['Class 7 → Professional Degree', '272 Careers Predicted', 'SHAP Explainability'].map((t, i) => (
                <div key={i} style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.83rem', color: 'var(--text-muted)', fontWeight: '600' }}>
                  <span style={{ color: '#10b981', fontWeight: '900' }}>✓</span> {t}
                </div>
              ))}
            </div>
          </div>

          {/* RIGHT: Interactive Live Preview Card */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0', minWidth: 0 }}>
            <div style={{ background: 'var(--bg-card)', borderRadius: '20px', border: '1px solid var(--border-color)', overflow: 'hidden', boxShadow: '0 32px 64px rgba(0,0,0,0.15)' }}>
              {/* Card header */}
              <div style={{ padding: '1rem 1.25rem', borderBottom: '1px solid var(--border-color)', display: 'flex', justifyContent: 'space-between', alignItems: 'center', background: 'var(--bg-card-subtle)' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <span style={{ display: 'inline-block', width: '8px', height: '8px', borderRadius: '50%', background: '#10b981', boxShadow: '0 0 0 3px rgba(16,185,129,0.2)' }} />
                  <span style={{ fontWeight: '800', fontSize: '0.82rem', color: 'var(--text-heading)', textTransform: 'uppercase', letterSpacing: '0.04em' }}>Live ML Preview</span>
                </div>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: '600' }}>Select candidate profile</span>
              </div>

              {/* Profile selector tabs */}
              <div style={{ display: 'flex', padding: '0.75rem', gap: '0.5rem', borderBottom: '1px solid var(--border-color)', flexWrap: 'wrap' }}>
                {Object.entries(PREVIEWS).map(([key, p]) => (
                  <button key={key} onClick={() => setActivePreview(key)} style={{ padding: '0.4rem 0.85rem', borderRadius: '8px', border: activePreview === key ? `1.5px solid ${p.color}` : '1px solid var(--border-color)', background: activePreview === key ? `${p.color}18` : 'transparent', color: activePreview === key ? p.color : 'var(--text-muted)', fontWeight: '700', fontSize: '0.78rem', cursor: 'pointer', transition: 'all 0.2s', whiteSpace: 'nowrap' }}>
                    {p.label}
                  </button>
                ))}
              </div>

              {/* Result */}
              <div style={{ padding: '1.25rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.85rem' }}>
                  <div>
                    <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.04em' }}>Top Career Match #1</div>
                    <div style={{ fontSize: '1.1rem', fontWeight: '900', color: 'var(--text-heading)', marginTop: '0.2rem' }}>{preview.top}</div>
                  </div>
                  <div style={{ background: preview.color, color: '#fff', padding: '0.35rem 0.75rem', borderRadius: '8px', fontWeight: '900', fontSize: '0.9rem' }}>
                    {preview.score}%
                  </div>
                </div>

                {/* XAI chips */}
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.35rem', marginBottom: '1rem' }}>
                  {preview.why.map((w, i) => (
                    <span key={i} style={{ background: 'rgba(16,185,129,0.12)', color: '#059669', padding: '0.2rem 0.55rem', borderRadius: '5px', fontSize: '0.72rem', fontWeight: '700' }}>
                      ✓ {w}
                    </span>
                  ))}
                </div>

                {/* Top 5 list */}
                <div style={{ borderTop: '1px solid var(--border-color)', paddingTop: '0.85rem' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.6rem' }}>
                    <span style={{ fontSize: '0.72rem', fontWeight: '700', color: 'var(--text-muted)', textTransform: 'uppercase' }}>Top 5 Ranked Careers</span>
                    <span style={{ fontSize: '0.72rem', fontWeight: '800', color: '#10b981' }}>Readiness: {preview.readiness}%</span>
                  </div>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '0.45rem' }}>
                    {preview.matches.map(([career, conf], i) => (
                      <div key={i} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <span style={{ fontSize: '0.82rem', fontWeight: i === 0 ? '800' : '600', color: i === 0 ? 'var(--text-heading)' : 'var(--text-secondary)' }}>#{i + 1} {career}</span>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                          <div style={{ width: '60px', height: '4px', background: 'var(--border-color)', borderRadius: '99px', overflow: 'hidden' }}>
                            <div style={{ height: '100%', width: `${conf}%`, background: preview.color, borderRadius: '99px' }} />
                          </div>
                          <span style={{ fontSize: '0.78rem', fontWeight: '800', color: preview.color, minWidth: '32px' }}>{conf}%</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <div style={{ marginTop: '1rem', padding: '0.6rem 0.85rem', background: 'var(--bg-card-subtle)', borderRadius: '8px', fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: '600', textAlign: 'center' }}>
                  ⚡ LightGBM · 35K dataset · 272 career labels · SHAP XAI
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ══════════════════════════════════════════════════════════════════
          2. STATS STRIP
      ══════════════════════════════════════════════════════════════════ */}
      <section ref={statsRef} style={{ padding: '4rem 1.5rem', background: 'var(--bg-card)', borderTop: '1px solid var(--border-color)', borderBottom: '1px solid var(--border-color)' }}>
        <div style={{ maxWidth: '1100px', margin: '0 auto', display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '2rem' }}>
          {STATS.map((s, i) => (
            <div key={i} style={{ textAlign: 'center' }}>
              <div style={{ fontSize: 'clamp(2rem, 5vw, 3rem)', fontWeight: '900', color: 'transparent', background: 'linear-gradient(135deg, #6366f1, #8b5cf6)', WebkitBackgroundClip: 'text', backgroundClip: 'text', transform: visibleStats ? 'translateY(0)' : 'translateY(20px)', opacity: visibleStats ? 1 : 0, transition: `all 0.6s ease ${i * 0.1}s` }}>
                {s.number}
              </div>
              <div style={{ fontSize: '0.9rem', color: 'var(--text-muted)', fontWeight: '600', marginTop: '0.35rem' }}>{s.label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* ══════════════════════════════════════════════════════════════════
          3. 9-STEP ASSESSMENT PIPELINE
      ══════════════════════════════════════════════════════════════════ */}
      <section id="pipeline" style={{ padding: '6rem 1.5rem', background: 'var(--bg-page)' }}>
        <div style={{ maxWidth: '1100px', margin: '0 auto' }}>
          <div style={{ textAlign: 'center', marginBottom: '3.5rem' }}>
            <div style={{ display: 'inline-block', background: 'var(--badge-bg)', color: 'var(--badge-text)', borderRadius: '999px', padding: '0.35rem 1rem', fontSize: '0.75rem', fontWeight: '800', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '1rem' }}>
              Assessment Pipeline
            </div>
            <h2 style={{ fontFamily: 'var(--heading-font)', fontSize: 'clamp(1.75rem, 4vw, 2.75rem)', fontWeight: '900', color: 'var(--text-heading)', marginBottom: '0.85rem', lineHeight: '1.2' }}>
              9-Stage AI Assessment{' '}
              <span style={{ background: 'linear-gradient(135deg, #6366f1, #ec4899)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', backgroundClip: 'text' }}>Pipeline</span>
            </h2>
            <p style={{ color: 'var(--text-muted)', fontSize: '1rem', maxWidth: '560px', margin: '0 auto' }}>
              Every student receives a different assessment — questions adapt to your education level, stream, and real-time performance.
            </p>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '1.25rem' }}>
            {PIPELINE.map((p, i) => (
              <div key={i} style={{ background: 'var(--bg-card)', borderRadius: '16px', border: '1px solid var(--border-color)', padding: '1.5rem', position: 'relative', overflow: 'hidden', transition: 'transform 0.25s, box-shadow 0.25s', cursor: 'default' }}
                onMouseEnter={e => { e.currentTarget.style.transform = 'translateY(-4px)'; e.currentTarget.style.boxShadow = '0 20px 40px rgba(0,0,0,0.12)'; }}
                onMouseLeave={e => { e.currentTarget.style.transform = 'translateY(0)'; e.currentTarget.style.boxShadow = 'none'; }}
              >
                <div style={{ position: 'absolute', top: '1rem', right: '1rem', fontSize: '0.7rem', fontWeight: '900', color: 'var(--text-muted)', letterSpacing: '0.06em' }}>{p.step}</div>
                <div style={{ fontSize: '1.75rem', marginBottom: '0.75rem' }}>{p.icon}</div>
                <h3 style={{ fontWeight: '800', color: 'var(--text-heading)', fontSize: '0.95rem', marginBottom: '0.5rem' }}>{p.title}</h3>
                <p style={{ color: 'var(--text-muted)', fontSize: '0.83rem', lineHeight: '1.6' }}>{p.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ══════════════════════════════════════════════════════════════════
          4. CAREER DOMAIN EXPLORER
      ══════════════════════════════════════════════════════════════════ */}
      <section style={{ padding: '6rem 1.5rem', background: 'var(--bg-card)', borderTop: '1px solid var(--border-color)' }}>
        <div style={{ maxWidth: '1100px', margin: '0 auto' }}>
          <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
            <div style={{ display: 'inline-block', background: 'var(--badge-bg)', color: 'var(--badge-text)', borderRadius: '999px', padding: '0.35rem 1rem', fontSize: '0.75rem', fontWeight: '800', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '1rem' }}>Career Domains</div>
            <h2 style={{ fontFamily: 'var(--heading-font)', fontSize: 'clamp(1.75rem, 4vw, 2.5rem)', fontWeight: '900', color: 'var(--text-heading)', marginBottom: '0.75rem' }}>
              Explore 272 Career Paths
            </h2>
            <p style={{ color: 'var(--text-muted)', fontSize: '1rem' }}>
              The ML model covers every major career domain from STEM to Law.
            </p>
          </div>

          {/* Domain tabs */}
          <div style={{ display: 'flex', gap: '0.6rem', flexWrap: 'wrap', justifyContent: 'center', marginBottom: '2rem' }}>
            {DOMAINS.map((d, i) => (
              <button key={i} onClick={() => setActiveDomain(i)} style={{ padding: '0.55rem 1.1rem', borderRadius: '10px', border: activeDomain === i ? `1.5px solid ${d.color}` : '1px solid var(--border-color)', background: activeDomain === i ? `${d.color}18` : 'var(--bg-page)', color: activeDomain === i ? d.color : 'var(--text-secondary)', fontWeight: '700', fontSize: '0.85rem', cursor: 'pointer', transition: 'all 0.2s', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                {d.icon} {d.title}
              </button>
            ))}
          </div>

          {/* Domain detail card */}
          <div style={{ background: 'var(--bg-page)', borderRadius: '20px', border: `1px solid ${domain.color}30`, padding: '2rem', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2.5rem', alignItems: 'start' }}>
            <div>
              <div style={{ fontSize: '2.5rem', marginBottom: '0.75rem' }}>{domain.icon}</div>
              <h3 style={{ fontSize: '1.4rem', fontWeight: '900', color: 'var(--text-heading)', marginBottom: '0.5rem' }}>{domain.title}</h3>
              <div style={{ display: 'flex', gap: '1.5rem', marginBottom: '1.5rem' }}>
                <div>
                  <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', fontWeight: '700', textTransform: 'uppercase' }}>Avg Salary</div>
                  <div style={{ fontWeight: '800', color: domain.color, fontSize: '1rem' }}>{domain.salary}</div>
                </div>
                <div>
                  <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', fontWeight: '700', textTransform: 'uppercase' }}>Growth</div>
                  <div style={{ fontWeight: '800', color: '#10b981', fontSize: '1rem' }}>{domain.growth} annually</div>
                </div>
              </div>
              <Link to="/register" style={{ display: 'inline-block', padding: '0.7rem 1.5rem', background: domain.color, color: '#fff', borderRadius: '10px', fontWeight: '700', fontSize: '0.9rem', textDecoration: 'none' }}>
                Explore Careers in {domain.title} →
              </Link>
            </div>
            <div>
              <div style={{ fontSize: '0.75rem', fontWeight: '700', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.04em', marginBottom: '0.85rem' }}>Sample Careers Predicted</div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.6rem' }}>
                {domain.careers.map((c, ci) => (
                  <div key={ci} style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', padding: '0.7rem 1rem', background: 'var(--bg-card)', borderRadius: '10px', border: '1px solid var(--border-color)' }}>
                    <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: domain.color, flexShrink: 0 }} />
                    <span style={{ fontWeight: '700', color: 'var(--text-heading)', fontSize: '0.9rem' }}>{c}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ══════════════════════════════════════════════════════════════════
          5. TESTIMONIALS
      ══════════════════════════════════════════════════════════════════ */}
      <section style={{ padding: '6rem 1.5rem', background: 'var(--bg-page)' }}>
        <div style={{ maxWidth: '1100px', margin: '0 auto' }}>
          <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
            <div style={{ display: 'inline-block', background: 'var(--badge-bg)', color: 'var(--badge-text)', borderRadius: '999px', padding: '0.35rem 1rem', fontSize: '0.75rem', fontWeight: '800', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '1rem' }}>Testimonials</div>
            <h2 style={{ fontFamily: 'var(--heading-font)', fontSize: 'clamp(1.75rem, 4vw, 2.5rem)', fontWeight: '900', color: 'var(--text-heading)' }}>
              What Students Say
            </h2>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.5rem' }}>
            {TESTIMONIALS.map((t, i) => (
              <div key={i} style={{ background: 'var(--bg-card)', borderRadius: '16px', border: '1px solid var(--border-color)', padding: '1.75rem', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                <div style={{ display: 'flex', gap: '0.25rem' }}>
                  {'★★★★★'.split('').map((s, si) => (
                    <span key={si} style={{ color: '#f59e0b', fontSize: '1rem' }}>{s}</span>
                  ))}
                </div>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: '1.7', fontStyle: 'italic' }}>"{t.text}"</p>
                <div>
                  <div style={{ fontWeight: '800', color: 'var(--text-heading)', fontSize: '0.9rem' }}>{t.name}</div>
                  <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginTop: '0.15rem' }}>{t.level}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ══════════════════════════════════════════════════════════════════
          6. FAQ
      ══════════════════════════════════════════════════════════════════ */}
      <section style={{ padding: '6rem 1.5rem', background: 'var(--bg-card)', borderTop: '1px solid var(--border-color)' }}>
        <div style={{ maxWidth: '820px', margin: '0 auto' }}>
          <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
            <div style={{ display: 'inline-block', background: 'var(--badge-bg)', color: 'var(--badge-text)', borderRadius: '999px', padding: '0.35rem 1rem', fontSize: '0.75rem', fontWeight: '800', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '1rem' }}>FAQ</div>
            <h2 style={{ fontFamily: 'var(--heading-font)', fontSize: 'clamp(1.75rem, 4vw, 2.5rem)', fontWeight: '900', color: 'var(--text-heading)' }}>Frequently Asked Questions</h2>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            {FAQS.map((faq, i) => {
              const isOpen = openFaq === i;
              return (
                <div key={i} style={{ background: 'var(--bg-page)', borderRadius: '14px', border: isOpen ? '1px solid rgba(99,102,241,0.4)' : '1px solid var(--border-color)', overflow: 'hidden', transition: 'border-color 0.2s' }}>
                  <button onClick={() => setOpenFaq(isOpen ? -1 : i)} style={{ width: '100%', display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '1.1rem 1.5rem', background: 'none', border: 'none', cursor: 'pointer', textAlign: 'left', gap: '1rem' }}>
                    <span style={{ fontWeight: '700', color: 'var(--text-heading)', fontSize: '0.95rem' }}>{faq.q}</span>
                    <span style={{ fontWeight: '900', fontSize: '1.1rem', color: isOpen ? '#6366f1' : 'var(--text-muted)', flexShrink: 0, transition: 'transform 0.2s', transform: isOpen ? 'rotate(45deg)' : 'rotate(0deg)' }}>+</span>
                  </button>
                  {isOpen && (
                    <div style={{ padding: '0 1.5rem 1.25rem', color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: '1.7' }}>
                      {faq.a}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* ══════════════════════════════════════════════════════════════════
          7. CTA BANNER
      ══════════════════════════════════════════════════════════════════ */}
      <section style={{ padding: '5rem 1.5rem', background: 'var(--bg-page)' }}>
        <div style={{ maxWidth: '820px', margin: '0 auto', textAlign: 'center', background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%)', borderRadius: '24px', padding: '4rem 2.5rem', position: 'relative', overflow: 'hidden' }}>
          {/* Decorative orbs */}
          <div style={{ position: 'absolute', top: '-40px', right: '-40px', width: '200px', height: '200px', borderRadius: '50%', background: 'rgba(255,255,255,0.06)' }} />
          <div style={{ position: 'absolute', bottom: '-30px', left: '-30px', width: '150px', height: '150px', borderRadius: '50%', background: 'rgba(255,255,255,0.06)' }} />
          <div style={{ position: 'relative', zIndex: 1 }}>
            <div style={{ display: 'inline-block', background: 'rgba(255,255,255,0.15)', color: '#fff', borderRadius: '999px', padding: '0.35rem 1rem', fontSize: '0.78rem', fontWeight: '800', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '1.25rem' }}>
              Start Today — It&apos;s Free
            </div>
            <h2 style={{ fontFamily: 'var(--heading-font)', color: '#fff', fontSize: 'clamp(1.75rem, 4vw, 2.75rem)', fontWeight: '900', marginBottom: '1rem', lineHeight: '1.2' }}>
              Ready to Discover Your Ideal Career?
            </h2>
            <p style={{ color: 'rgba(255,255,255,0.85)', fontSize: '1rem', marginBottom: '2.5rem', lineHeight: '1.7' }}>
              {user
                ? `Welcome back, ${user.full_name?.split(' ')[0]}! Continue your AI career assessment.`
                : 'Join thousands of students who found their path with AI-powered personalized career guidance.'}
            </p>
            <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', flexWrap: 'wrap' }}>
              <button onClick={handleStart} style={{ padding: '0.95rem 2.5rem', background: '#fff', color: '#6366f1', border: 'none', borderRadius: '12px', fontWeight: '900', fontSize: '1rem', cursor: 'pointer', boxShadow: '0 8px 24px rgba(0,0,0,0.2)', transition: 'transform 0.2s' }}
                onMouseEnter={e => e.currentTarget.style.transform = 'translateY(-2px)'}
                onMouseLeave={e => e.currentTarget.style.transform = 'translateY(0)'}
              >
                {user ? 'Continue Assessment →' : 'Start Free Assessment →'}
              </button>
              {!user && (
                <Link to="/login" style={{ padding: '0.95rem 2.5rem', background: 'rgba(255,255,255,0.15)', color: '#fff', borderRadius: '12px', fontWeight: '700', fontSize: '1rem', textDecoration: 'none', border: '1px solid rgba(255,255,255,0.3)' }}>
                  Sign In
                </Link>
              )}
            </div>
          </div>
        </div>
      </section>

      {/* ══════════════════════════════════════════════════════════════════
          8. FOOTER
      ══════════════════════════════════════════════════════════════════ */}
      <footer style={{ padding: '2.5rem 1.5rem', borderTop: '1px solid var(--border-color)', background: 'var(--bg-card)' }}>
        <div style={{ maxWidth: '1100px', margin: '0 auto', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
          <div style={{ fontWeight: '800', fontSize: '1.1rem', color: 'var(--text-heading)' }}>
            ✨ Career<span style={{ background: 'linear-gradient(135deg, #6366f1, #8b5cf6)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', backgroundClip: 'text' }}>AI</span>
          </div>
          <div style={{ display: 'flex', gap: '1.5rem', flexWrap: 'wrap' }}>
            {[['/', 'Home'], ['/assessment', 'Assessment'], ['/dashboard', 'Dashboard'], ['/admin-login', 'Admin']].map(([to, label]) => (
              <Link key={to} to={to} style={{ color: 'var(--text-muted)', textDecoration: 'none', fontSize: '0.85rem', fontWeight: '600', transition: 'color 0.2s' }}
                onMouseEnter={e => e.currentTarget.style.color = 'var(--color-primary-light)'}
                onMouseLeave={e => e.currentTarget.style.color = 'var(--text-muted)'}
              >
                {label}
              </Link>
            ))}
          </div>
          <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
            © 2026 AI Career Recommendation System
          </div>
        </div>
      </footer>

      <style>{`
        @keyframes pulse {
          0%, 100% { opacity: 1; transform: scale(1); }
          50% { opacity: 0.5; transform: scale(0.8); }
        }
        @media (max-width: 768px) {
          section > div[style*="gridTemplateColumns: 1fr 1fr"] {
            grid-template-columns: 1fr !important;
          }
        }
      `}</style>
    </div>
  );
};

export default Home;
