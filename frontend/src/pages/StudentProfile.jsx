import { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

// ─── API base ────────────────────────────────────────────────────────────────
const API = 'http://127.0.0.1:5000';

// ─── Board subject maps ───────────────────────────────────────────────────────
const BOARD_SUBJECTS = {
  'Class 7': {
    'Kerala State Board': ['First Language (Malayalam/English)', 'Second Language (English)', 'Third Language', 'Social Science', 'Mathematics', 'General Science', 'ICT'],
    'CBSE': ['Language I', 'Language II', 'Mathematics', 'Science', 'Social Science', 'Artificial Intelligence'],
    'ICSE': ['English', 'Second Language', 'Mathematics', 'Science', 'Social Studies', 'Computer Applications'],
    'default': ['Language I', 'English', 'Mathematics', 'Science', 'Social Studies'],
  },
  'Class 8': {
    'Kerala State Board': ['First Language', 'Second Language (English)', 'Third Language', 'Social Science', 'Physics', 'Chemistry', 'Biology', 'Mathematics', 'ICT'],
    'CBSE': ['Language I', 'Language II', 'Mathematics', 'Science', 'Social Science', 'Information Technology'],
    'ICSE': ['English', 'Second Language', 'Mathematics', 'Physics', 'Chemistry', 'History & Civics', 'Computer Applications'],
    'default': ['Language I', 'English', 'Mathematics', 'Science', 'Social Studies', 'Computer Applications'],
  },
  'Class 9': {
    'Kerala State Board': ['First Language', 'Second Language (English)', 'Third Language', 'Social Science', 'Physics', 'Chemistry', 'Biology', 'Mathematics', 'ICT'],
    'CBSE': ['Language I', 'Language II', 'Mathematics', 'Science', 'Social Science', 'AI / Information Technology'],
    'ICSE': ['English', 'Second Language', 'Mathematics', 'Physics', 'Chemistry', 'Biology', 'History', 'Computer Applications'],
    'default': ['Language I', 'English', 'Mathematics', 'Science', 'Social Studies'],
  },
  'Class 10': {
    'Kerala State Board': ['First Language', 'Second Language (English)', 'Third Language', 'Social Science', 'Physics', 'Chemistry', 'Biology', 'Mathematics', 'ICT'],
    'CBSE': ['Language I', 'Language II', 'Mathematics', 'Science', 'Social Science', 'AI / Information Technology'],
    'ICSE': ['English', 'Second Language', 'Mathematics', 'Physics', 'Chemistry', 'Biology', 'History', 'Computer Science'],
    'default': ['Language I', 'English', 'Mathematics', 'Science', 'Social Studies'],
  },
};

const HS_STREAM_SUBJECTS = {
  'Science (PCM)':   ['Physics', 'Chemistry', 'Mathematics', 'Computer Science', 'English'],
  'Science (PCB)':   ['Physics', 'Chemistry', 'Biology', 'Mathematics', 'English'],
  'Science (PCMB)':  ['Physics', 'Chemistry', 'Mathematics', 'Biology', 'English'],
  'Commerce':        ['Accountancy', 'Business Studies', 'Economics', 'Mathematics / Applied Maths', 'English'],
  'Humanities/Arts': ['History', 'Geography', 'Political Science', 'Sociology', 'Psychology', 'Economics', 'English'],
  'Vocational':      ['Vocational Subject I', 'Vocational Subject II', 'English', 'Mathematics', 'General Studies'],
};

const SKILLS_MATRIX = [
  'Python', 'Java', 'C++', 'JavaScript', 'SQL & Databases', 'Machine Learning',
  'Data Structures & Algorithms', 'React.js / Frontend', 'Node.js / Backend',
  'Financial Accounting', 'Tally / ERP', 'UI/UX Design', 'Digital Marketing',
  'Public Speaking', 'Project Management', 'CAD & Mechanical Design',
  'Medical Biology / Anatomy', 'Copywriting & Content', 'Cyber Security',
  'Cloud Computing (AWS/Azure)', 'Android/iOS Development', 'Data Analysis (Excel/BI)',
];

const INTEREST_PAIRS = [
  { q: 'Which activity sounds more engaging?', a: { label: 'Building AI systems & robots', domain: 'Technology' }, b: { label: 'Creating business strategies', domain: 'Business' } },
  { q: 'Which sounds more fulfilling?',        a: { label: 'Teaching & mentoring students', domain: 'Education' }, b: { label: 'Diagnosing & treating patients', domain: 'Healthcare' } },
  { q: 'Which problem excites you most?',      a: { label: 'Solving complex algorithms', domain: 'Technology' }, b: { label: 'Designing creative campaigns', domain: 'Creative Arts' } },
  { q: 'Where would you work?',                a: { label: 'Research laboratory or tech company', domain: 'Research' }, b: { label: 'Courtroom or law firm', domain: 'Law' } },
  { q: 'Which career path interests you?',     a: { label: 'Engineering large-scale infrastructure', domain: 'Engineering' }, b: { label: 'Working in environment conservation', domain: 'Environment' } },
  { q: 'Which project would you prefer?',      a: { label: 'Building a data analytics platform', domain: 'Technology' }, b: { label: 'Launching a social enterprise', domain: 'Business' } },
  { q: 'Which role suits you better?',         a: { label: 'Medical researcher developing vaccines', domain: 'Healthcare' }, b: { label: 'Journalist writing investigative reports', domain: 'Creative Arts' } },
  { q: 'What would you enjoy more?',           a: { label: 'Designing a new sustainable city', domain: 'Engineering' }, b: { label: 'Teaching rural communities new skills', domain: 'Education' } },
];

const PSYCH_SCENARIOS = [
  {
    q: 'Your team is behind schedule on a critical project. What do you do?',
    options: [
      { label: 'Organize a triage meeting, reassign tasks based on capacity', traits: { Leadership: 15, Communication: 10 } },
      { label: 'Work extra hours yourself to bridge the gap', traits: { Persistence: 15, Resilience: 10 } },
      { label: 'Motivate the team and focus on morale', traits: { Teamwork: 15, Communication: 10 } },
      { label: 'Prioritize ruthlessly and cut non-essential tasks', traits: { Decision_Making: 15, Analytical_Thinking: 10 } },
    ]
  },
  {
    q: 'You encounter a completely new type of problem you have never seen before. You:',
    options: [
      { label: 'Research methodically using documentation and forums', traits: { Curiosity: 15, Self_Learning: 10 } },
      { label: 'Ask an experienced colleague for guidance', traits: { Teamwork: 10, Adaptability: 10 } },
      { label: 'Break it into smaller sub-problems and tackle each', traits: { Analytical_Thinking: 15, Problem_Solving: 10 } },
      { label: 'Try different solutions systematically until one works', traits: { Persistence: 15, Adaptability: 10 } },
    ]
  },
  {
    q: 'You are given complete freedom to choose a project topic. You choose:',
    options: [
      { label: 'The most technically challenging unsolved problem', traits: { Curiosity: 15, Analytical_Thinking: 10 } },
      { label: 'Something with clear measurable social impact', traits: { Leadership: 10, Communication: 10 } },
      { label: 'Something involving creative design and innovation', traits: { Creativity: 15, Self_Learning: 10 } },
      { label: 'Something with strong financial ROI potential', traits: { Decision_Making: 10, Confidence: 10 } },
    ]
  },
  {
    q: 'A critical bug is found 1 hour before a major product launch. You:',
    options: [
      { label: 'Stay calm, triage severity, and decide quickly', traits: { Stress_Management: 15, Decision_Making: 10 } },
      { label: 'Rally the entire team to fix it immediately', traits: { Leadership: 15, Teamwork: 10 } },
      { label: 'Apply a quick patch and document the full fix for later', traits: { Adaptability: 15, Problem_Solving: 10 } },
      { label: 'Escalate to management with a clear options briefing', traits: { Communication: 15, Confidence: 10 } },
    ]
  },
];

const StudentProfile = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [currentStep, setCurrentStep] = useState(1);
  const [maxUnlocked, setMaxUnlocked] = useState(1);

  // ── STEP 1: Education ────────────────────────────────────────────────────
  const [educationLevel, setEducationLevel] = useState('Undergraduate');
  const [board, setBoard] = useState('CBSE');
  const [stream, setStream] = useState('Science (PCM)');
  const [degree, setDegree] = useState('BTech');
  const [specialization, setSpecialization] = useState('Computer Science & Engineering');

  // ── STEP 2: Academic Marks ───────────────────────────────────────────────
  const [subjectMarks, setSubjectMarks] = useState({});
  const [ugPgSubjects, setUgPgSubjects] = useState([
    { id: 1, subject: 'Data Structures & Algorithms', semester: 'Semester 3', marks: 88, credits: 4, grade: 'A+' },
    { id: 2, subject: 'Database Management Systems',  semester: 'Semester 3', marks: 85, credits: 4, grade: 'A' },
  ]);
  const [overallCgpa, setOverallCgpa]     = useState(8.5);
  const [attendancePct, setAttendancePct] = useState(92);

  // ── STEP 3: Adaptive Aptitude Questions (from DB) ────────────────────────
  const [questions, setQuestions]           = useState([]);
  const [qLoading, setQLoading]             = useState(false);
  const [currentQIdx, setCurrentQIdx]       = useState(0);
  const [aptAnswers, setAptAnswers]         = useState({});
  const [aptScore, setAptScore]             = useState({ correct: 0, total: 0 });
  const [currentDifficulty, setCurrentDiff] = useState('Medium');

  // ── STEP 4: Psychometrics ────────────────────────────────────────────────
  const [psychoAnswers, setPsychoAnswers]   = useState({});
  const [psychoTraits, setPsychoTraits]     = useState({
    Leadership: 70, Teamwork: 75, Communication: 72, Creativity: 68,
    Resilience: 70, Curiosity: 72, Problem_Solving: 70, Adaptability: 70,
    Analytical_Thinking: 70, Confidence: 65, Decision_Making: 68,
    Time_Management: 70, Stress_Management: 65, Self_Learning: 72, Persistence: 70,
  });

  // ── STEP 5: Career Interest Profiler ────────────────────────────────────
  const [interestAnswers, setInterestAnswers] = useState({});
  const [interestScores, setInterestScores]   = useState({
    Technology: 50, Business: 40, Healthcare: 30, Education: 25,
    'Creative Arts': 35, Research: 45, Engineering: 50, Law: 20, Environment: 25,
  });

  // ── STEP 6: Skill Verification ───────────────────────────────────────────
  const [selectedSkills, setSelectedSkills]       = useState(['Python', 'SQL & Databases', 'Machine Learning']);
  const [skillQuestions, setSkillQuestions]       = useState({});
  const [skillAnswers, setSkillAnswers]           = useState({});
  const [verifiedScores, setVerifiedScores]       = useState({});
  const [activeSkillTest, setActiveSkillTest]     = useState(null);

  // ── STEP 7: Projects & Certifications ───────────────────────────────────
  const [projects, setProjects]         = useState([{ id: 1, title: '', description: '', technology: '', github_link: '' }]);
  const [certifications, setCerts]      = useState([]);
  const [certInput, setCertInput]       = useState({ name: '', provider: '', status: 'Completed' });
  const [portfolioLink, setPortfolio]   = useState('');

  // ── STEP 8: Career Preferences ──────────────────────────────────────────
  const [preferences, setPreferences]   = useState({
    target_industry: 'Technology & AI',
    company_type: 'MNC / Product Company',
    work_style: 'Hybrid',
    salary_range: '$80,000 - $120,000',
    preferred_country: 'India / USA',
  });

  // ─────────────────────────────────────────────────────────────────────────
  // FETCH QUESTIONS FROM BACKEND (dynamic, DB-driven)
  // ─────────────────────────────────────────────────────────────────────────
  const fetchQuestions = useCallback(async () => {
    setQLoading(true);
    try {
      const params = new URLSearchParams({
        education_level: educationLevel,
        board,
        stream,
        degree,
        category: 'Logical Reasoning,Numerical Reasoning,Algorithms & CS,Database Systems,Mathematics,Science Aptitude,Analytical Thinking',
        limit: 15,
      });
      const res = await axios.get(`${API}/api/questions?${params}`);
      if (res.data.questions && res.data.questions.length > 0) {
        setQuestions(res.data.questions);
      } else {
        // Fallback local questions if DB is empty
        setQuestions(getLocalFallbackQuestions(educationLevel));
      }
    } catch {
      setQuestions(getLocalFallbackQuestions(educationLevel));
    } finally {
      setQLoading(false);
    }
  }, [educationLevel, board, stream, degree]);

  const fetchSkillQuestions = useCallback(async (skill) => {
    if (skillQuestions[skill]) return;
    try {
      const res = await axios.get(`${API}/api/questions?category=Skill Verification&skill=${encodeURIComponent(skill)}&limit=5`);
      const qs  = res.data.questions && res.data.questions.length > 0
        ? res.data.questions
        : getSkillFallbackQuestions(skill);
      setSkillQuestions(prev => ({ ...prev, [skill]: qs }));
    } catch {
      setSkillQuestions(prev => ({ ...prev, [skill]: getSkillFallbackQuestions(skill) }));
    }
  }, [skillQuestions]);

  // ─────────────────────────────────────────────────────────────────────────
  // DERIVED HELPERS
  // ─────────────────────────────────────────────────────────────────────────
  const getBoardSubjects = () => {
    const level = educationLevel;
    if (['Class 7', 'Class 8', 'Class 9', 'Class 10'].includes(level)) {
      return (BOARD_SUBJECTS[level] || {})[board] || BOARD_SUBJECTS[level]?.default || [];
    }
    if (level === 'Higher Secondary') {
      return HS_STREAM_SUBJECTS[stream] || HS_STREAM_SUBJECTS['Science (PCM)'];
    }
    return [];
  };

  const isClassOrHS = ['Class 7', 'Class 8', 'Class 9', 'Class 10', 'Higher Secondary'].includes(educationLevel);
  const isUGPG      = ['Undergraduate', 'Postgraduate', 'Diploma', 'ITI', 'Professional Degree'].includes(educationLevel);

  // ─────────────────────────────────────────────────────────────────────────
  // STEP NAVIGATION
  // ─────────────────────────────────────────────────────────────────────────
  const goToStep = (step) => {
    setError('');
    if (step > maxUnlocked) setMaxUnlocked(step);
    setCurrentStep(step);
    window.scrollTo({ top: 0, behavior: 'smooth' });
    if (step === 3 && questions.length === 0) fetchQuestions();
    if (step === 6) {
      selectedSkills.forEach(sk => fetchSkillQuestions(sk));
    }
  };

  const validateStep1 = () => {
    if (!educationLevel) { setError('Please select your education level.'); return false; }
    return true;
  };

  const validateStep2 = () => {
    if (isUGPG) {
      for (const row of ugPgSubjects) {
        if (!row.subject.trim()) { setError('Please fill in all subject names.'); return false; }
        if (row.marks < 0 || row.marks > 100) { setError(`Invalid marks for "${row.subject}".`); return false; }
      }
    }
    setError('');
    return true;
  };

  // ─────────────────────────────────────────────────────────────────────────
  // APTITUDE ANSWER HANDLER (adaptive difficulty)
  // ─────────────────────────────────────────────────────────────────────────
  const handleAptAnswer = (qId, selected, correct) => {
    const isCorrect = selected === correct || selected?.startsWith(correct);
    setAptAnswers(prev => ({ ...prev, [qId]: { selected, isCorrect } }));
    setAptScore(prev => ({
      correct: prev.correct + (isCorrect ? 1 : 0),
      total:   prev.total + 1,
    }));
    if (isCorrect) {
      setCurrentDiff(d => d === 'Easy' ? 'Medium' : d === 'Medium' ? 'Hard' : 'Hard');
    } else {
      setCurrentDiff(d => d === 'Hard' ? 'Medium' : d === 'Medium' ? 'Easy' : 'Easy');
    }
    setTimeout(() => {
      if (currentQIdx < questions.length - 1) setCurrentQIdx(i => i + 1);
    }, 400);
  };

  // ─────────────────────────────────────────────────────────────────────────
  // PSYCHOMETRIC ANSWER HANDLER
  // ─────────────────────────────────────────────────────────────────────────
  const handlePsychoAnswer = (scenarioIdx, optionIdx) => {
    setPsychoAnswers(prev => ({ ...prev, [scenarioIdx]: optionIdx }));
    const traits = PSYCH_SCENARIOS[scenarioIdx].options[optionIdx].traits;
    setPsychoTraits(prev => {
      const updated = { ...prev };
      for (const [t, v] of Object.entries(traits)) {
        updated[t] = Math.min(100, (updated[t] || 70) + v);
      }
      return updated;
    });
  };

  // ─────────────────────────────────────────────────────────────────────────
  // INTEREST ANSWER HANDLER
  // ─────────────────────────────────────────────────────────────────────────
  const handleInterestChoice = (idx, chosen) => {
    setInterestAnswers(prev => ({ ...prev, [idx]: chosen }));
    setInterestScores(prev => ({
      ...prev,
      [chosen.domain]: Math.min(100, (prev[chosen.domain] || 50) + 15),
    }));
  };

  // ─────────────────────────────────────────────────────────────────────────
  // SKILL ANSWER HANDLER
  // ─────────────────────────────────────────────────────────────────────────
  const handleSkillAnswer = (skill, qId, selected, correct) => {
    const isCorrect = selected === correct || selected?.startsWith(correct);
    setSkillAnswers(prev => ({
      ...prev,
      [skill]: { ...(prev[skill] || {}), [qId]: { selected, isCorrect } },
    }));
    // Compute verified score
    const answers = { ...skillAnswers[skill], [qId]: { isCorrect } };
    const total   = Object.keys(answers).length;
    const correct_ = Object.values(answers).filter(a => a.isCorrect).length;
    const score   = total > 0 ? Math.round((correct_ / total) * 100) : 0;
    setVerifiedScores(prev => ({ ...prev, [skill]: score }));
  };

  // ─────────────────────────────────────────────────────────────────────────
  // UG/PG SUBJECT TABLE HANDLERS
  // ─────────────────────────────────────────────────────────────────────────
  const addSubjectRow = () => {
    const id = ugPgSubjects.length ? Math.max(...ugPgSubjects.map(r => r.id)) + 1 : 1;
    setUgPgSubjects(prev => [...prev, { id, subject: '', semester: 'Semester 1', marks: 80, credits: 3, grade: 'A' }]);
  };
  const removeSubjectRow = (id) => {
    if (ugPgSubjects.length <= 1) return;
    setUgPgSubjects(prev => prev.filter(r => r.id !== id));
  };
  const updateSubjectRow = (id, field, value) => {
    setUgPgSubjects(prev => prev.map(r => r.id === id ? { ...r, [field]: value } : r));
  };

  // ─────────────────────────────────────────────────────────────────────────
  // FINAL SUBMISSION
  // ─────────────────────────────────────────────────────────────────────────
  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setError('');

    const token = localStorage.getItem('authToken') || localStorage.getItem('token');

    const payload = {
      education_level: educationLevel,
      board,
      stream,
      degree,
      specialization,
      gender: 'Male',
      cgpa:   overallCgpa,
      attendance: attendancePct,
      semester_marks: isClassOrHS
        ? Object.values(subjectMarks).reduce((a, b) => a + b, 0) / (Object.keys(subjectMarks).length || 1)
        : ugPgSubjects.reduce((a, r) => a + r.marks, 0) / (ugPgSubjects.length || 1),
      project_score: Math.min(projects.filter(p => p.title.trim()).length * 25, 100),
      internships_count: 0,
      aptitude_answers: Object.fromEntries(
        Object.entries(aptAnswers).map(([k, v]) => [k, { is_correct: v.isCorrect }])
      ),
      psychometric_traits: psychoTraits,
      interest_scores: interestScores,
      skill_scores: verifiedScores,
      certifications: certifications.map(c => c.name),
      projects: projects.filter(p => p.title.trim()),
    };

    try {
      const headers = token ? { Authorization: `Bearer ${token}` } : {};
      const res = await axios.post(`${API}/api/assessment/submit`, payload, { headers });
      const data = res.data;

      localStorage.setItem('top5Careers',            JSON.stringify(data.top5_careers || []));
      localStorage.setItem('finalRecommendedCareer', (data.top5_careers?.[0]?.career) || 'Software Developer');
      localStorage.setItem('recommendedCareer',      (data.top5_careers?.[0]?.career) || 'Software Developer');
      localStorage.setItem('readinessScore',         data.readiness_score || 0);
      localStorage.setItem('featureScores',          JSON.stringify(data.feature_scores || {}));
      localStorage.setItem('xaiAttributions',        JSON.stringify(data.xai_attributions || []));
      localStorage.setItem('studentProfile',         JSON.stringify(payload));

      navigate('/dashboard');
    } catch (err) {
      console.error(err);
      setError('Submission failed. Check your connection and try again.');
    } finally {
      setSubmitting(false);
    }
  };

  // ─────────────────────────────────────────────────────────────────────────
  // RENDER
  // ─────────────────────────────────────────────────────────────────────────
  const steps = [
    { id: 1, label: '1. Education' },
    { id: 2, label: '2. Academics' },
    { id: 3, label: '3. Aptitude' },
    { id: 4, label: '4. Psychometrics' },
    { id: 5, label: '5. Interests' },
    { id: 6, label: '6. Skills' },
    { id: 7, label: '7. Projects & Certs' },
    { id: 8, label: '8. Preferences' },
    { id: 9, label: '9. Review & Submit' },
  ];

  return (
    <div className="profile-container" style={{ maxWidth: '1100px', margin: '0 auto' }}>
      {/* HEADER */}
      <div className="profile-header" style={{ marginBottom: '2rem' }}>
        <span className="badge" style={{ padding: '0.35rem 0.85rem', background: 'var(--badge-bg)', color: 'var(--badge-text)', borderRadius: 'var(--radius-full)', fontSize: '0.8rem', fontWeight: '700' }}>
          ADAPTIVE CAREER ASSESSMENT ENGINE
        </span>
        <h2 style={{ fontSize: '2rem', fontWeight: '800', marginTop: '0.4rem', color: 'var(--text-heading)' }}>
          AI Career Assessment Wizard
        </h2>
        <p style={{ fontSize: '0.95rem', color: 'var(--text-muted)' }}>
          Adaptive 9-step pipeline · Questions from database · ML-powered predictions · 272 career labels
        </p>
      </div>

      {/* STEPPER */}
      <div style={{ display: 'flex', gap: '0.4rem', overflowX: 'auto', paddingBottom: '0.75rem', marginBottom: '2rem' }}>
        {steps.map((s) => {
          const unlocked = s.id <= maxUnlocked;
          const active   = s.id === currentStep;
          const done     = s.id < currentStep;
          return (
            <button
              key={s.id}
              type="button"
              onClick={() => unlocked && goToStep(s.id)}
              disabled={!unlocked}
              style={{
                padding: '0.6rem 0.9rem',
                borderRadius: 'var(--radius-lg)',
                border: '1px solid var(--border-color)',
                background: active ? 'var(--primary-gradient)' : done ? 'rgba(16,185,129,0.15)' : unlocked ? 'var(--bg-card)' : 'var(--bg-card-subtle)',
                color:  active ? '#fff' : done ? 'var(--color-emerald)' : unlocked ? 'var(--text-heading)' : 'var(--text-muted)',
                fontWeight: '700',
                fontSize:   '0.8rem',
                whiteSpace: 'nowrap',
                cursor:     unlocked ? 'pointer' : 'not-allowed',
              }}
            >
              {done && !active ? '✓ ' : ''}{s.label}{!unlocked ? ' 🔒' : ''}
            </button>
          );
        })}
      </div>

      {error && (
        <div style={{ background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.3)', color: '#ef4444', padding: '0.85rem 1.25rem', borderRadius: 'var(--radius-lg)', marginBottom: '1.5rem', fontSize: '0.9rem' }}>
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit}>

        {/* ═══════════════════════════════════════════════════════════════ */}
        {/* STEP 1: EDUCATION LEVEL & STREAM */}
        {/* ═══════════════════════════════════════════════════════════════ */}
        {currentStep === 1 && (
          <div className="wizard-card" style={{ background: 'var(--bg-card)', padding: '2rem', borderRadius: 'var(--radius-2xl)', border: '1px solid var(--border-color)' }}>
            <h3 style={{ fontSize: '1.35rem', fontWeight: '800', color: 'var(--text-heading)' }}>🎓 Step 1: Education Level &amp; Specialization</h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginTop: '0.25rem' }}>Question bank and adaptive difficulty will be configured for your specific level.</p>

            <div className="form-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '1.25rem', marginTop: '1.5rem' }}>
              <div className="form-group" style={{ gridColumn: '1 / -1' }}>
                <label>Select Education Level *</label>
                <select value={educationLevel} onChange={e => setEducationLevel(e.target.value)} style={{ fontSize: '1rem' }}>
                  <option value="Class 7">Class 7 (Middle School)</option>
                  <option value="Class 8">Class 8 (Middle School)</option>
                  <option value="Class 9">Class 9 (High School)</option>
                  <option value="Class 10">Class 10 (SSC / SSLC)</option>
                  <option value="Higher Secondary">Higher Secondary (Class 11-12)</option>
                  <option value="Diploma">Diploma (Engineering / Pharmacy)</option>
                  <option value="ITI">ITI (Industrial Training)</option>
                  <option value="Undergraduate">Undergraduate (BTech, BCA, BSc, BCom, BBA, MBBS)</option>
                  <option value="Postgraduate">Postgraduate (MTech, MCA, MSc, MBA)</option>
                  <option value="Professional Degree">Professional Degree (CA, LLB, Architecture)</option>
                </select>
              </div>

              {['Class 7','Class 8','Class 9','Class 10'].includes(educationLevel) && (
                <div className="form-group">
                  <label>Education Board *</label>
                  <select value={board} onChange={e => setBoard(e.target.value)}>
                    <option value="Kerala State Board">Kerala State Board</option>
                    <option value="CBSE">CBSE (Central Board)</option>
                    <option value="ICSE">ICSE / CISCE</option>
                    <option value="NIOS">NIOS (Open Schooling)</option>
                    <option value="Others">Other State Board</option>
                  </select>
                </div>
              )}

              {educationLevel === 'Higher Secondary' && (
                <>
                  <div className="form-group">
                    <label>Education Board *</label>
                    <select value={board} onChange={e => setBoard(e.target.value)}>
                      <option value="Kerala HSE">Kerala Higher Secondary Board</option>
                      <option value="CBSE">CBSE Class 12</option>
                      <option value="ISC">ISC Class 12</option>
                      <option value="Others">Other Board</option>
                    </select>
                  </div>
                  <div className="form-group">
                    <label>Select Stream *</label>
                    <select value={stream} onChange={e => setStream(e.target.value)}>
                      <option value="Science (PCM)">Science — PCM (Physics, Chemistry, Maths)</option>
                      <option value="Science (PCB)">Science — PCB (Physics, Chemistry, Biology)</option>
                      <option value="Science (PCMB)">Science — PCMB (All four)</option>
                      <option value="Commerce">Commerce</option>
                      <option value="Humanities/Arts">Humanities / Arts</option>
                      <option value="Vocational">Vocational Stream</option>
                    </select>
                  </div>
                </>
              )}

              {['Undergraduate','Postgraduate','Diploma','ITI','Professional Degree'].includes(educationLevel) && (
                <>
                  <div className="form-group">
                    <label>Degree / Program *</label>
                    <select value={degree} onChange={e => setDegree(e.target.value)}>
                      <option value="BTech">B.Tech / B.E.</option>
                      <option value="BCA">BCA (Computer Applications)</option>
                      <option value="BSc">B.Sc (Science)</option>
                      <option value="BCom">B.Com (Commerce)</option>
                      <option value="BBA">BBA (Business Administration)</option>
                      <option value="BA">B.A. (Arts / Humanities)</option>
                      <option value="MBBS">MBBS (Medical)</option>
                      <option value="LLB">LLB (Law)</option>
                      <option value="BArch">B.Arch (Architecture)</option>
                      <option value="MTech">M.Tech / M.E.</option>
                      <option value="MCA">MCA (Computer Applications)</option>
                      <option value="MSc">M.Sc</option>
                      <option value="MBA">MBA (Business Administration)</option>
                      <option value="Diploma">Diploma</option>
                      <option value="ITI">ITI Certificate</option>
                      <option value="CA">CA (Chartered Accountancy)</option>
                    </select>
                  </div>
                  <div className="form-group">
                    <label>Specialization / Branch *</label>
                    <input type="text" value={specialization} onChange={e => setSpecialization(e.target.value)} placeholder="e.g. Computer Science, AI, Finance, Mechanical" />
                  </div>
                </>
              )}
            </div>

            <div style={{ marginTop: '2rem', display: 'flex', justifyContent: 'flex-end' }}>
              <button type="button" className="primary-btn" onClick={() => { if (validateStep1()) goToStep(2); }}>
                Proceed to Academic Record &rarr;
              </button>
            </div>
          </div>
        )}

        {/* ═══════════════════════════════════════════════════════════════ */}
        {/* STEP 2: ACADEMIC PERFORMANCE */}
        {/* ═══════════════════════════════════════════════════════════════ */}
        {currentStep === 2 && (
          <div className="wizard-card" style={{ background: 'var(--bg-card)', padding: '2rem', borderRadius: 'var(--radius-2xl)', border: '1px solid var(--border-color)' }}>
            <h3 style={{ fontSize: '1.35rem', fontWeight: '800', color: 'var(--text-heading)' }}>📊 Step 2: Academic Performance Record</h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginTop: '0.25rem' }}>
              {isClassOrHS ? `Official ${board} subjects for ${educationLevel}.` : 'Dynamic subject builder — add unlimited rows with marks, credits, and grades.'}
            </p>

            {/* CLASS / HS BOARD MARKS */}
            {isClassOrHS && getBoardSubjects().length > 0 && (
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1.25rem', marginTop: '1.5rem' }}>
                {getBoardSubjects().map(sub => (
                  <div key={sub} className="form-group">
                    <label>{sub} (%)</label>
                    <input
                      type="number" min="0" max="100"
                      value={subjectMarks[sub] ?? 80}
                      onChange={e => setSubjectMarks(prev => ({ ...prev, [sub]: parseInt(e.target.value) || 0 }))}
                    />
                  </div>
                ))}
                <div className="form-group">
                  <label>Overall Attendance (%)</label>
                  <input type="number" min="0" max="100" value={attendancePct} onChange={e => setAttendancePct(parseInt(e.target.value) || 0)} />
                </div>
              </div>
            )}

            {/* UG / PG DYNAMIC TABLE */}
            {isUGPG && (
              <div style={{ marginTop: '1.5rem' }}>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1.5rem' }}>
                  <div className="form-group">
                    <label>Cumulative CGPA (0–10)</label>
                    <input type="number" step="0.01" min="0" max="10" value={overallCgpa} onChange={e => setOverallCgpa(parseFloat(e.target.value) || 0)} />
                  </div>
                  <div className="form-group">
                    <label>Overall Attendance (%)</label>
                    <input type="number" min="0" max="100" value={attendancePct} onChange={e => setAttendancePct(parseInt(e.target.value) || 0)} />
                  </div>
                </div>

                <div style={{ overflowX: 'auto' }}>
                  <table className="admin-table" style={{ width: '100%', borderCollapse: 'collapse' }}>
                    <thead>
                      <tr style={{ background: 'var(--bg-card-subtle)', textAlign: 'left' }}>
                        {['Semester','Subject Name','Marks (%)','Credits','Grade',''].map(h => (
                          <th key={h} style={{ padding: '0.75rem', fontSize: '0.85rem', fontWeight: '700', color: 'var(--text-muted)' }}>{h}</th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {ugPgSubjects.map(row => (
                        <tr key={row.id} style={{ borderBottom: '1px solid var(--border-color)' }}>
                          <td style={{ padding: '0.5rem' }}>
                            <select value={row.semester} onChange={e => updateSubjectRow(row.id, 'semester', e.target.value)} style={{ padding: '0.45rem' }}>
                              {[1,2,3,4,5,6,7,8].map(s => <option key={s} value={`Semester ${s}`}>Sem {s}</option>)}
                            </select>
                          </td>
                          <td style={{ padding: '0.5rem' }}>
                            <input type="text" value={row.subject} onChange={e => updateSubjectRow(row.id, 'subject', e.target.value)} placeholder="Subject name" style={{ width: '100%', padding: '0.45rem' }} />
                          </td>
                          <td style={{ padding: '0.5rem' }}>
                            <input type="number" min="0" max="100" value={row.marks} onChange={e => updateSubjectRow(row.id, 'marks', parseInt(e.target.value) || 0)} style={{ width: '70px', padding: '0.45rem' }} />
                          </td>
                          <td style={{ padding: '0.5rem' }}>
                            <input type="number" min="1" max="10" value={row.credits} onChange={e => updateSubjectRow(row.id, 'credits', parseInt(e.target.value) || 1)} style={{ width: '60px', padding: '0.45rem' }} />
                          </td>
                          <td style={{ padding: '0.5rem' }}>
                            <select value={row.grade} onChange={e => updateSubjectRow(row.id, 'grade', e.target.value)} style={{ padding: '0.45rem' }}>
                              {['S','A+','A','B+','B','C','D','F'].map(g => <option key={g}>{g}</option>)}
                            </select>
                          </td>
                          <td style={{ padding: '0.5rem' }}>
                            <button type="button" onClick={() => removeSubjectRow(row.id)} style={{ padding: '0.35rem 0.65rem', background: 'rgba(239,68,68,0.1)', color: '#ef4444', border: '1px solid rgba(239,68,68,0.3)', borderRadius: 'var(--radius-sm)', cursor: 'pointer', fontSize: '0.8rem' }}>
                              Remove
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
                <button type="button" onClick={addSubjectRow} className="primary-btn" style={{ marginTop: '1rem', padding: '0.55rem 1.25rem', fontSize: '0.85rem' }}>
                  + Add Subject Row
                </button>
              </div>
            )}

            <div style={{ marginTop: '2rem', display: 'flex', justifyContent: 'space-between' }}>
              <button type="button" className="secondary-btn" onClick={() => goToStep(1)}>&larr; Back</button>
              <button type="button" className="primary-btn" onClick={() => { if (validateStep2()) goToStep(3); }}>Proceed to Adaptive Aptitude &rarr;</button>
            </div>
          </div>
        )}

        {/* ═══════════════════════════════════════════════════════════════ */}
        {/* STEP 3: ADAPTIVE APTITUDE (DB-DRIVEN) */}
        {/* ═══════════════════════════════════════════════════════════════ */}
        {currentStep === 3 && (
          <div className="wizard-card" style={{ background: 'var(--bg-card)', padding: '2rem', borderRadius: 'var(--radius-2xl)', border: '1px solid var(--border-color)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.75rem' }}>
              <div>
                <h3 style={{ fontSize: '1.35rem', fontWeight: '800', color: 'var(--text-heading)' }}>🧩 Step 3: Adaptive Question Bank Engine</h3>
                <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginTop: '0.25rem' }}>
                  Fetched from database for <strong>{educationLevel}</strong>. Difficulty adapts to your performance.
                </p>
              </div>
              <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center', flexWrap: 'wrap' }}>
                <span style={{ padding: '0.35rem 0.75rem', background: 'rgba(16,185,129,0.15)', color: 'var(--color-emerald)', borderRadius: 'var(--radius-full)', fontWeight: '800', fontSize: '0.85rem' }}>
                  Difficulty: {currentDifficulty}
                </span>
                <span style={{ padding: '0.35rem 0.75rem', background: 'var(--badge-bg)', color: 'var(--badge-text)', borderRadius: 'var(--radius-full)', fontWeight: '700', fontSize: '0.85rem' }}>
                  Score: {aptScore.correct}/{aptScore.total}
                </span>
              </div>
            </div>

            {qLoading ? (
              <div style={{ textAlign: 'center', padding: '3rem', color: 'var(--text-muted)' }}>
                <div style={{ fontSize: '2rem', marginBottom: '0.75rem' }}>⏳</div>
                <p>Fetching questions from database...</p>
              </div>
            ) : questions.length > 0 && currentQIdx < questions.length ? (
              <div style={{ background: 'var(--bg-card-subtle)', padding: '1.5rem', borderRadius: 'var(--radius-xl)', border: '1px solid var(--border-color)', marginTop: '1.5rem' }}>
                <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '0.85rem', flexWrap: 'wrap' }}>
                  <span style={{ padding: '0.25rem 0.65rem', background: 'var(--badge-bg)', color: 'var(--badge-text)', borderRadius: 'var(--radius-full)', fontSize: '0.75rem', fontWeight: '700' }}>
                    {questions[currentQIdx].category}
                  </span>
                  <span style={{ padding: '0.25rem 0.65rem', background: 'var(--bg-card)', color: 'var(--text-muted)', borderRadius: 'var(--radius-full)', fontSize: '0.75rem', fontWeight: '700', border: '1px solid var(--border-color)' }}>
                    Q{currentQIdx + 1} of {questions.length}
                  </span>
                </div>

                <h4 style={{ color: 'var(--text-heading)', fontSize: '1.05rem', fontWeight: '700', lineHeight: '1.5' }}>
                  {questions[currentQIdx].question_text}
                </h4>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.65rem', marginTop: '1.25rem' }}>
                  {['option_a','option_b','option_c','option_d'].map((opt, i) => {
                    const optText   = questions[currentQIdx][opt];
                    const qId       = questions[currentQIdx].id;
                    const isAnswered= aptAnswers[qId];
                    const isSelected= aptAnswers[qId]?.selected === optText;
                    const isCorrect = aptAnswers[qId]?.isCorrect && isSelected;
                    if (!optText) return null;
                    return (
                      <button
                        key={i} type="button"
                        onClick={() => !isAnswered && handleAptAnswer(qId, optText, questions[currentQIdx].correct_answer)}
                        style={{
                          textAlign: 'left', padding: '0.85rem 1.15rem',
                          borderRadius: 'var(--radius-lg)',
                          border: isSelected ? `2px solid ${isCorrect ? '#10b981' : '#ef4444'}` : '1px solid var(--border-color)',
                          background: isSelected ? (isCorrect ? 'rgba(16,185,129,0.1)' : 'rgba(239,68,68,0.1)') : 'var(--bg-card)',
                          color: 'var(--text-primary)', fontWeight: '600', fontSize: '0.9rem',
                          cursor: isAnswered ? 'default' : 'pointer',
                        }}
                      >
                        {optText}
                      </button>
                    );
                  })}
                </div>

                {aptAnswers[questions[currentQIdx].id] && currentQIdx < questions.length - 1 && (
                  <button type="button" className="primary-btn" onClick={() => setCurrentQIdx(i => i + 1)} style={{ marginTop: '1.25rem', padding: '0.65rem 1.5rem', fontSize: '0.9rem' }}>
                    Next Question &rarr;
                  </button>
                )}
              </div>
            ) : (
              <div style={{ textAlign: 'center', padding: '2.5rem', color: 'var(--text-muted)' }}>
                <div style={{ fontSize: '2.5rem', marginBottom: '0.5rem' }}>🎉</div>
                <p style={{ fontWeight: '700', color: 'var(--text-heading)' }}>All {questions.length} questions completed!</p>
                <p>Score: {aptScore.correct} correct out of {aptScore.total} answered</p>
              </div>
            )}

            <div style={{ marginTop: '2rem', display: 'flex', justifyContent: 'space-between' }}>
              <button type="button" className="secondary-btn" onClick={() => goToStep(2)}>&larr; Back</button>
              <button type="button" className="primary-btn" onClick={() => goToStep(4)}>Proceed to Psychometrics &rarr;</button>
            </div>
          </div>
        )}

        {/* ═══════════════════════════════════════════════════════════════ */}
        {/* STEP 4: SITUATIONAL PSYCHOMETRICS */}
        {/* ═══════════════════════════════════════════════════════════════ */}
        {currentStep === 4 && (
          <div className="wizard-card" style={{ background: 'var(--bg-card)', padding: '2rem', borderRadius: 'var(--radius-2xl)', border: '1px solid var(--border-color)' }}>
            <h3 style={{ fontSize: '1.35rem', fontWeight: '800', color: 'var(--text-heading)' }}>🧠 Step 4: Situational Psychometric Assessment</h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginTop: '0.25rem' }}>
              Indirect evaluation using realistic workplace scenarios. Measures Leadership, Teamwork, Resilience, Curiosity.
            </p>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', marginTop: '1.5rem' }}>
              {PSYCH_SCENARIOS.map((scenario, sIdx) => (
                <div key={sIdx} style={{ background: 'var(--bg-card-subtle)', padding: '1.5rem', borderRadius: 'var(--radius-xl)', border: '1px solid var(--border-color)' }}>
                  <p style={{ fontWeight: '700', color: 'var(--text-heading)', marginBottom: '1rem', fontSize: '0.95rem' }}>
                    Scenario {sIdx + 1}: {scenario.q}
                  </p>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '0.6rem' }}>
                    {scenario.options.map((opt, oIdx) => {
                      const selected = psychoAnswers[sIdx] === oIdx;
                      return (
                        <button
                          key={oIdx} type="button"
                          onClick={() => handlePsychoAnswer(sIdx, oIdx)}
                          style={{
                            textAlign: 'left', padding: '0.8rem 1.1rem',
                            borderRadius: 'var(--radius-lg)',
                            border: selected ? '2px solid var(--color-primary-light)' : '1px solid var(--border-color)',
                            background: selected ? 'var(--primary-gradient)' : 'var(--bg-card)',
                            color: selected ? '#fff' : 'var(--text-primary)',
                            fontWeight: selected ? '700' : '500', fontSize: '0.88rem', cursor: 'pointer',
                          }}
                        >
                          {opt.label}
                        </button>
                      );
                    })}
                  </div>
                </div>
              ))}
            </div>

            <div style={{ marginTop: '2rem', display: 'flex', justifyContent: 'space-between' }}>
              <button type="button" className="secondary-btn" onClick={() => goToStep(3)}>&larr; Back</button>
              <button type="button" className="primary-btn" onClick={() => goToStep(5)}>Proceed to Career Interests &rarr;</button>
            </div>
          </div>
        )}

        {/* ═══════════════════════════════════════════════════════════════ */}
        {/* STEP 5: CAREER INTEREST PROFILER */}
        {/* ═══════════════════════════════════════════════════════════════ */}
        {currentStep === 5 && (
          <div className="wizard-card" style={{ background: 'var(--bg-card)', padding: '2rem', borderRadius: 'var(--radius-2xl)', border: '1px solid var(--border-color)' }}>
            <h3 style={{ fontSize: '1.35rem', fontWeight: '800', color: 'var(--text-heading)' }}>🎯 Step 5: Activity-Choice Career Interest Profiler</h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginTop: '0.25rem' }}>
              Choose the activity that resonates most. Each choice maps to career domain interest scores.
            </p>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem', marginTop: '1.5rem' }}>
              {INTEREST_PAIRS.map((pair, idx) => (
                <div key={idx} style={{ background: 'var(--bg-card-subtle)', padding: '1.25rem', borderRadius: 'var(--radius-xl)', border: '1px solid var(--border-color)' }}>
                  <p style={{ fontWeight: '700', color: 'var(--text-heading)', marginBottom: '0.85rem', fontSize: '0.9rem' }}>{pair.q}</p>
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem' }}>
                    {[pair.a, pair.b].map((choice, ci) => {
                      const sel = interestAnswers[idx]?.label === choice.label;
                      return (
                        <button
                          key={ci} type="button"
                          onClick={() => handleInterestChoice(idx, choice)}
                          style={{
                            padding: '0.85rem 1rem', borderRadius: 'var(--radius-lg)', textAlign: 'left',
                            border: sel ? '2px solid var(--color-primary-light)' : '1px solid var(--border-color)',
                            background: sel ? 'var(--primary-gradient)' : 'var(--bg-card)',
                            color: sel ? '#fff' : 'var(--text-primary)',
                            fontWeight: sel ? '700' : '500', fontSize: '0.88rem', cursor: 'pointer',
                          }}
                        >
                          {choice.label}
                          <span style={{ display: 'block', fontSize: '0.72rem', marginTop: '0.2rem', opacity: 0.75 }}>{choice.domain}</span>
                        </button>
                      );
                    })}
                  </div>
                </div>
              ))}
            </div>

            <div style={{ marginTop: '2rem', display: 'flex', justifyContent: 'space-between' }}>
              <button type="button" className="secondary-btn" onClick={() => goToStep(4)}>&larr; Back</button>
              <button type="button" className="primary-btn" onClick={() => goToStep(6)}>Proceed to Skill Verification &rarr;</button>
            </div>
          </div>
        )}

        {/* ═══════════════════════════════════════════════════════════════ */}
        {/* STEP 6: SELECTIVE SKILL VERIFICATION */}
        {/* ═══════════════════════════════════════════════════════════════ */}
        {currentStep === 6 && (
          <div className="wizard-card" style={{ background: 'var(--bg-card)', padding: '2rem', borderRadius: 'var(--radius-2xl)', border: '1px solid var(--border-color)' }}>
            <h3 style={{ fontSize: '1.35rem', fontWeight: '800', color: 'var(--text-heading)' }}>🔬 Step 6: Selective Skill Verification Engine</h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginTop: '0.25rem' }}>
              Select your skills. Verification tests are generated <strong>ONLY for selected skills</strong>.
            </p>

            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.6rem', marginTop: '1.25rem', marginBottom: '1.5rem' }}>
              {SKILLS_MATRIX.map(sk => {
                const sel = selectedSkills.includes(sk);
                return (
                  <button
                    key={sk} type="button"
                    onClick={() => {
                      const newSel = sel ? selectedSkills.filter(s => s !== sk) : [...selectedSkills, sk];
                      setSelectedSkills(newSel);
                      if (!sel) fetchSkillQuestions(sk);
                    }}
                    style={{
                      padding: '0.5rem 1rem', borderRadius: 'var(--radius-full)',
                      border: '1px solid var(--border-color)',
                      background: sel ? 'var(--badge-bg)' : 'var(--bg-card-subtle)',
                      color: sel ? 'var(--badge-text)' : 'var(--text-secondary)',
                      fontWeight: '700', fontSize: '0.85rem', cursor: 'pointer',
                    }}
                  >
                    {sel ? '✔ ' : '+ '}{sk}
                  </button>
                );
              })}
            </div>

            {selectedSkills.length === 0 && (
              <p style={{ color: 'var(--text-muted)', fontStyle: 'italic' }}>Select at least one skill to generate a verification test.</p>
            )}

            {selectedSkills.map(sk => (
              <div key={sk} style={{ marginBottom: '1.5rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
                  <h4 style={{ color: 'var(--text-heading)', fontWeight: '800' }}>{sk} Verification Diagnostic</h4>
                  {verifiedScores[sk] !== undefined && (
                    <span style={{ fontWeight: '900', color: verifiedScores[sk] >= 60 ? 'var(--color-emerald)' : '#ef4444', fontSize: '1.1rem' }}>
                      {verifiedScores[sk]}% {verifiedScores[sk] >= 60 ? 'Verified' : 'Practice More'}
                    </span>
                  )}
                </div>

                {skillQuestions[sk] ? (
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                    {skillQuestions[sk].map((q, qi) => (
                      <div key={qi} style={{ background: 'var(--bg-card-subtle)', padding: '1.25rem', borderRadius: 'var(--radius-xl)', border: '1px solid var(--border-color)' }}>
                        <p style={{ fontWeight: '700', color: 'var(--text-heading)', fontSize: '0.9rem', marginBottom: '0.75rem' }}>Q{qi + 1}. {q.question_text}</p>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                          {['option_a','option_b','option_c','option_d'].map((opt, oi) => {
                            const optTxt = q[opt];
                            const answered = skillAnswers[sk]?.[q.id];
                            const isSel  = skillAnswers[sk]?.[q.id]?.selected === optTxt;
                            if (!optTxt) return null;
                            return (
                              <button
                                key={oi} type="button"
                                onClick={() => !answered && handleSkillAnswer(sk, q.id, optTxt, q.correct_answer)}
                                style={{
                                  textAlign: 'left', padding: '0.6rem 0.85rem', borderRadius: 'var(--radius-lg)',
                                  border: isSel ? '2px solid var(--color-primary-light)' : '1px solid var(--border-color)',
                                  background: isSel ? 'var(--primary-gradient)' : 'var(--bg-card)',
                                  color: isSel ? '#fff' : 'var(--text-primary)',
                                  fontWeight: isSel ? '700' : '500', fontSize: '0.85rem', cursor: answered ? 'default' : 'pointer',
                                }}
                              >
                                {optTxt}
                              </button>
                            );
                          })}
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', fontStyle: 'italic' }}>Loading questions...</p>
                )}
              </div>
            ))}

            <div style={{ marginTop: '2rem', display: 'flex', justifyContent: 'space-between' }}>
              <button type="button" className="secondary-btn" onClick={() => goToStep(5)}>&larr; Back</button>
              <button type="button" className="primary-btn" onClick={() => goToStep(7)}>Proceed to Projects &amp; Certifications &rarr;</button>
            </div>
          </div>
        )}

        {/* ═══════════════════════════════════════════════════════════════ */}
        {/* STEP 7: PROJECTS & CERTIFICATIONS */}
        {/* ═══════════════════════════════════════════════════════════════ */}
        {currentStep === 7 && (
          <div className="wizard-card" style={{ background: 'var(--bg-card)', padding: '2rem', borderRadius: 'var(--radius-2xl)', border: '1px solid var(--border-color)' }}>
            <h3 style={{ fontSize: '1.35rem', fontWeight: '800', color: 'var(--text-heading)' }}>🏆 Step 7: Projects, Portfolio &amp; Certifications</h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginTop: '0.25rem' }}>Academic projects, GitHub links, and recognized certifications boost your score.</p>

            <h4 style={{ color: 'var(--text-heading)', fontWeight: '700', marginTop: '1.5rem' }}>Projects</h4>
            {projects.map((proj, pi) => (
              <div key={proj.id} style={{ background: 'var(--bg-card-subtle)', padding: '1.25rem', borderRadius: 'var(--radius-xl)', border: '1px solid var(--border-color)', marginTop: '0.85rem' }}>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem' }}>
                  <div className="form-group">
                    <label>Project Title</label>
                    <input type="text" value={proj.title} onChange={e => setProjects(p => p.map(r => r.id === proj.id ? { ...r, title: e.target.value } : r))} placeholder="e.g. AI Career Platform" />
                  </div>
                  <div className="form-group">
                    <label>Technology Stack</label>
                    <input type="text" value={proj.technology} onChange={e => setProjects(p => p.map(r => r.id === proj.id ? { ...r, technology: e.target.value } : r))} placeholder="e.g. React, Python, MySQL" />
                  </div>
                  <div className="form-group">
                    <label>GitHub / Demo Link</label>
                    <input type="text" value={proj.github_link} onChange={e => setProjects(p => p.map(r => r.id === proj.id ? { ...r, github_link: e.target.value } : r))} placeholder="https://github.com/..." />
                  </div>
                </div>
              </div>
            ))}
            <button type="button" className="primary-btn" style={{ marginTop: '0.85rem', padding: '0.5rem 1rem', fontSize: '0.85rem' }}
              onClick={() => setProjects(p => [...p, { id: Date.now(), title: '', description: '', technology: '', github_link: '' }])}>
              + Add Project
            </button>

            <h4 style={{ color: 'var(--text-heading)', fontWeight: '700', marginTop: '2rem' }}>Certifications</h4>
            <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap', marginTop: '0.75rem', marginBottom: '0.75rem' }}>
              {certifications.map((c, ci) => (
                <span key={ci} style={{ padding: '0.4rem 0.85rem', background: 'rgba(16,185,129,0.15)', color: 'var(--color-emerald)', borderRadius: 'var(--radius-full)', fontWeight: '700', fontSize: '0.82rem', display: 'flex', gap: '0.4rem', alignItems: 'center' }}>
                  {c.name} ({c.status})
                  <button type="button" onClick={() => setCerts(prev => prev.filter((_, i) => i !== ci))} style={{ background: 'none', border: 'none', color: '#ef4444', cursor: 'pointer', fontWeight: '900', padding: 0 }}>×</button>
                </span>
              ))}
            </div>
            <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
              <input type="text" placeholder="Certificate name" value={certInput.name} onChange={e => setCertInput(c => ({ ...c, name: e.target.value }))} style={{ flex: 1, minWidth: '180px' }} />
              <input type="text" placeholder="Provider (e.g. Google, AWS)" value={certInput.provider} onChange={e => setCertInput(c => ({ ...c, provider: e.target.value }))} style={{ flex: 1, minWidth: '150px' }} />
              <select value={certInput.status} onChange={e => setCertInput(c => ({ ...c, status: e.target.value }))} style={{ padding: '0.65rem' }}>
                <option>Completed</option>
                <option>In Progress</option>
                <option>Interested</option>
              </select>
              <button type="button" className="primary-btn" style={{ padding: '0.5rem 1rem', fontSize: '0.85rem' }}
                onClick={() => { if (certInput.name.trim()) { setCerts(prev => [...prev, { ...certInput }]); setCertInput({ name: '', provider: '', status: 'Completed' }); } }}>
                Add
              </button>
            </div>

            <div style={{ marginTop: '2rem', display: 'flex', justifyContent: 'space-between' }}>
              <button type="button" className="secondary-btn" onClick={() => goToStep(6)}>&larr; Back</button>
              <button type="button" className="primary-btn" onClick={() => goToStep(8)}>Proceed to Preferences &rarr;</button>
            </div>
          </div>
        )}

        {/* ═══════════════════════════════════════════════════════════════ */}
        {/* STEP 8: CAREER PREFERENCES */}
        {/* ═══════════════════════════════════════════════════════════════ */}
        {currentStep === 8 && (
          <div className="wizard-card" style={{ background: 'var(--bg-card)', padding: '2rem', borderRadius: 'var(--radius-2xl)', border: '1px solid var(--border-color)' }}>
            <h3 style={{ fontSize: '1.35rem', fontWeight: '800', color: 'var(--text-heading)' }}>🎯 Step 8: Career Preferences &amp; Values</h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginTop: '0.25rem' }}>Tell us what matters most in your career path.</p>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1.25rem', marginTop: '1.5rem' }}>
              <div className="form-group">
                <label>Preferred Work Style</label>
                <select value={preferences.work_style} onChange={e => setPreferences(p => ({ ...p, work_style: e.target.value }))}>
                  <option>Hybrid</option>
                  <option>Remote</option>
                  <option>On-Site Office</option>
                  <option>Field Work</option>
                </select>
              </div>
              <div className="form-group">
                <label>Target Industry</label>
                <input type="text" value={preferences.target_industry} onChange={e => setPreferences(p => ({ ...p, target_industry: e.target.value }))} />
              </div>
              <div className="form-group">
                <label>Company Type</label>
                <select value={preferences.company_type} onChange={e => setPreferences(p => ({ ...p, company_type: e.target.value }))}>
                  <option>MNC / Product Company</option>
                  <option>Government / PSU</option>
                  <option>Startup</option>
                  <option>Research / Academia</option>
                  <option>NGO / Social Enterprise</option>
                  <option>Self-Employed / Freelance</option>
                </select>
              </div>
              <div className="form-group">
                <label>Salary Expectation</label>
                <select value={preferences.salary_range} onChange={e => setPreferences(p => ({ ...p, salary_range: e.target.value }))}>
                  <option>Under $30,000</option>
                  <option>$30,000 - $60,000</option>
                  <option>$60,000 - $100,000</option>
                  <option>$80,000 - $120,000</option>
                  <option>$120,000 - $180,000</option>
                  <option>$180,000+</option>
                </select>
              </div>
            </div>

            <div style={{ marginTop: '2rem', display: 'flex', justifyContent: 'space-between' }}>
              <button type="button" className="secondary-btn" onClick={() => goToStep(7)}>&larr; Back</button>
              <button type="button" className="primary-btn" onClick={() => goToStep(9)}>Review &amp; Submit &rarr;</button>
            </div>
          </div>
        )}

        {/* ═══════════════════════════════════════════════════════════════ */}
        {/* STEP 9: PRE-SUBMISSION REVIEW */}
        {/* ═══════════════════════════════════════════════════════════════ */}
        {currentStep === 9 && (
          <div className="wizard-card" style={{ background: 'var(--bg-card)', padding: '2rem', borderRadius: 'var(--radius-2xl)', border: '1px solid var(--border-color)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem', marginBottom: '1.5rem' }}>
              <div>
                <h3 style={{ fontSize: '1.4rem', fontWeight: '800', color: 'var(--text-heading)' }}>📋 Step 9: Assessment Review &amp; ML Submission</h3>
                <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginTop: '0.2rem' }}>Review all inputs before the AI model predicts your top 5 career matches.</p>
              </div>
              <span style={{ padding: '0.35rem 0.85rem', background: 'rgba(16,185,129,0.15)', color: 'var(--color-emerald)', borderRadius: 'var(--radius-full)', fontWeight: '800', fontSize: '0.85rem' }}>
                READY FOR ML
              </span>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '1.25rem' }}>
              {[
                { icon: '🎓', title: 'Education Profile', body: `${educationLevel} · ${stream || degree} · ${specialization}`, sub: `Board: ${board}` },
                { icon: '📊', title: 'Aptitude Score', body: `${aptScore.correct} correct / ${aptScore.total} answered`, sub: `Logical Score: ${aptScore.total > 0 ? Math.round((aptScore.correct/aptScore.total)*100) : 'N/A'}%` },
                { icon: '🧠', title: 'Psychometric Traits', body: `Leadership: ${psychoTraits.Leadership}% | Teamwork: ${psychoTraits.Teamwork}%`, sub: `Curiosity: ${psychoTraits.Curiosity}% | Resilience: ${psychoTraits.Resilience}%` },
                { icon: '🔬', title: 'Selected Skills', body: selectedSkills.join(', ') || 'None selected', sub: `Verified scores computed` },
                { icon: '🏆', title: 'Projects & Certs', body: `${projects.filter(p => p.title.trim()).length} project(s) · ${certifications.length} certification(s)`, sub: portfolioLink || 'No portfolio link' },
                { icon: '🎯', title: 'Career Preferences', body: `${preferences.work_style} · ${preferences.target_industry}`, sub: `${preferences.company_type} · ${preferences.salary_range}` },
              ].map((card, ci) => (
                <div key={ci} style={{ background: 'var(--bg-card-subtle)', padding: '1.25rem', borderRadius: 'var(--radius-xl)', border: '1px solid var(--border-color)' }}>
                  <div style={{ fontSize: '1.4rem', marginBottom: '0.35rem' }}>{card.icon}</div>
                  <strong style={{ color: 'var(--color-primary-light)', fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: '0.04em' }}>{card.title}</strong>
                  <p style={{ fontWeight: '700', color: 'var(--text-heading)', marginTop: '0.3rem', fontSize: '0.9rem', lineHeight: '1.4' }}>{card.body}</p>
                  <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>{card.sub}</span>
                </div>
              ))}
            </div>

            <div style={{ marginTop: '2.5rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
              <button type="button" className="secondary-btn" onClick={() => goToStep(8)}>&larr; Back to Edit</button>
              <button type="submit" className="primary-btn submit-btn" disabled={submitting}
                style={{ padding: '0.95rem 2.5rem', fontWeight: '900', fontSize: '1rem', letterSpacing: '0.02em' }}>
                {submitting ? '⏳ AI Model Processing...' : '🚀 Execute AI Assessment & View Career Report'}
              </button>
            </div>
          </div>
        )}

      </form>
    </div>
  );
};

