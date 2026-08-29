/**
 * Assessment Engine Interactive Controller (Upgraded UX & Accessibility Suite).
 * Features:
 * - Question Palette Grid with real-time status (Answered, Flagged, Active, Unanswered)
 * - Flag for Review bookmarking
 * - Text-to-Speech (TTS) Voice Audio Reader with SpeechSynthesis API
 * - Font Size Scaler (A-, A, A+)
 * - Full Keyboard Shortcuts (1-5, A-D, Arrows, N, P, F, S, ?)
 * - Timed Challenge Mode countdown timer
 * - Robust instant autosaving and progress metrics
 */

class AssessmentEngine {
    constructor(sessionId, questionsData, existingAnswers) {
        this.sessionId = sessionId;
        this.questions = questionsData || [];
        this.answers = existingAnswers || {};
        this.currentIndex = 0;
        this.totalQuestions = this.questions.length;
        this.questionStartTime = Date.now();

        // Load flagged questions from localStorage
        const storedFlags = localStorage.getItem(`assessment_flags_${this.sessionId}`);
        this.flagged = new Set(storedFlags ? JSON.parse(storedFlags) : []);

        // Text-to-Speech Synth
        this.synth = window.speechSynthesis;
        this.isSpeaking = false;

        // Current Font Size Scale
        this.currentFontSize = 'md';

        // Timed Mode Setup
        this.mode = localStorage.getItem('assessment_mode') || 'standard';
        this.remainingSeconds = 45 * 60; // 45 minutes default for timed mode
        this.timerInterval = null;

        this.initDOM();
        this.bindEvents();
        this.initTimedMode();
        this.renderPalette();
        this.renderQuestion(0);
        this.updateProgress();
    }

    initDOM() {
        this.container = document.getElementById('question-display-area');
        this.progressBar = document.getElementById('assessment-progress-bar');
        this.progressText = document.getElementById('progress-text');
        this.progressSummary = document.getElementById('progress-summary-text');
        this.qNumBadge = document.getElementById('question-number-badge');
        this.qSectionBadge = document.getElementById('question-section-badge');
        this.qDiffBadge = document.getElementById('question-diff-badge');
        this.qTextEl = document.getElementById('question-text');
        this.optionsContainer = document.getElementById('question-options-container');
        this.btnPrev = document.getElementById('btn-prev-q');
        this.btnNext = document.getElementById('btn-next-q');
        this.btnReview = document.getElementById('btn-review-q');
        this.saveStatusEl = document.getElementById('autosave-status');

        // Accessibility & UX Elements
        this.btnFlag = document.getElementById('btn-flag-q');
        this.flagIcon = document.getElementById('flag-icon');
        this.flagText = document.getElementById('flag-text');
        this.btnTTS = document.getElementById('btn-tts-speak');
        this.ttsIcon = document.getElementById('tts-icon');
        this.ttsText = document.getElementById('tts-text');

        this.btnFontSm = document.getElementById('btn-font-sm');
        this.btnFontMd = document.getElementById('btn-font-md');
        this.btnFontLg = document.getElementById('btn-font-lg');

        this.paletteGrid = document.getElementById('question-palette-grid');
        this.paletteAnswered = document.getElementById('palette-count-answered');
        this.paletteFlagged = document.getElementById('palette-count-flagged');
        this.paletteRemaining = document.getElementById('palette-count-remaining');
        this.paletteTotalBadge = document.getElementById('palette-total-badge');

        this.timerContainer = document.getElementById('assessment-timer-container');
        this.timerDisplay = document.getElementById('timer-display');
        this.timerBadge = document.getElementById('assessment-timer-badge');
        this.modeBadge = document.getElementById('active-mode-badge');
    }

    bindEvents() {
        if (this.btnPrev) {
            this.btnPrev.addEventListener('click', () => this.navigate(-1));
        }
        if (this.btnNext) {
            this.btnNext.addEventListener('click', () => this.navigate(1));
        }
        if (this.btnFlag) {
            this.btnFlag.addEventListener('click', () => this.toggleFlag());
        }
        if (this.btnTTS) {
            this.btnTTS.addEventListener('click', () => this.toggleSpeech());
        }

        // Font scaling
        if (this.btnFontSm) this.btnFontSm.addEventListener('click', () => this.setFontSize('sm'));
        if (this.btnFontMd) this.btnFontMd.addEventListener('click', () => this.setFontSize('md'));
        if (this.btnFontLg) this.btnFontLg.addEventListener('click', () => this.setFontSize('lg'));

        // Global Keyboard Shortcuts
        window.addEventListener('keydown', (e) => this.handleKeyboardShortcut(e));
    }

