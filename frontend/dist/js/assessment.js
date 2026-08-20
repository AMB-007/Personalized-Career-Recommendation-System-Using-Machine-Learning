/* assessment.js — Multi-step AI Career Assessment */


const SKILL_QUIZ_BANK = {
  'Python': [
    { q:'What does `list(range(5))` return?', opts:['[1,2,3,4,5]','[0,1,2,3,4]','[0,1,2,3,4,5]','Error'], ans:1 },
    { q:'What keyword is used to define a function in Python?', opts:['function','def','fun','define'], ans:1 },
    { q:'What is the output of `print(type([]))` in Python?', opts:["<class 'dict'>","<class 'tuple'>","<class 'list'>","<class 'array'>"], ans:2 },
  ],
  'Java': [
    { q:'Which keyword is used to create an object in Java?', opts:['create','new','object','make'], ans:1 },
    { q:'What is the correct way to declare a constant in Java?', opts:['const int X=5','static final int X=5','final int X=5','const final int X=5'], ans:1 },
    { q:'What does JVM stand for?', opts:['Java Variable Machine','Java Virtual Machine','Java Visual Machine','Java Value Machine'], ans:1 },
  ],
  'C++': [
    { q:'Which operator is used for dynamic memory allocation in C++?', opts:['malloc','alloc','new','create'], ans:2 },
    { q:'What is the correct syntax to declare a pointer?', opts:['int &p','int *p','int p*','pointer int p'], ans:1 },
    { q:'What does `cout` do in C++?', opts:['Takes input','Outputs to console','Creates a loop','Declares a variable'], ans:1 },
  ],
  'JavaScript': [
    { q:'Which method adds an element to the end of an array?', opts:['push()','pop()','shift()','append()'], ans:0 },
    { q:'What does `===` check in JavaScript?', opts:['Assignment','Value only','Value and type','Reference'], ans:2 },
    { q:'Which keyword declares a block-scoped variable?', opts:['var','let','const','both let and const'], ans:3 },
  ],
  'SQL & Databases': [
    { q:'Which SQL command retrieves data from a table?', opts:['INSERT','UPDATE','SELECT','DELETE'], ans:2 },
    { q:'What does `GROUP BY` do in SQL?', opts:['Sorts rows','Filters rows','Groups rows by column values','Joins tables'], ans:2 },
    { q:'Which key uniquely identifies each row in a table?', opts:['Foreign Key','Unique Key','Primary Key','Index Key'], ans:2 },
  ],
  'Machine Learning': [
    { q:'What type of learning uses labeled training data?', opts:['Unsupervised','Reinforcement','Supervised','Transfer'], ans:2 },
    { q:'Which algorithm is used for classification tasks?', opts:['K-Means','Linear Regression','Logistic Regression','PCA'], ans:2 },
    { q:'What does overfitting mean?', opts:['Model performs well on test data','Model too simple','Model memorizes training data and fails on new data','Model not trained enough'], ans:2 },
  ],
  'Data Structures & Algorithms': [
    { q:'Which data structure follows LIFO (Last In First Out)?', opts:['Queue','Stack','Linked List','Tree'], ans:1 },
    { q:'What is the time complexity of Binary Search?', opts:['O(N)','O(N^2)','O(log N)','O(1)'], ans:2 },
    { q:'Which sorting algorithm has best average-case complexity?', opts:['Bubble Sort','Selection Sort','Merge Sort','Insertion Sort'], ans:2 },
  ],
  'React.js / Frontend': [
    { q:'What is JSX in React?', opts:['A JavaScript framework','A CSS preprocessor','A syntax extension for JavaScript','A database query language'], ans:2 },
    { q:'Which hook is used to manage state in a React functional component?', opts:['useEffect','useState','useContext','useReducer'], ans:1 },
    { q:'What does `props` allow in React?', opts:['State management','Passing data from parent to child component','Styling components','Routing between pages'], ans:1 },
  ],
  'Node.js / Backend': [
    { q:'What is Node.js built on?', opts:['JVM','V8 JavaScript Engine','Python interpreter','Ruby runtime'], ans:1 },
    { q:'Which module is used to create an HTTP server in Node.js?', opts:['fs','path','http','net'], ans:2 },
    { q:'What does `npm` stand for?', opts:['Node Package Manager','Node Process Manager','New Package Module','Node Program Manager'], ans:0 },
  ],
  'Financial Accounting': [
    { q:'What does the Balance Sheet show?', opts:['Profit and Loss','Cash flows','Assets, liabilities and equity at a point in time','Revenue and expenses'], ans:2 },
    { q:'Which accounting principle states revenue should be recognized when earned?', opts:['Matching Principle','Accrual Principle','Going Concern','Conservatism'], ans:1 },
    { q:'What is depreciation?', opts:['Increase in asset value','Allocation of asset cost over useful life','Cash payment for assets','Amortization of liabilities'], ans:1 },
  ],
  'Tally / ERP': [
    { q:'What type of software is Tally?', opts:['Spreadsheet software','Accounting and ERP software','Database software','Word processing software'], ans:1 },
    { q:'In Tally, what is a "Ledger"?', opts:['A group of companies','An account record for transactions','A financial report','A user profile'], ans:1 },
    { q:'What does GST stand for in Tally?', opts:['General Sales Tax','Goods and Services Tax','Government Service Tax','Gross Sales Tax'], ans:1 },
  ],
  'UI/UX Design': [
    { q:'What does UX stand for?', opts:['User Experience','User Export','Unique Experience','Unified Extension'], ans:0 },
    { q:'What is a wireframe in UI/UX?', opts:['A color palette','A low-fidelity visual layout of an interface','A finished product design','A coding framework'], ans:1 },
    { q:'Which principle states that similar elements should look similar?', opts:['Contrast','Proximity','Consistency','Alignment'], ans:2 },
  ],
  'Digital Marketing': [
    { q:'What does SEO stand for?', opts:['Social Engine Optimization','Search Engine Optimization','Social Engagement Outreach','Search Event Organizer'], ans:1 },
    { q:'What is CTR in digital marketing?', opts:['Click-Through Rate','Customer Transaction Record','Content Transfer Rate','Campaign Tracking Result'], ans:0 },
    { q:'Which platform is best known for B2B professional marketing?', opts:['Instagram','TikTok','LinkedIn','Snapchat'], ans:2 },
  ],
  'Public Speaking': [
    { q:'What is the primary purpose of using pauses in a speech?', opts:['To forget what to say next','To emphasize key points and let audience absorb information','To check your notes','To avoid eye contact'], ans:1 },
    { q:'What is extemporaneous speaking?', opts:['Reading from a script','Memorized word-for-word speech','Prepared but spoken in natural conversational style','Completely impromptu speech'], ans:2 },
    { q:'What does "vocal variety" mean in public speaking?', opts:['Using multiple languages','Changing pitch, pace, and volume for emphasis','Speaking louder than normal','Using technical vocabulary'], ans:1 },
  ],
  'Project Management': [
    { q:'What does a Gantt chart show?', opts:['Budget allocation','Team hierarchy','Project timeline and task schedule','Risk assessment'], ans:2 },
    { q:'In Agile, what is a "Sprint"?', opts:['A quick meeting','A fixed time period to complete a set of tasks','A type of bug fix','A release to production'], ans:1 },
    { q:'What does SMART goal stand for?', opts:['Simple, Measurable, Achievable, Relevant, Time-bound','Specific, Measurable, Achievable, Relevant, Time-bound','Specific, Manageable, Accurate, Realistic, Time-bound','Simple, Manageable, Achievable, Real, Timed'], ans:1 },
  ],
  'CAD & Mechanical Design': [
    { q:'What does CAD stand for?', opts:['Computer Aided Drafting','Computer Aided Design','Computer Application Drawing','Computerized Assembly Design'], ans:1 },
    { q:'Which software is most commonly used for 3D mechanical design?', opts:['Photoshop','SolidWorks / AutoCAD','Excel','MATLAB'], ans:1 },
    { q:'What is a "tolerance" in mechanical design?', opts:['The load a part can handle','Acceptable variation in a part dimension','The material strength','The surface finish'], ans:1 },
  ],
  'Medical Biology / Anatomy': [
    { q:'Which organ pumps blood throughout the body?', opts:['Lungs','Kidneys','Heart','Liver'], ans:2 },
    { q:'What does DNA stand for?', opts:['Deoxyribonucleic Acid','Deoxyribose Nucleotide Arrangement','Double Nucleic Acid','Dinucleotide Acid'], ans:0 },
    { q:'What is the function of red blood cells?', opts:['Fight infection','Carry oxygen','Produce hormones','Filter blood'], ans:1 },
  ],
  'Copywriting & Content': [
    { q:'What is a "CTA" in content writing?', opts:['Content Theme Assignment','Call To Action','Creative Text Arrangement','Copy Tone Adjustment'], ans:1 },
    { q:'What is the primary goal of a headline in copywriting?', opts:['To summarize the whole article','To attract attention and make reader want to read more','To explain the product features','To include keywords for SEO'], ans:1 },
    { q:'What does AIDA stand for in marketing copywriting?', opts:['Attention, Interest, Decision, Action','Awareness, Interest, Desire, Action','Attention, Inform, Decide, Acquire','Attract, Influence, Drive, Achieve'], ans:1 },
  ],
  'Cyber Security': [
    { q:'What does phishing mean?', opts:['Network scanning','Deceiving users into revealing sensitive information','Encrypting data','Blocking network access'], ans:1 },
    { q:'What is a firewall?', opts:['A type of virus','Hardware or software that monitors and controls network traffic','An encryption algorithm','A password manager'], ans:1 },
    { q:'What does SQL injection attack do?', opts:['Overloads a server','Injects malicious SQL code to manipulate database','Intercepts network packets','Breaks SSL encryption'], ans:1 },
  ],
  'Cloud Computing (AWS/Azure)': [
    { q:'What does IaaS stand for?', opts:['Internet as a Service','Infrastructure as a Service','Integration as a Service','Information as a Service'], ans:1 },
    { q:'What is Amazon S3 used for?', opts:['Running virtual machines','Object storage service','Database management','DNS routing'], ans:1 },
    { q:'What does "scalability" mean in cloud computing?', opts:['Data security','Ability to increase or decrease resources based on demand','Geographic distribution of servers','Cost reduction'], ans:1 },
  ],
  'Android/iOS Development': [
    { q:'What programming language is primarily used for Android development?', opts:['Swift','Kotlin/Java','Python','C#'], ans:1 },
    { q:'What is Flutter?', opts:['An Android emulator','A UI toolkit for building cross-platform apps','A database for mobile apps','An iOS testing tool'], ans:1 },
    { q:'What does APK stand for?', opts:['Apple Package Kit','Android Package Kit','Application Pack Key','App Prototype Kit'], ans:1 },
  ],
  'Data Analysis (Excel/BI)': [
    { q:'What does VLOOKUP do in Excel?', opts:['Creates a chart','Searches for a value in a table column and returns a value','Sorts data','Filters rows'], ans:1 },
    { q:'What is a Pivot Table used for?', opts:['Writing macros','Summarizing and analyzing large data sets','Creating graphs','Protecting sheets'], ans:1 },
    { q:'In Power BI, what is a "measure"?', opts:['A chart type','A calculated value using DAX formulas','A data source connection','A type of filter'], ans:1 },
  ],
};

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