// ─────────────────────────────────────────────────────────────────────────────
// FALLBACK QUESTIONS (when DB is empty)
// ─────────────────────────────────────────────────────────────────────────────
function getLocalFallbackQuestions(level) {
  const maps = {
    'Class 7': [
      { id: 'f7_1', question_text: 'If 3 cats catch 3 mice in 3 minutes, how many cats catch 100 mice in 100 minutes?', category: 'Logical Reasoning', difficulty: 'Easy', option_a: 'A) 100 cats', option_b: 'B) 3 cats', option_c: 'C) 33 cats', option_d: 'D) 1 cat', correct_answer: 'B' },
      { id: 'f7_2', question_text: 'What is 15% of 200?', category: 'Numerical Reasoning', difficulty: 'Easy', option_a: 'A) 20', option_b: 'B) 25', option_c: 'C) 30', option_d: 'D) 35', correct_answer: 'C' },
    ],
    'Class 8': [
      { id: 'f8_1', question_text: 'Complete: 2, 6, 12, 20, 30, ?', category: 'Logical Reasoning', difficulty: 'Medium', option_a: 'A) 38', option_b: 'B) 40', option_c: 'C) 42', option_d: 'D) 44', correct_answer: 'C' },
    ],
    'Class 9': [
      { id: 'f9_1', question_text: 'What is the speed of light in vacuum?', category: 'Science Aptitude', difficulty: 'Easy', option_a: 'A) 3×10⁸ m/s', option_b: 'B) 3×10⁶ m/s', option_c: 'C) 150,000 km/s', option_d: 'D) 300,000 m/s', correct_answer: 'A' },
    ],
    'Class 10': [
      { id: 'f10_1', question_text: 'A train 200m long passes a pole in 10s. What is the speed?', category: 'Numerical Reasoning', difficulty: 'Medium', option_a: 'A) 10 m/s', option_b: 'B) 20 m/s', option_c: 'C) 25 m/s', option_d: 'D) 15 m/s', correct_answer: 'B' },
    ],
    'Higher Secondary': [
      { id: 'fhs_1', question_text: 'If log₂(x) = 5, what is x?', category: 'Mathematics', difficulty: 'Medium', option_a: 'A) 10', option_b: 'B) 25', option_c: 'C) 32', option_d: 'D) 64', correct_answer: 'C' },
    ],
    'Undergraduate': [
      { id: 'fug_1', question_text: 'Worst-case time complexity of QuickSort?', category: 'Algorithms', difficulty: 'Hard', option_a: 'A) O(N log N)', option_b: 'B) O(N²)', option_c: 'C) O(N)', option_d: 'D) O(log N)', correct_answer: 'B' },
      { id: 'fug_2', question_text: 'Which SQL command permanently removes a table?', category: 'Database Systems', difficulty: 'Medium', option_a: 'A) DELETE', option_b: 'B) TRUNCATE', option_c: 'C) DROP', option_d: 'D) REMOVE', correct_answer: 'C' },
      { id: 'fug_3', question_text: 'What does TCP stand for?', category: 'Computer Networks', difficulty: 'Easy', option_a: 'A) Transfer Control', option_b: 'B) Transmission Control Protocol', option_c: 'C) Transport Code Protocol', option_d: 'D) Technical Control', correct_answer: 'B' },
    ],
    'Postgraduate': [
      { id: 'fpg_1', question_text: 'Which loss function is standard for multi-class classification in neural networks?', category: 'Machine Learning', difficulty: 'Hard', option_a: 'A) MSE', option_b: 'B) Categorical Cross-Entropy', option_c: 'C) Binary Cross-Entropy', option_d: 'D) Hinge Loss', correct_answer: 'B' },
    ],
  };
  return maps[level] || maps['Undergraduate'];
}

