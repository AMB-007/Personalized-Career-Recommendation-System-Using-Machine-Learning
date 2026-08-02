const SKILL_BENCHMARKS = {
  'Engineering/Technology': [
    { skill: 'Coding & Algorithms', benchmark: 85, key: 'Coding_Score' },
    { skill: 'Problem Solving', benchmark: 80, key: 'Problem_Solving_Score' },
    { skill: 'Mathematics & Logic', benchmark: 75, key: 'Math_Score' },
    { skill: 'Domain Knowledge', benchmark: 80, key: 'Domain_Knowledge_Score' }
  ],
  'Business/Commerce': [
    { skill: 'Financial Analysis', benchmark: 80, key: 'Domain_Knowledge_Score' },
    { skill: 'Quantitative Aptitude', benchmark: 75, key: 'Math_Score' },
    { skill: 'Leadership & Teamwork', benchmark: 70, key: 'Leadership_Score' },
    { skill: 'Verbal Communication', benchmark: 75, key: 'English_Score' }
  ],
  'Healthcare/Medical': [
    { skill: 'Biological Sciences', benchmark: 85, key: 'Science_Score' },
    { skill: 'Investigative Reasoning', benchmark: 80, key: 'Investigative_Score' },
    { skill: 'Problem Solving', benchmark: 75, key: 'Problem_Solving_Score' },
    { skill: 'Communication Skills', benchmark: 80, key: 'English_Score' }
  ],
  'Creative Arts/Design': [
    { skill: 'Creativity & Aesthetics', benchmark: 85, key: 'Artistic_Score' },
    { skill: 'Verbal & Visual Ability', benchmark: 75, key: 'English_Score' },
    { skill: 'Domain Knowledge', benchmark: 70, key: 'Domain_Knowledge_Score' }
  ],
  'Default': [
    { skill: 'General Aptitude', benchmark: 75, key: 'General_Aptitude_Score' },
    { skill: 'Problem Solving', benchmark: 75, key: 'Problem_Solving_Score' },
    { skill: 'Verbal Ability', benchmark: 70, key: 'English_Score' }
  ]
};

const COURSE_RECOMMENDATIONS = {
  'Engineering/Technology': [
    { title: 'Harvard CS50: Introduction to Computer Science', provider: 'edX / Harvard', link: 'https://www.edx.org/course/introduction-computer-science-harvardx-cs50x' },
    { title: 'Data Structures & Algorithms Specialization', provider: 'Coursera / UC San Diego', link: 'https://www.coursera.org/specializations/data-structures-algorithms' },
    { title: 'NPTEL Computer Science Core Certification', provider: 'NPTEL India', link: 'https://nptel.ac.in/courses' }
  ],
  'Business/Commerce': [
    { title: 'Financial Markets & Accounting Fundamentals', provider: 'Coursera / Yale', link: 'https://www.coursera.org/learn/financial-markets-global' },
    { title: 'Business Analytics & Data Interpretation', provider: 'edX / Wharton', link: 'https://www.edx.org/' }
  ],
  'Healthcare/Medical': [
    { title: 'Anatomy & General Physiology Foundations', provider: 'Coursera / Michigan', link: 'https://www.coursera.org/' },
    { title: 'NEET / Medical Entrance Prep Roadmap', provider: 'Khan Academy', link: 'https://www.khanacademy.org/' }
  ],
  'Creative Arts/Design': [
    { title: 'UI/UX Design Specialization', provider: 'Coursera / CalArts', link: 'https://www.coursera.org/specializations/ui-ux-design' },
    { title: 'Graphic Design & Digital Media Basics', provider: 'Udemy / Adobe', link: 'https://www.udemy.com/' }
  ],
  'Default': [
    { title: 'Problem Solving & Critical Thinking Masterclass', provider: 'Khan Academy', link: 'https://www.khanacademy.org/' },
    { title: 'Effective Communication Skills for Students', provider: 'Coursera', link: 'https://www.coursera.org/' }
  ]
};

const SkillGapAnalysis = ({ career = '', profile = {}, verifiedScore = 80 }) => {
  // Select matching benchmarks or default fallback
  const matchedCategory = Object.keys(SKILL_BENCHMARKS).find((cat) => career.toLowerCase().includes(cat.toLowerCase().split('/')[0])) || 'Default';
  const benchmarks = SKILL_BENCHMARKS[matchedCategory] || SKILL_BENCHMARKS['Default'];
  const courses = COURSE_RECOMMENDATIONS[matchedCategory] || COURSE_RECOMMENDATIONS['Default'];

  return (
    <div className="skill-gap-container">
      <div className="gap-header">
        <h3>🎯 Skill Gap Analysis & Industry Benchmarks</h3>
        <p className="gap-desc">Comparing your verified scores against top industry benchmarks for <strong>{career}</strong></p>
      </div>

      <div className="benchmarks-list">
        {benchmarks.map((item, idx) => {
          const userVal = Math.round(profile[item.key] ?? profile[item.key.replace('_Score', '')] ?? verifiedScore);
          const gap = userVal - item.benchmark;
          const isExceeded = gap >= 0;

          return (
            <div key={idx} className="gap-card">
              <div className="gap-info">
                <span className="skill-name">{item.skill}</span>
                <span className={`gap-badge ${isExceeded ? 'green' : 'amber'}`}>
                  {isExceeded ? `✔ Met Benchmark (${userVal}%)` : `Gap: ${gap}% (${userVal}% / ${item.benchmark}%)`}
                </span>
              </div>

              <div className="bar-track">
                <div className="bar-fill user-fill" style={{ width: `${Math.min(100, userVal)}%` }}></div>
                <div className="benchmark-line" style={{ left: `${item.benchmark}%` }} title={`Target: ${item.benchmark}%`}></div>
              </div>
            </div>
          );
        })}
      </div>

      <div className="courses-section">
        <h4>📚 Recommended Courses & Certification Roadmap</h4>
        <div className="course-cards-grid">
          {courses.map((c, i) => (
            <a key={i} href={c.link} target="_blank" rel="noopener noreferrer" className="course-card-link">
              <div className="course-provider">{c.provider}</div>
              <div className="course-title">{c.title}</div>
              <span className="course-arrow">Explore Course ↗</span>
            </a>
          ))}
        </div>
      </div>
    </div>
  );
};

export default SkillGapAnalysis;