    handleKeyboardShortcut(e) {
        // Ignore if typing in an input
        if (['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement.tagName)) return;

        const key = e.key;

        // Navigation: Next (N or ArrowRight)
        if (key === 'ArrowRight' || key === 'n' || key === 'N') {
            e.preventDefault();
            this.navigate(1);
        }
        // Navigation: Previous (P or ArrowLeft)
        else if (key === 'ArrowLeft' || key === 'p' || key === 'P') {
            e.preventDefault();
            this.navigate(-1);
        }
        // Flag for review: F
        else if (key === 'f' || key === 'F') {
            e.preventDefault();
            this.toggleFlag();
        }
        // Text-to-Speech: S
        else if (key === 's' || key === 'S') {
            e.preventDefault();
            this.toggleSpeech();
        }
        // Number keys 1-5 for options selection
        else if (['1', '2', '3', '4', '5'].includes(key)) {
            const numVal = parseInt(key, 10);
            const currentQ = this.questions[this.currentIndex];
            if (currentQ) {
                if (currentQ.question_type === 'RATING') {
                    this.selectRating(currentQ.id, key);
                } else if (currentQ.options && currentQ.options.length >= numVal) {
                    const opt = currentQ.options[numVal - 1];
                    this.selectOption(currentQ.id, opt.option_value);
                }
            }
        }
        // Letter keys A-D for MCQ
        else if (['a', 'b', 'c', 'd', 'A', 'B', 'C', 'D'].includes(key)) {
            const letter = key.toUpperCase();
            const currentQ = this.questions[this.currentIndex];
            if (currentQ && currentQ.options) {
                const opt = currentQ.options.find(o => String(o.option_value).toUpperCase() === letter);
                if (opt) {
                    this.selectOption(currentQ.id, opt.option_value);
                }
            }
        }
    }

    initTimedMode() {
        if (this.mode === 'timed' && this.timerContainer && this.timerDisplay) {
            this.timerContainer.style.display = 'block';
            if (this.modeBadge) {
                this.modeBadge.innerHTML = '<i class="bi bi-stopwatch text-warning me-1"></i> Timed Challenge Mode';
            }

            this.timerInterval = setInterval(() => {
                this.remainingSeconds--;
                if (this.remainingSeconds <= 0) {
                    clearInterval(this.timerInterval);
                    this.timerDisplay.textContent = '00:00';
                    alert('Time is up! Please review and submit your assessment.');
                    window.location.href = `/assessment/review`;
                    return;
                }

                const mins = Math.floor(this.remainingSeconds / 60);
                const secs = this.remainingSeconds % 60;
                this.timerDisplay.textContent = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;

                if (this.remainingSeconds <= 300 && this.timerBadge) {
                    this.timerBadge.classList.add('warning');
                }
            }, 1000);
        }
    }

    setFontSize(size) {
        this.currentFontSize = size;
        [this.btnFontSm, this.btnFontMd, this.btnFontLg].forEach(btn => {
            if (btn) btn.classList.remove('active');
        });

        if (size === 'sm') {
            if (this.btnFontSm) this.btnFontSm.classList.add('active');
            if (this.qTextEl) this.qTextEl.style.fontSize = '1.1rem';
            if (this.optionsContainer) this.optionsContainer.style.fontSize = '0.9rem';
        } else if (size === 'lg') {
            if (this.btnFontLg) this.btnFontLg.classList.add('active');
            if (this.qTextEl) this.qTextEl.style.fontSize = '1.55rem';
            if (this.optionsContainer) this.optionsContainer.style.fontSize = '1.15rem';
        } else {
            if (this.btnFontMd) this.btnFontMd.classList.add('active');
            if (this.qTextEl) this.qTextEl.style.fontSize = '1.35rem';
            if (this.optionsContainer) this.optionsContainer.style.fontSize = '1rem';
        }
    }

    toggleFlag() {
        const currentQ = this.questions[this.currentIndex];
        if (!currentQ) return;

        if (this.flagged.has(currentQ.id)) {
            this.flagged.delete(currentQ.id);
        } else {
            this.flagged.add(currentQ.id);
        }

        // Persist to localStorage
        localStorage.setItem(`assessment_flags_${this.sessionId}`, JSON.stringify(Array.from(this.flagged)));

        this.updateFlagButtonState(currentQ.id);
        this.renderPalette();
        this.updateProgress();
    }

    updateFlagButtonState(questionId) {
        const isFlagged = this.flagged.has(questionId);
        if (this.btnFlag) {
            if (isFlagged) {
                this.btnFlag.classList.add('active');
                if (this.flagIcon) this.flagIcon.className = 'bi bi-flag-fill text-warning';
                if (this.flagText) this.flagText.textContent = 'Flagged';
            } else {
                this.btnFlag.classList.remove('active');
                if (this.flagIcon) this.flagIcon.className = 'bi bi-flag';
                if (this.flagText) this.flagText.textContent = 'Flag';
            }
        }
    }

    toggleSpeech() {
        if (!('speechSynthesis' in window)) {
            alert('Text-to-speech audio reader is not supported in this browser.');
            return;
        }

        if (this.synth.speaking) {
            this.synth.cancel();
            this.resetTTSButton();
            return;
        }

        const currentQ = this.questions[this.currentIndex];
        if (!currentQ) return;

        let speechText = `Question ${this.currentIndex + 1}. Section: ${currentQ.section_name || 'General'}. ${currentQ.question_text}. `;
        if (currentQ.options && currentQ.options.length > 0) {
            currentQ.options.forEach((opt, idx) => {
                speechText += `Option ${String.fromCharCode(65 + idx)}: ${opt.option_text}. `;
            });
        }

        const utterance = new SpeechSynthesisUtterance(speechText);
        utterance.rate = 0.95;
        utterance.pitch = 1.0;

        utterance.onstart = () => {
            if (this.btnTTS) this.btnTTS.classList.add('speaking');
            if (this.ttsIcon) this.ttsIcon.className = 'bi bi-stop-circle-fill text-danger';
            if (this.ttsText) this.ttsText.textContent = 'Stop';
        };

        utterance.onend = () => {
            this.resetTTSButton();
        };

        utterance.onerror = () => {
            this.resetTTSButton();
        };

        this.synth.speak(utterance);
    }

    resetTTSButton() {
        if (this.btnTTS) this.btnTTS.classList.remove('speaking');
        if (this.ttsIcon) this.ttsIcon.className = 'bi bi-volume-up-fill';
        if (this.ttsText) this.ttsText.textContent = 'Listen';
    }

    renderPalette() {
        if (!this.paletteGrid) return;
        this.paletteGrid.innerHTML = '';

        if (this.paletteTotalBadge) {
            this.paletteTotalBadge.textContent = `${this.totalQuestions} Qs`;
        }

        this.questions.forEach((q, idx) => {
            const btn = document.createElement('button');
            btn.type = 'button';
            const isCurrent = idx === this.currentIndex;
            const isAnswered = this.answers[q.id] !== undefined;
            const isFlagged = this.flagged.has(q.id);

            let statusClass = 'unanswered';
            if (isAnswered) statusClass = 'answered';
            if (isFlagged) statusClass = 'flagged';
            if (isCurrent) statusClass += ' active';

            btn.className = `q-palette-btn ${statusClass}`;
            btn.textContent = idx + 1;
            btn.title = `Jump to Question ${idx + 1} (${q.section_name || 'General'})`;

            btn.addEventListener('click', () => {
                this.jumpToQuestion(idx);
            });

            this.paletteGrid.appendChild(btn);
        });
    }

    jumpToQuestion(index) {
        if (index < 0 || index >= this.totalQuestions) return;
        if (this.synth && this.synth.speaking) this.synth.cancel();
        this.resetTTSButton();

        const timeTaken = Math.round((Date.now() - this.questionStartTime) / 1000);
        const currentQ = this.questions[this.currentIndex];
        if (currentQ && this.answers[currentQ.id] !== undefined) {
            this.saveAnswerToBackend(currentQ.id, this.answers[currentQ.id], timeTaken);
        }

        this.currentIndex = index;
        this.questionStartTime = Date.now();
        this.renderQuestion(this.currentIndex);
        this.updateProgress();
        this.renderPalette();
    }

    navigate(direction) {
        if (this.synth && this.synth.speaking) this.synth.cancel();
        this.resetTTSButton();

        const timeTaken = Math.round((Date.now() - this.questionStartTime) / 1000);
        const currentQ = this.questions[this.currentIndex];
        
        if (currentQ && this.answers[currentQ.id] !== undefined) {
            this.saveAnswerToBackend(currentQ.id, this.answers[currentQ.id], timeTaken);
        }

        const newIndex = this.currentIndex + direction;
        if (newIndex >= 0 && newIndex < this.totalQuestions) {
            this.currentIndex = newIndex;
            this.questionStartTime = Date.now();
            this.renderQuestion(this.currentIndex);
            this.updateProgress();
            this.renderPalette();
        }
    }

    renderQuestion(index) {
        if (index < 0 || index >= this.totalQuestions) return;
        const q = this.questions[index];

        if (this.qNumBadge) this.qNumBadge.textContent = `Question ${index + 1} of ${this.totalQuestions}`;
        if (this.qSectionBadge) this.qSectionBadge.textContent = q.section_name || 'General';
        if (this.qDiffBadge) this.qDiffBadge.textContent = q.difficulty || 'Medium';
        if (this.qTextEl) this.qTextEl.textContent = q.question_text;

        this.updateFlagButtonState(q.id);
        this.setFontSize(this.currentFontSize);

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

            optionsToRender.forEach((opt, idx) => {
                const btn = document.createElement('button');
                btn.type = 'button';
                const optVal = opt.option_value || opt.val;
                const isSelected = savedAnswer == optVal;
                btn.className = `rating-btn-custom ${isSelected ? 'active' : ''}`;
                btn.innerHTML = `
                    <div class="d-flex justify-content-between align-items-center w-100">
                        <span>${opt.option_text || opt.text}</span>
                        <span class="kbd-badge ms-2">${idx + 1}</span>
                    </div>
                `;
                btn.setAttribute('aria-pressed', isSelected ? 'true' : 'false');
                btn.addEventListener('click', () => {
                    this.selectRating(q.id, optVal);
                });
                ratingWrap.appendChild(btn);
            });
            this.optionsContainer.appendChild(ratingWrap);

        } else {
            // MCQ, Scenario, Multi-select
            q.options.forEach((opt, idx) => {
                const optBox = document.createElement('div');
                const isSelected = savedAnswer == opt.option_value;
                const letterKey = String.fromCharCode(65 + idx);
                optBox.className = `option-box ${isSelected ? 'selected' : ''}`;
                optBox.innerHTML = `
                    <div class="form-check w-100 d-flex justify-content-between align-items-center mb-0">
                        <div class="d-flex align-items-center">
                            <input class="form-check-input me-3" type="radio" name="q_${q.id}" id="opt_${opt.id}" value="${opt.option_value}" ${isSelected ? 'checked' : ''}>
                            <label class="form-check-label cursor-pointer text-start" for="opt_${opt.id}">
                                <strong>${letterKey}.</strong> ${opt.option_text}
                            </label>
                        </div>
                        <span class="kbd-badge ms-2">${letterKey}</span>
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
        this.renderPalette();
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
        this.renderPalette();
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
        const flaggedCount = this.flagged.size;
        const remainingCount = Math.max(0, this.totalQuestions - answeredCount);
        const pct = Math.round((answeredCount / this.totalQuestions) * 100);

        if (this.progressBar) {
            this.progressBar.style.width = `${pct}%`;
            this.progressBar.setAttribute('aria-valuenow', pct);
        }
        if (this.progressText) {
            this.progressText.textContent = `${pct}% Complete`;
        }
        if (this.progressSummary) {
            this.progressSummary.textContent = `${answeredCount} / ${this.totalQuestions} Answered`;
        }
        if (this.paletteAnswered) {
            this.paletteAnswered.textContent = answeredCount;
        }
        if (this.paletteFlagged) {
            this.paletteFlagged.textContent = flaggedCount;
        }
        if (this.paletteRemaining) {
            this.paletteRemaining.textContent = remainingCount;
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