const ALL_PSYCH_SCENARIOS = [
  { q:'Your team is behind schedule on a critical project. What do you do?', options:[
    {label:'Organize a triage meeting and reassign tasks based on capacity',traits:{Leadership:15,Communication:10}},
    {label:'Work extra hours yourself to bridge the gap',traits:{Persistence:15,Self_Learning:10}},
    {label:'Motivate the team and focus on team morale',traits:{Teamwork:15,Communication:10}},
    {label:'Prioritize ruthlessly and cut non-essential tasks',traits:{Decision_Making:15,Analytical_Thinking:10}},
  ]},
  { q:'You encounter a completely new type of problem. You:', options:[
    {label:'Research methodically using documentation and online resources',traits:{Curiosity:15,Self_Learning:10}},
    {label:'Ask an experienced colleague or mentor for guidance',traits:{Teamwork:10,Adaptability:10}},
    {label:'Break it into smaller sub-problems and tackle each one',traits:{Analytical_Thinking:15,Problem_Solving:10}},
    {label:'Try different approaches systematically until one works',traits:{Persistence:15,Adaptability:10}},
  ]},
  { q:'You are given freedom to choose a project topic. You choose:', options:[
    {label:'The most technically challenging unsolved problem I can find',traits:{Curiosity:15,Analytical_Thinking:10}},
    {label:'Something with clear measurable social or community impact',traits:{Leadership:10,Communication:10}},
    {label:'Something involving creative design and visual innovation',traits:{Creativity:15,Self_Learning:10}},
    {label:'Something with strong financial value or business ROI',traits:{Decision_Making:10,Confidence:10}},
  ]},
  { q:'A critical issue is found 1 hour before a major deadline. You:', options:[
    {label:'Stay calm, assess severity, and make a quick call',traits:{Stress_Management:15,Decision_Making:10}},
    {label:'Rally the entire team to solve it together immediately',traits:{Leadership:15,Teamwork:10}},
    {label:'Apply a quick fix now and plan the proper fix for later',traits:{Adaptability:15,Problem_Solving:10}},
    {label:'Inform the stakeholders with a clear status and options',traits:{Communication:15,Confidence:10}},
  ]},
  { q:'You receive criticism on work you were proud of. You:', options:[
    {label:'Reflect carefully on the feedback and look for truth in it',traits:{Analytical_Thinking:15,Adaptability:10}},
    {label:'Ask for specific examples to better understand the critique',traits:{Communication:15,Curiosity:10}},
    {label:'Defend your decisions but stay open to revising later',traits:{Confidence:15,Critical_Thinking:10}},
    {label:'Thank them, note the feedback, and act on it immediately',traits:{Teamwork:10,Adaptability:15}},
  ]},
  { q:'You have to present a complex idea to a non-technical audience. You:', options:[
    {label:'Use simple analogies and real-world examples to explain',traits:{Communication:15,Creativity:10}},
    {label:'Create a visual presentation with charts and diagrams',traits:{Creativity:15,Analytical_Thinking:10}},
    {label:'Walk them through the logic step by step, patiently',traits:{Persistence:10,Communication:15}},
    {label:'Focus on the outcomes and benefits rather than the process',traits:{Leadership:10,Decision_Making:15}},
  ]},
  { q:'You are assigned to a group project with people you disagree with. You:', options:[
    {label:'Focus on shared goals and find common ground first',traits:{Teamwork:15,Communication:10}},
    {label:'Propose a structured approach so everyone contributes fairly',traits:{Leadership:15,Decision_Making:10}},
    {label:'Adapt to the group dynamic and find where you fit best',traits:{Adaptability:15,Stress_Management:10}},
    {label:'Listen to all views carefully before proposing a middle path',traits:{Critical_Thinking:15,Communication:10}},
  ]},
  { q:'You have 3 equally important tasks and time for only 2. You:', options:[
    {label:'Rank them by impact and drop the lowest-impact one',traits:{Decision_Making:15,Analytical_Thinking:10}},
    {label:'Try to do all 3 at reduced quality to meet all commitments',traits:{Persistence:10,Stress_Management:10}},
    {label:'Delegate one task to someone with capacity',traits:{Leadership:15,Teamwork:10}},
    {label:'Communicate the conflict clearly and ask for guidance',traits:{Communication:15,Confidence:10}},
  ]},
];

