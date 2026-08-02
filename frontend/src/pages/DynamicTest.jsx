import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const DynamicTest = () => {
  const navigate = useNavigate();
  const [careerPath, setCareerPath] = useState('');
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [evaluating, setEvaluating] = useState(false);

  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [score, setScore] = useState(0);
  const [userAnswers, setUserAnswers] = useState([]);
  const [showResults, setShowResults] = useState(false);
  const [verifiedCareer, setVerifiedCareer] = useState('');

  useEffect(() => {
    const savedCareer = localStorage.getItem('recommendedCareer');
    const savedInterest = localStorage.getItem('userInterest') || '';
    const targetCareer = savedCareer || 'General Aptitude';
    setCareerPath(targetCareer);
    fetchQuestions(targetCareer, savedInterest);
  }, []);

  const fetchQuestions = async (career, interest = '') => {
    try {
      const response = await axios.get(
        `http://127.0.0.1:5000/api/questions?career=${encodeURIComponent(career)}&interest=${encodeURIComponent(interest)}&limit=10`
      );
      if (response.data.status === 'success' && response.data.questions.length > 0) {
        setQuestions(response.data.questions);
      } else {
        setError('No questions found for this career path.');
      }
    } catch (err) {
      console.error(err);
      setError('Failed to fetch questions from the database.');
    } finally {
      setLoading(false);
    }
  };

  const handleAnswerClick = (selectedOption) => {
    const currentQ = questions[currentQuestionIndex];
    const isCorrect = selectedOption.toUpperCase() === currentQ.correct_option.toUpperCase();
    
    const updatedScore = isCorrect ? score + 1 : score;
    setScore(updatedScore);
    setUserAnswers((prev) => [...prev, { question: currentQ.question_text, selectedOption, isCorrect }]);

    const nextQuestion = currentQuestionIndex + 1;
    if (nextQuestion < questions.length) {
      setCurrentQuestionIndex(nextQuestion);
    } else {
      setShowResults(true);
      reEvaluateCareer(updatedScore, questions.length);
    }
  };

  const reEvaluateCareer = async (finalScore, totalQuestions) => {
    setEvaluating(true);
    try {
      const scorePct = Math.round((finalScore / totalQuestions) * 100);
      const savedProfile = JSON.parse(localStorage.getItem('studentProfile') || '{}');

      // Update student profile with verified skill test score
      const updatedProfile = {
        ...savedProfile,
        Coding_Score: scorePct,
        Domain_Knowledge_Score: scorePct,
        Problem_Solving_Score: Math.min(100, Math.max(50, scorePct + 10)),
        Career_Readiness_Score: scorePct
      };

      // Re-run AI model with verified profile
      const response = await axios.post('http://127.0.0.1:5000/api/predict/career', updatedProfile);
      const finalCareer = response.data.recommended_career_cluster;

      setVerifiedCareer(finalCareer);
      localStorage.setItem('verifiedScore', scorePct);
      localStorage.setItem('finalRecommendedCareer', finalCareer);
      localStorage.setItem('verifiedProfile', JSON.stringify(updatedProfile));

      // Save to user assessment history if logged in
      const userStr = localStorage.getItem('user');
      if (userStr) {
        const user = JSON.parse(userStr);
        await axios.post('http://127.0.0.1:5000/api/assessment/save', {
          user_id: user.id,
          education_level: updatedProfile.Education_Level || 'Class 11-12',
          riasec_trait: localStorage.getItem('riasecTrait') || 'Investigative',
          recommended_career: finalCareer,
          verified_score: scorePct
        }).catch(e => console.error("History save failed:", e));
      }
    } catch (err) {
      console.error('Re-evaluation error:', err);
      setVerifiedCareer(careerPath);
      localStorage.setItem('finalRecommendedCareer', careerPath);
    } finally {
      setEvaluating(false);
    }
  };

  const finishTest = () => {
    navigate('/dashboard');
  };

  if (loading) {
    return (
      <div className="test-card">
        <p>Loading dynamic verification questions...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="test-card">
        <p className="error-text">{error}</p>
        <button onClick={() => navigate('/')}>Back to Profile</button>
      </div>
    );
  }

  const q = questions[currentQuestionIndex];
  const progressPct = Math.round(((currentQuestionIndex + 1) / questions.length) * 100);

  return (
    <div className="test-container">
      <h2>Step 2: Dynamic Skill Verification Test</h2>
      <p className="subtitle">Targeting: <strong>{careerPath}</strong></p>
      
      {showResults ? (
        <div className="results-card">
          <h3>Skill Verification Complete!</h3>
          <div className="score-badge">
            <span className="score-num">{score}</span> / {questions.length} Correct ({Math.round((score / questions.length) * 100)}%)
          </div>

          {evaluating ? (
            <p className="loading-text">Recalculating AI Recommendation with your verified score...</p>
          ) : (
            <div className="verified-box">
              <p><strong>Verified Recommendation:</strong></p>
              <h4 className="career-tag">{verifiedCareer || careerPath}</h4>
            </div>
          )}

          <br />
          <button className="primary-btn" onClick={finishTest} disabled={evaluating}>
            Proceed to Final Dashboard
          </button>
        </div>
      ) : (
        <div className="question-card">
          <div className="progress-bar">
            <div className="progress-fill" style={{ width: `${progressPct}%` }}></div>
          </div>
          <p className="q-counter">Question {currentQuestionIndex + 1} of {questions.length} ({q.difficulty} level)</p>
          
          <h3 className="q-text">{q.question_text}</h3>
          
          <div className="options-grid">
            <button className="option-btn" onClick={() => handleAnswerClick('A')}>
              <strong>A.</strong> {q.option_a}
            </button>
            <button className="option-btn" onClick={() => handleAnswerClick('B')}>
              <strong>B.</strong> {q.option_b}
            </button>
            <button className="option-btn" onClick={() => handleAnswerClick('C')}>
              <strong>C.</strong> {q.option_c}
            </button>
            <button className="option-btn" onClick={() => handleAnswerClick('D')}>
              <strong>D.</strong> {q.option_d}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default DynamicTest;