function getSkillFallbackQuestions(skill) {
  const banks = {
    'Python': [
      { id: `py_1`, question_text: "What is the output of print(type([]))?", category: 'Skill Verification', option_a: "A) <class 'tuple'>", option_b: "B) <class 'list'>", option_c: "C) <class 'dict'>", option_d: "D) <class 'set'>", correct_answer: 'B' },
      { id: `py_2`, question_text: "Which keyword defines a generator function?", category: 'Skill Verification', option_a: "A) return", option_b: "B) yield", option_c: "C) generate", option_d: "D) async", correct_answer: 'B' },
    ],
    'SQL & Databases': [
      { id: `sql_1`, question_text: "Which SQL clause filters groups after GROUP BY?", category: 'Skill Verification', option_a: "A) WHERE", option_b: "B) HAVING", option_c: "C) FILTER", option_d: "D) SELECT", correct_answer: 'B' },
    ],
    'Machine Learning': [
      { id: `ml_1`, question_text: "What does overfitting mean?", category: 'Skill Verification', option_a: "A) High bias", option_b: "B) Memorizes training data, poor generalization", option_c: "C) Performs well on all data", option_d: "D) Fast training", correct_answer: 'B' },
    ],
    'Financial Accounting': [
      { id: `fa_1`, question_text: "Balance sheet equation is?", category: 'Skill Verification', option_a: "A) Revenue = Expense", option_b: "B) Assets = Liabilities + Equity", option_c: "C) Cash = Assets", option_d: "D) None", correct_answer: 'B' },
    ],
  };
  return banks[skill] || [
    { id: `gen_${skill}_1`, question_text: `Which best describes a core concept in ${skill}?`, category: 'Skill Verification', option_a: "A) Structured problem solving", option_b: "B) Domain-specific methodologies", option_c: "C) Industry-standard practices", option_d: "D) All of the above", correct_answer: 'D' },
  ];
}

export default StudentProfile;