// Pick 4 random unique scenarios each visit
function getRandomScenarios(pool, count) {
  const shuffled = [...pool].sort(() => Math.random() - 0.5);
  return shuffled.slice(0, count);
}
const PSYCH_SCENARIOS = getRandomScenarios(ALL_PSYCH_SCENARIOS, 4);

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
  nav.innerHTML = `
    <div class="stepper-wrapper">
      ${labels.map((label, i) => `
        <div class="step-item ${i + 1 < currentStep ? 'completed' : i + 1 === currentStep ? 'active' : ''}">
          <div class="step-dot">${i + 1 < currentStep ? '✓' : i + 1}</div>
          <div class="step-label">${label}</div>
        </div>
      `).join('<div class="step-connector"></div>')}
    </div>
  `;
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
    const res = await API.get(`/api/questions?education_level=${lvl}&board=${board}&limit=10`);
    aptitudeQuestions = (res.questions || []).slice(0, 10);
    if (!aptitudeQuestions.length) throw new Error('No questions');
  } catch {
    // Fallback static questions
    // 20 diverse aptitude questions, 10 shown randomly each visit
    const ALL_APT_Q = [
      { id:1,  question_text:'What is the next number: 2, 6, 12, 20, 30, ?', option_a:'40', option_b:'42', option_c:'44', option_d:'46', correct_answer:'B', category:'Logical Reasoning', difficulty:'Easy' },
      { id:2,  question_text:'A shopkeeper buys goods for Rs.800 and sells at 25% profit. Selling price?', option_a:'Rs.1000', option_b:'Rs.900', option_c:'Rs.1100', option_d:'Rs.1050', correct_answer:'A', category:'Numerical Reasoning', difficulty:'Easy' },
      { id:3,  question_text:'Find the odd one out: 36, 49, 64, 81, 100, 112', option_a:'81', option_b:'100', option_c:'112', option_d:'64', correct_answer:'C', category:'Logical Reasoning', difficulty:'Easy' },
      { id:4,  question_text:'A pipe fills a tank in 6 hours, another empties in 9 hours. Time to fill if both open?', option_a:'12 hrs', option_b:'15 hrs', option_c:'18 hrs', option_d:'9 hrs', correct_answer:'C', category:'Numerical Reasoning', difficulty:'Medium' },
      { id:5,  question_text:'If 5 machines make 5 items in 5 minutes, how long for 100 machines to make 100 items?', option_a:'100 min', option_b:'50 min', option_c:'5 min', option_d:'10 min', correct_answer:'C', category:'Logical Reasoning', difficulty:'Hard' },
      { id:6,  question_text:'Choose the correct analogy: Doctor : Hospital :: Teacher : ?', option_a:'Student', option_b:'School', option_c:'Book', option_d:'Classroom', correct_answer:'B', category:'Verbal Reasoning', difficulty:'Easy' },
      { id:7,  question_text:'A car travels 60 km in 1.5 hours. Speed in m/s?', option_a:'11.11 m/s', option_b:'16.67 m/s', option_c:'10 m/s', option_d:'40 m/s', correct_answer:'A', category:'Numerical Reasoning', difficulty:'Medium' },
      { id:8,  question_text:'Which word does NOT belong: Mango, Apple, Carrot, Banana, Grapes', option_a:'Mango', option_b:'Carrot', option_c:'Apple', option_d:'Banana', correct_answer:'B', category:'Verbal Reasoning', difficulty:'Easy' },
      { id:9,  question_text:'What is 15% of 280?', option_a:'40', option_b:'42', option_c:'45', option_d:'48', correct_answer:'B', category:'Numerical Reasoning', difficulty:'Easy' },
      { id:10, question_text:'Complete the series: AZ, BY, CX, DW, ?', option_a:'EV', option_b:'EU', option_c:'FV', option_d:'EW', correct_answer:'A', category:'Logical Reasoning', difficulty:'Easy' },
      { id:11, question_text:'A is 2 yrs older than B who is twice as old as C. Total A+B+C = 27. How old is B?', option_a:'8', option_b:'10', option_c:'12', option_d:'9', correct_answer:'B', category:'Logical Reasoning', difficulty:'Medium' },
      { id:12, question_text:'Which 3D shape has 6 faces, 12 edges, and 8 vertices?', option_a:'Sphere', option_b:'Pyramid', option_c:'Cube', option_d:'Cylinder', correct_answer:'C', category:'Spatial Reasoning', difficulty:'Easy' },
      { id:13, question_text:'Find next: 3, 6, 11, 18, 27, ?', option_a:'36', option_b:'38', option_c:'40', option_d:'42', correct_answer:'B', category:'Logical Reasoning', difficulty:'Medium' },
      { id:14, question_text:'Probability of drawing a red card from a 52-card deck?', option_a:'1/4', option_b:'1/3', option_c:'1/2', option_d:'1/13', correct_answer:'C', category:'Numerical Reasoning', difficulty:'Easy' },
      { id:15, question_text:'Avg score of 40 students is 72. If 4 leave with avg 60, new class average?', option_a:'73.3', option_b:'72.8', option_c:'74.1', option_d:'71.5', correct_answer:'A', category:'Numerical Reasoning', difficulty:'Hard' },
      { id:16, question_text:'If PAPER=24, PEN=12, then PENCIL=?', option_a:'36', option_b:'30', option_c:'28', option_d:'32', correct_answer:'B', category:'Verbal Reasoning', difficulty:'Medium' },
      { id:17, question_text:'Complete: 1, 1, 2, 3, 5, 8, 13, ?', option_a:'18', option_b:'19', option_c:'20', option_d:'21', correct_answer:'D', category:'Logical Reasoning', difficulty:'Easy' },
      { id:18, question_text:'Worst-case time complexity of QuickSort?', option_a:'O(N log N)', option_b:'O(N^2)', option_c:'O(N)', option_d:'O(log N)', correct_answer:'B', category:'Algorithms', difficulty:'Hard' },
      { id:19, question_text:'A room 12m x 9m. Cost to carpet at Rs.45 per sq.m?', option_a:'Rs.4860', option_b:'Rs.4500', option_c:'Rs.5040', option_d:'Rs.5400', correct_answer:'A', category:'Numerical Reasoning', difficulty:'Medium' },
      { id:20, question_text:'If a clock shows 3:45, what time does the mirror image show?', option_a:'8:15', option_b:'9:15', option_c:'8:45', option_d:'9:45', correct_answer:'A', category:'Spatial Reasoning', difficulty:'Medium' },
    ];
    // Show 10 random questions each visit for variety
    aptitudeQuestions = [...ALL_APT_Q].sort(() => Math.random() - 0.5).slice(0, 10);
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
  const alreadySelected = btn.classList.contains('selected');
  // Always clear all options in this pair first
  document.querySelectorAll(`#int-pair-${pi} .interest-option`).forEach(b => {
    b.classList.remove('selected');
    b.setAttribute('aria-pressed', 'false');
  });
  if (alreadySelected) {
    // Clicking the same one again deselects it
    state._interestAnswers[pi] = null;
  } else {
    // Select the new one
    btn.classList.add('selected');
    btn.setAttribute('aria-pressed', 'true');
    state._interestAnswers[pi] = opt;
  }
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

// ── STEP 6: SKILLS WITH QUIZ VERIFICATION ──────────────────────────────────
const state_skillProficiency = {};

function renderSkills() {
  const grid = document.getElementById('skill-grid');
  if (!grid) return;
  grid.innerHTML = SKILLS_MATRIX.map(skill => {
    const safeKey = skill.replace(/[^a-zA-Z0-9]/g,'_');
    const hasQuiz = !!SKILL_QUIZ_BANK[skill];
    return `
      <div class="skill-chip-wrapper" id="sw-${safeKey}">
        <div class="skill-chip" data-skill="${skill}" onclick="onSkillClick('${skill}')">
          <span class="skill-name">${skill}</span>
          <span class="skill-level-badge" id="slb-${safeKey}" style="display:none"></span>
        </div>
        <div class="skill-score-tag" id="sst-${safeKey}"
          style="display:none;font-size:0.6rem;color:var(--text-muted);text-align:center;margin-top:2px">
        </div>
        ${hasQuiz ? '' : ''}
      </div>
    `;
  }).join('');
}

function onSkillClick(skill) {
  const chip = document.querySelector(`.skill-chip[data-skill="${skill}"]`);
  const isSelected = chip && chip.classList.contains('selected');

  if (isSelected) {
    // Deselect: remove skill
    if (chip) chip.classList.remove('selected');
    state.selectedSkills = state.selectedSkills.filter(s => s !== skill);
    delete state_skillProficiency[skill];
    const safeKey = skill.replace(/[^a-zA-Z0-9]/g,'_');
    const badge = document.getElementById('slb-' + safeKey);
    const scoreTag = document.getElementById('sst-' + safeKey);
    if (badge) badge.style.display = 'none';
    if (scoreTag) scoreTag.style.display = 'none';
  } else {
    // Open quiz to verify, then add
    openSkillQuiz(skill);
  }
}

function toggleSkill(el, skill) { onSkillClick(skill); }

function saveSkills() {
  state.skillsWithLevel = state.selectedSkills.map(s => ({
    skill: s,
    proficiency: state_skillProficiency[s] || 'Beginner',
  }));
}

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
  saveSkills();

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
    skills_with_level: state.skillsWithLevel || state.selectedSkills.map(s => ({skill:s, proficiency:'Beginner'})),
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

// ─── SKILL QUIZ MODAL ────────────────────────────────────────────────────────
let _quizSkill = null;
let _quizAnswers = [];
let _quizTotal   = 0;

function openSkillQuiz(skill) {
  const questions = SKILL_QUIZ_BANK[skill];
  if (!questions || !questions.length) {
    // No quiz available - fallback to proficiency picker
    openFallbackPicker(skill);
    return;
  }
  _quizSkill   = skill;
  _quizAnswers = new Array(questions.length).fill(null);
  _quizTotal   = questions.length;

  const modal = document.getElementById('skill-quiz-modal');
  const title = document.getElementById('sqm-title');
  const body  = document.getElementById('sqm-body');
  const submitBtn = document.getElementById('sqm-submit');

  title.textContent = 'Skill Check: ' + skill;
  submitBtn.style.display = 'none';

  body.innerHTML = questions.map((q, qi) => `
    <div class="sqm-question" id="sqm-q${qi}">
      <div class="sqm-q-label">Q${qi+1} of ${questions.length}</div>
      <div class="sqm-q-text">${q.q}</div>
      <div class="sqm-options">
        ${q.opts.map((opt, oi) => `
          <button class="sqm-opt-btn" id="sqm-opt-${qi}-${oi}"
            onclick="selectSkillQuizOpt(${qi}, ${oi}, ${q.ans})">
            <span class="sqm-opt-letter">${['A','B','C','D'][oi]}</span>
            ${opt}
          </button>
        `).join('')}
      </div>
    </div>
  `).join('<hr style="border:none;border-top:1px solid var(--border);margin:0.75rem 0">');

  modal.style.display = 'flex';
  setTimeout(() => modal.classList.add('show'), 10);
}

function selectSkillQuizOpt(qi, oi, correctOi) {
  _quizAnswers[qi] = oi;

  // Highlight options
  document.querySelectorAll(`#sqm-q${qi} .sqm-opt-btn`).forEach((b, idx) => {
    b.classList.remove('sqm-selected', 'sqm-correct', 'sqm-wrong');
    if (idx === correctOi) b.classList.add('sqm-correct');
    else if (idx === oi && oi !== correctOi) b.classList.add('sqm-wrong');
    b.disabled = true;
  });

  // Show submit if all answered
  const allAnswered = _quizAnswers.every(a => a !== null);
  if (allAnswered) {
    const submitBtn = document.getElementById('sqm-submit');
    submitBtn.style.display = 'inline-flex';
    submitBtn.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }
}

function submitSkillQuiz() {
  const questions = SKILL_QUIZ_BANK[_quizSkill];
  let score = 0;
  _quizAnswers.forEach((ans, i) => { if (ans === questions[i].ans) score++; });

  let level = 'Beginner';
  if (score === _quizTotal) level = 'Advanced';
  else if (score >= Math.ceil(_quizTotal / 2)) level = 'Intermediate';

  // Show result in modal
  const body = document.getElementById('sqm-body');
  const icons = { Beginner:'🟡', Intermediate:'🟠', Advanced:'🟢' };
  const msgs  = {
    Beginner:     'Keep learning! You have foundational awareness.',
    Intermediate: 'Good understanding! You know the core concepts.',
    Advanced:     'Excellent! You have strong command of this skill.',
  };
  body.innerHTML = `
    <div style="text-align:center;padding:1.5rem 0">
      <div style="font-size:3rem;margin-bottom:0.5rem">${icons[level]}</div>
      <div style="font-size:1.4rem;font-weight:800;color:var(--text-h);margin-bottom:0.25rem">
        ${score} / ${_quizTotal} Correct
      </div>
      <div style="font-size:1rem;font-weight:700;color:var(--primary);margin-bottom:0.5rem">
        Proficiency: ${level}
      </div>
      <div style="font-size:0.85rem;color:var(--text-muted)">${msgs[level]}</div>
    </div>
  `;
  document.getElementById('sqm-submit').style.display = 'none';

  // Auto close after 1.8 seconds and apply result
  setTimeout(() => {
    closeSkillQuiz();
    applySkillVerification(_quizSkill, level, score, _quizTotal);
  }, 1800);
}

function closeSkillQuiz() {
  const modal = document.getElementById('skill-quiz-modal');
  modal.classList.remove('show');
  setTimeout(() => { modal.style.display = 'none'; }, 250);
}

function openFallbackPicker(skill) {
  // If no quiz, let user self-rate (simple inline)
  console.log('No quiz for:', skill);
  applySkillVerification(skill, 'Beginner', 0, 0);
}

function applySkillVerification(skill, level, score, total) {
  const safeKey = skill.replace(/[^a-zA-Z0-9]/g,'_');
  const chip  = document.querySelector(`.skill-chip[data-skill="${skill}"]`);
  const badge = document.getElementById('slb-' + safeKey);

  state_skillProficiency[skill] = level;
  if (!state.selectedSkills.includes(skill)) state.selectedSkills.push(skill);

  if (chip) chip.classList.add('selected');

  const colors     = { Beginner:'rgba(245,158,11,0.15)', Intermediate:'rgba(99,102,241,0.15)', Advanced:'rgba(16,185,129,0.15)' };
  const textColors = { Beginner:'var(--amber)', Intermediate:'var(--primary)', Advanced:'var(--emerald)' };
  const checkIcons = { Beginner:'📘', Intermediate:'📗', Advanced:'⭐' };

  if (badge) {
    badge.textContent = checkIcons[level] + ' ' + level;
    badge.style.display  = 'inline-block';
    badge.style.background  = colors[level];
    badge.style.color       = textColors[level];
    badge.style.padding     = '2px 7px';
    badge.style.borderRadius= '10px';
    badge.style.fontSize    = '0.62rem';
    badge.style.fontWeight  = '700';
    badge.style.marginLeft  = '4px';
  }

  // Show score tag if quiz was taken
  if (total > 0) {
    const scoreTag = document.getElementById('sst-' + safeKey);
    if (scoreTag) {
      scoreTag.textContent = `${score}/${total}`;
      scoreTag.style.display = 'inline-block';
    }
  }
}
// ─────────────────────────────────────────────────────────────────────────────


document.addEventListener('DOMContentLoaded', () => {
  if (!Auth.requireAuth()) return;
  renderNavbar('assessment');
  updateStepUI();
  bindEducationFields();
  renderPsychometric();
  renderInterests();
  renderSkills();
});
