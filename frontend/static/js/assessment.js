/**
 * Assessment Engine Interactive Controller.
 * Handles client-side question stepping, answer selection, autosaving,
 * status messages, and progressive submission loading UX.
 */

class AssessmentEngine {
    constructor(sessionId, questionsData, existingAnswers) {
        this.sessionId = sessionId;
        this.questions = questionsData || [];
        this.answers = existingAnswers || {};
        this.currentIndex = 0;
        this.totalQuestions = this.questions.length;
        this.questionStartTime = Date.now();

        this.initDOM();
        this.bindEvents();
        this.renderQuestion(0);
        this.updateProgress();
    }

    initDOM() {
        this.container = document.getElementById('question-display-area');
        this.progressBar = document.getElementById('assessment-progress-bar');
        this.progressText = document.getElementById('progress-text');
        this.qNumBadge = document.getElementById('question-number-badge');
        this.qSectionBadge = document.getElementById('question-section-badge');
        this.qDiffBadge = document.getElementById('question-diff-badge');
        this.qTextEl = document.getElementById('question-text');
        this.optionsContainer = document.getElementById('question-options-container');
        this.btnPrev = document.getElementById('btn-prev-q');
        this.btnNext = document.getElementById('btn-next-q');
        this.btnReview = document.getElementById('btn-review-q');
        this.saveStatusEl = document.getElementById('autosave-status');
    }

    bindEvents() {
        if (this.btnPrev) {
            this.btnPrev.addEventListener('click', () => this.navigate(-1));
        }
        if (this.btnNext) {
            this.btnNext.addEventListener('click', () => this.navigate(1));
        }
    }

    navigate(direction) {
        const timeTaken = Math.round((Date.now() - this.questionStartTime) / 1000);
        const currentQ = this.questions[this.currentIndex];
        
        if (this.answers[currentQ.id] !== undefined) {
            this.saveAnswerToBackend(currentQ.id, this.answers[currentQ.id], timeTaken);
        }

        const newIndex = this.currentIndex + direction;
        if (newIndex >= 0 && newIndex < this.totalQuestions) {
            this.currentIndex = newIndex;
            this.questionStartTime = Date.now();
            this.renderQuestion(this.currentIndex);
            this.updateProgress();
        }
    }

    renderQuestion(index) {
        if (index < 0 || index >= this.totalQuestions) return;
        const q = this.questions[index];

        if (this.qNumBadge) this.qNumBadge.textContent = `Question ${index + 1} of ${this.totalQuestions}`;
        if (this.qSectionBadge) this.qSectionBadge.textContent = q.section_name || 'General';
        if (this.qDiffBadge) this.qDiffBadge.textContent = q.difficulty || 'Medium';
        if (this.qTextEl) this.qTextEl.textContent = q.question_text;

        this.optionsContainer.innerHTML = '';
        const savedAnswer = this.answers[q.id];

        if (q.question_type === 'RATING') {
            const ratingWrap = document.createElement('div');
            ratingWrap.className = 'rating-grid-custom';

            const ratingLabels = [
                { val: '1', text: '1 - Low Interest / Ability' },
                { val: '2', text: '2 - Basic Familiarity' },
                { val: '3', text: '3 - Moderate / Average' },
                { val: '4', text: '4 - Strong Confidence' },
                { val: '5', text: '5 - High Affinity / Passion' }
            ];

            const optionsToRender = q.options && q.options.length > 0 ? q.options : ratingLabels;

            optionsToRender.forEach(opt => {
                const btn = document.createElement('button');
                btn.type = 'button';
                const optVal = opt.option_value || opt.val;
                const isSelected = savedAnswer == optVal;
                btn.className = `rating-btn-custom ${isSelected ? 'active' : ''}`;
                btn.textContent = opt.option_text || opt.text;
                btn.setAttribute('aria-pressed', isSelected ? 'true' : 'false');
                btn.addEventListener('click', () => {
                    this.selectRating(q.id, optVal);
                });
                ratingWrap.appendChild(btn);
            });
            this.optionsContainer.appendChild(ratingWrap);

        } else {
            // MCQ, Scenario, Multi-select
            q.options.forEach((opt) => {
                const optBox = document.createElement('div');
                const isSelected = savedAnswer == opt.option_value;
                optBox.className = `option-box ${isSelected ? 'selected' : ''}`;
                optBox.innerHTML = `
                    <div class="form-check w-100 d-flex align-items-center mb-0">
                        <input class="form-check-input me-3" type="radio" name="q_${q.id}" id="opt_${opt.id}" value="${opt.option_value}" ${isSelected ? 'checked' : ''}>
                        <label class="form-check-label w-100 cursor-pointer text-start" for="opt_${opt.id}">
                            ${opt.option_text}
                        </label>
                    </div>
                `;

                optBox.addEventListener('click', () => {
                    const radio = optBox.querySelector('input[type="radio"]');
                    if (radio) radio.checked = true;
                    this.selectOption(q.id, opt.option_value);
                });

                this.optionsContainer.appendChild(optBox);
            });
        }

        // Button Visibility
        if (this.btnPrev) this.btnPrev.disabled = (index === 0);
        if (this.btnNext) {
            if (index === this.totalQuestions - 1) {
                this.btnNext.style.display = 'none';
                if (this.btnReview) this.btnReview.style.display = 'inline-flex';
            } else {
                this.btnNext.style.display = 'inline-flex';
                if (this.btnReview) this.btnReview.style.display = 'none';
            }
        }
    }

    selectOption(questionId, value) {
        this.answers[questionId] = value;
        const allBoxes = this.optionsContainer.querySelectorAll('.option-box');
        allBoxes.forEach(box => {
            const radio = box.querySelector('input');
            if (radio && radio.value == value) {
                box.classList.add('selected');
            } else {
                box.classList.remove('selected');
            }
        });
        this.saveAnswerToBackend(questionId, value);
        this.updateProgress();
    }

    selectRating(questionId, value) {
        this.answers[questionId] = value;
        const allRatingBtns = this.optionsContainer.querySelectorAll('.rating-btn-custom');
        allRatingBtns.forEach(btn => {
            btn.classList.remove('active');
            btn.setAttribute('aria-pressed', 'false');
            if (btn.textContent.startsWith(value) || btn.textContent.includes(value)) {
                btn.classList.add('active');
                btn.setAttribute('aria-pressed', 'true');
            }
        });
        this.saveAnswerToBackend(questionId, value);
        this.updateProgress();
    }

    async saveAnswerToBackend(questionId, value, timeTaken = 0) {
        if (this.saveStatusEl) {
            this.saveStatusEl.innerHTML = '<span class="text-muted"><i class="bi bi-arrow-repeat spin"></i> Saving...</span>';
        }
        try {
            const res = await fetch('/api/assessment/answer', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    session_id: this.sessionId,
                    question_id: questionId,
                    selected_option: value,
                    time_taken_seconds: timeTaken
                })
            });
            if (res.ok && this.saveStatusEl) {
                this.saveStatusEl.innerHTML = '<span class="text-success"><i class="bi bi-check-circle-fill me-1"></i> Progress saved</span>';
            }
        } catch (err) {
            if (this.saveStatusEl) {
                this.saveStatusEl.innerHTML = '<span class="text-muted">Saved offline</span>';
            }
        }
    }

    updateProgress() {
        const answeredCount = Object.keys(this.answers).length;
        const pct = Math.round((answeredCount / this.totalQuestions) * 100);
        if (this.progressBar) {
            this.progressBar.style.width = `${pct}%`;
            this.progressBar.setAttribute('aria-valuenow', pct);
        }
        if (this.progressText) {
            this.progressText.textContent = `${answeredCount} of ${this.totalQuestions} answered (${pct}%)`;
        }
    }
}

// Function to trigger progressive loading overlay on final assessment submission
function showSubmissionLoadingOverlay() {
    const overlay = document.createElement('div');
    overlay.className = 'loading-overlay';
    overlay.id = 'submission-loading-overlay';
    overlay.innerHTML = `
        <div class="loading-card">
            <div class="spinner-border text-primary mb-3" style="width: 3rem; height: 3rem;" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <h4 class="fw-bold mb-2">Generating Recommendations</h4>
            <p id="loading-status-msg" class="text-secondary mb-0">Analyzing your profile...</p>
        </div>
    `;
    document.body.appendChild(overlay);

    const statusMsg = document.getElementById('loading-status-msg');
    setTimeout(() => {
        if (statusMsg) statusMsg.textContent = 'Comparing your profile with 1,206 career paths...';
    }, 1200);
    setTimeout(() => {
        if (statusMsg) statusMsg.textContent = 'Evaluating compatibility with XGBoost model...';
    }, 2400);
    setTimeout(() => {
        if (statusMsg) statusMsg.textContent = 'Preparing your personalized roadmap...';
    }, 3600);
}

window.AssessmentEngine = AssessmentEngine;
window.showSubmissionLoadingOverlay = showSubmissionLoadingOverlay;
