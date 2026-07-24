// Main JavaScript for Career Recommendation System

// Global variables
let currentTheme = 'light';
let currentUser = null;

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', function() {
    initializeTheme();
    initializeTooltips();
    initializeDropdowns();
    initializeFormValidation();
    initializeRangeSliders();
    initializeCharts();
    initializeProgressBars();
    initializeLoadingStates();
    initializeSearchAutocomplete();
    setupEventListeners();
});

// Theme Management
function initializeTheme() {
    // Check for saved theme preference
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    currentTheme = savedTheme;
    updateThemeIcons(savedTheme);
}

function toggleTheme() {
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    currentTheme = newTheme;
    updateThemeIcons(newTheme);
}

function updateThemeIcons(theme) {
    const themeIcons = document.querySelectorAll('[data-theme-icon]');
    themeIcons.forEach(icon => {
        if (theme === 'dark') {
            icon.classList.remove('fa-sun');
            icon.classList.add('fa-moon');
        } else {
            icon.classList.remove('fa-moon');
            icon.classList.add('fa-sun');
        }
    });
}

// Tooltip Initialization
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Dropdown Initialization
function initializeDropdowns() {
    const dropdownElementList = [].slice.call(document.querySelectorAll('.dropdown-toggle'));
    dropdownElementList.map(function(dropdownToggleEl) {
        return new bootstrap.Dropdown(dropdownToggleEl);
    });
}

// Form Validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Real-time validation
    const inputs = document.querySelectorAll('input[required], select[required], textarea[required]');
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateField(this);
        });
        input.addEventListener('input', function() {
            if (this.classList.contains('is-invalid')) {
                validateField(this);
            }
        });
    });
}

function validateField(field) {
    if (field.checkValidity()) {
        field.classList.remove('is-invalid');
        field.classList.add('is-valid');
        return true;
    } else {
        field.classList.remove('is-valid');
        field.classList.add('is-invalid');
        return false;
    }
}

function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;

    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');

    requiredFields.forEach(field => {
        if (!validateField(field)) {
            isValid = false;
        }
    });

    return isValid;
}

// Range Slider Value Display
function initializeRangeSliders() {
    const rangeSliders = document.querySelectorAll('input[type="range"]');
    rangeSliders.forEach(slider => {
        const valueDisplay = document.getElementById(slider.id + '-value');
        if (valueDisplay) {
            valueDisplay.textContent = slider.value;
            slider.addEventListener('input', function() {
                valueDisplay.textContent = this.value;
            });
        }
    });
}

// Chart Initialization
function initializeCharts() {
    // Check if Chart.js is loaded
    if (typeof Chart === 'undefined') return;

    // Skill Radar Chart
    const radarCtx = document.getElementById('skillRadarChart');
    if (radarCtx) {
        new Chart(radarCtx, {
            type: 'radar',
            data: {
                labels: ['Technical', 'Analytical', 'Communication', 'Leadership', 'Problem Solving', 'Creativity'],
                datasets: [{
                    label: 'Your Skills',
                    data: [7, 8, 6, 5, 8, 7],
                    backgroundColor: 'rgba(99, 102, 241, 0.2)',
                    borderColor: 'rgba(99, 102, 241, 1)',
                    borderWidth: 2,
                    pointBackgroundColor: 'rgba(99, 102, 241, 1)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgba(99, 102, 241, 1)'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                scales: {
                    r: {
                        angleLines: {
                            display: true
                        },
                        suggestedMin: 0,
                        suggestedMax: 10,
                        pointLabels: {
                            font: {
                                size: 12
                            }
                        }
                    }
                },
                plugins: {
                    legend: {
                        position: 'top',
                    }
                }
            }
        });
    }

    // Recommendation Confidence Chart
    const confidenceCtx = document.getElementById('confidenceChart');
    if (confidenceCtx) {
        const confidenceData = JSON.parse(confidenceCtx.dataset.confidence || '[]');
        new Chart(confidenceCtx, {
            type: 'bar',
            data: {
                labels: confidenceData.map(d => d.career),
                datasets: [{
                    label: 'Confidence Score (%)',
                    data: confidenceData.map(d => d.confidence),
                    backgroundColor: 'rgba(99, 102, 241, 0.8)',
                    borderColor: 'rgba(99, 102, 241, 1)',
                    borderWidth: 1,
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                indexAxis: 'y',
                scales: {
                    x: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    }

    // Skill Distribution Chart
    const skillDistributionCtx = document.getElementById('skillDistributionChart');
    if (skillDistributionCtx) {
        const skillData = JSON.parse(skillDistributionCtx.dataset.skills || '{}');
        new Chart(skillDistributionCtx, {
            type: 'doughnut',
            data: {
                labels: Object.keys(skillData),
                datasets: [{
                    data: Object.values(skillData),
                    backgroundColor: [
                        'rgba(99, 102, 241, 0.8)',
                        'rgba(139, 92, 246, 0.8)',
                        'rgba(16, 185, 129, 0.8)',
                        'rgba(245, 158, 11, 0.8)',
                        'rgba(239, 68, 68, 0.8)',
                        'rgba(59, 130, 246, 0.8)'
                    ],
                    borderColor: [
                        'rgba(99, 102, 241, 1)',
                        'rgba(139, 92, 246, 1)',
                        'rgba(16, 185, 129, 1)',
                        'rgba(245, 158, 11, 1)',
                        'rgba(239, 68, 68, 1)',
                        'rgba(59, 130, 246, 1)'
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'right'
                    }
                }
            }
        });
    }
}

// Progress Bar Animation
function initializeProgressBars() {
    const progressBars = document.querySelectorAll('.progress-bar');
    progressBars.forEach(bar => {
        const percent = bar.getAttribute('aria-valuenow');
        if (percent) {
            // Animate on scroll into view
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.style.width = percent + '%';
                        observer.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.5 });

            observer.observe(bar);
        }
    });
}

// Loading State Management
function initializeLoadingStates() {
    // Add loading state to buttons with data-loading attribute
    const loadingButtons = document.querySelectorAll('[data-loading]');
    loadingButtons.forEach(button => {
        button.addEventListener('click', function() {
            const loadingText = this.dataset.loading;
            const originalText = this.innerHTML;
            this.innerHTML = '<span class="loading-spinner me-2"></span>' + loadingText;
            this.disabled = true;

            // Auto-disable after 10 seconds as fallback
            setTimeout(() => {
                this.innerHTML = originalText;
                this.disabled = false;
            }, 10000);
        });
    });
}

// Search Autocomplete
function initializeSearchAutocomplete() {
    const searchInputs = document.querySelectorAll('[data-autocomplete]');
    searchInputs.forEach(input => {
        let debounceTimer;
        input.addEventListener('input', function() {
            clearTimeout(debounceTimer);
            const query = this.value.trim();

            if (query.length < 2) {
                hideAutocomplete(this);
                return;
            }

            debounceTimer = setTimeout(() => {
                fetchAutocomplete(this, query);
            }, 300);
        });

        // Hide autocomplete on click outside
        document.addEventListener('click', function(e) {
            if (!input.contains(e.target)) {
                hideAutocomplete(input);
            }
        });
    });
}

function fetchAutocomplete(input, query) {
    const endpoint = input.dataset.autocomplete || '/api/search';

    fetch(`${endpoint}?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            if (data.success && data.results) {
                showAutocomplete(input, data.results);
            }
        })
        .catch(error => {
            console.error('Autocomplete error:', error);
        });
}

function showAutocomplete(input, results) {
    // Remove existing autocomplete
    hideAutocomplete(input);

    // Create autocomplete dropdown
    const dropdown = document.createElement('div');
    dropdown.className = 'autocomplete-dropdown';
    dropdown.style.cssText = 'position: absolute; top: 100%; left: 0; right: 0; background: white; border: 1px solid var(--gray-200); border-radius: 0.5rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1); z-index: 1000; max-height: 200px; overflow-y: auto; margin-top: 0.25rem;';

    results.forEach(result => {
        const item = document.createElement('div');
        item.className = 'autocomplete-item';
        item.style.cssText = 'padding: 0.75rem 1rem; cursor: pointer; border-bottom: 1px solid var(--gray-100);';
        item.innerHTML = `<strong>${result.name}</strong><br><small class="text-muted">${result.description || ''}</small>`;
        item.addEventListener('click', () => {
            input.value = result.name;
            hideAutocomplete(input);
            if (input.onautocompleteselect) {
                input.onautocompleteselect(result);
            }
        });
        dropdown.appendChild(item);
    });

    // Position relative to input
    const parent = input.parentElement;
    parent.style.position = 'relative';
    parent.appendChild(dropdown);
}

function hideAutocomplete(input) {
    const dropdown = input.parentElement.querySelector('.autocomplete-dropdown');
    if (dropdown) {
        dropdown.remove();
    }
}

// Event Listeners
function setupEventListeners() {
    // Assessment form navigation
    const assessmentForm = document.getElementById('assessment-form');
    if (assessmentForm) {
        setupAssessmentNavigation();
    }

    // Recommendation actions
    const recommendationCards = document.querySelectorAll('.recommendation-card');
    recommendationCards.forEach(card => {
        const bookmarkBtn = card.querySelector('[data-action="bookmark"]');
        if (bookmarkBtn) {
            bookmarkBtn.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                const careerName = this.dataset.career;
                bookmarkCareer(careerName, this);
            });
        }

        const exploreBtn = card.querySelector('[data-action="explore"]');
        if (exploreBtn) {
            exploreBtn.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                const careerName = this.dataset.career;
                window.location.href = `/career/${encodeURIComponent(careerName)}`;
            });
        }
    });

    // Copy to clipboard
    const copyButtons = document.querySelectorAll('[data-copy]');
    copyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetId = this.dataset.copy;
            const target = document.getElementById(targetId);
            if (target) {
                copyToClipboard(target.value || target.textContent);
                showToast('Copied to clipboard!', 'success');
            }
        });
    });

    // Modal confirmations
    const confirmButtons = document.querySelectorAll('[data-confirm]');
    confirmButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const message = this.dataset.confirm;
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });
}

// Assessment Form Navigation
function setupAssessmentNavigation() {
    const form = document.getElementById('assessment-form');
    const sections = form.querySelectorAll('.assessment-section');
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    const progressBar = document.getElementById('progress-bar');
    const currentStepSpan = document.getElementById('current-step');
    const stepTitleSpan = document.getElementById('step-title');
    const loadingOverlay = document.getElementById('loading-overlay');
    const currentStepInput = document.getElementById('current-step-input');

    let currentStep = 1;
    const totalSections = sections.length;

    // Section titles
    const sectionTitles = [
        'Personal Details',
        'Academic Skills',
        'Technical Skills',
        'Soft Skills',
        'Interests',
        'Experiences',
        'Certifications',
        'Career Goals'
    ];

    // Initialize range sliders
    const rangeSliders = form.querySelectorAll('input[type="range"]');
    rangeSliders.forEach(slider => {
        const valueDisplay = document.getElementById(slider.id + '-value');
        if (valueDisplay) {
            valueDisplay.textContent = slider.value;
            slider.addEventListener('input', () => {
                valueDisplay.textContent = slider.value;
            });
        }
    });

    function updateProgress() {
        const progressPercent = ((currentStep - 1) / (totalSections - 1)) * 100;
        progressBar.style.width = progressPercent + '%';
        progressBar.setAttribute('aria-valuenow', currentStep);
        currentStepSpan.textContent = currentStep;
        stepTitleSpan.textContent = sectionTitles[currentStep - 1];
        currentStepInput.value = currentStep;

        // Update button states
        prevBtn.disabled = currentStep === 1;
        nextBtn.textContent = currentStep === totalSections ? 'Get Recommendations' : 'Next Step';

        // Show/hide sections
        sections.forEach((section, index) => {
            if (index + 1 === currentStep) {
                section.classList.add('active');
                section.classList.remove('d-none');
            } else {
                section.classList.remove('active');
                section.classList.add('d-none');
            }
        });
    }

    // Previous button handler
    if (prevBtn) {
        prevBtn.addEventListener('click', () => {
            if (currentStep > 1) {
                currentStep--;
                updateProgress();
            }
        });
    }

    // Next button handler
    if (nextBtn) {
        nextBtn.addEventListener('click', function(e) {
            if (currentStep < totalSections) {
                // Validate current section before moving forward
                if (validateSection(currentStep, sections)) {
                    currentStep++;
                    updateProgress();
                }
            } else {
                // Final submission
                e.preventDefault();
                if (validateForm()) {
                    showLoading(loadingOverlay);
                    // Form will submit normally after this
                }
            }
        });
    }

    // Form submission
    form.addEventListener('submit', function(e) {
        if (currentStep < totalSections) {
            e.preventDefault();
            if (validateSection(currentStep, sections)) {
                currentStep++;
                updateProgress();
            }
        } else {
            // Final validation before submit
            if (!validateForm()) {
                e.preventDefault();
            } else {
                showLoading(loadingOverlay);
            }
        }
    });

    function validateSection(step, sections) {
        const section = sections[step - 1];
        const inputs = section.querySelectorAll('input[required], select[required], textarea[required]');
        let isValid = true;

        inputs.forEach(input => {
            if (!validateField(input)) {
                isValid = false;
            }
        });

        return isValid;
    }

    function validateForm() {
        let isValid = true;
        const allInputs = form.querySelectorAll('input[required], select[required], textarea[required]');

        allInputs.forEach(input => {
            if (!validateField(input)) {
                isValid = false;
            }
        });

        return isValid;
    }

    // Initialize
    updateProgress();
}

// Bookmark Career
function bookmarkCareer(careerName, button) {
    const formData = new FormData();
    formData.append('career_name', careerName);

    // Add CSRF token if available
    const csrfToken = document.querySelector('meta[name="csrf-token"]');
    if (csrfToken) {
        formData.append('csrf_token', csrfToken.content);
    }

    fetch('/api/bookmark', {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showToast('Career bookmarked successfully!', 'success');
            button.innerHTML = '<i class="fas fa-bookmark me-1"></i> Bookmarked';
            button.disabled = true;
            button.classList.remove('btn-outline-primary');
            button.classList.add('btn-success');
        } else {
            showToast('Failed to bookmark career', 'error');
        }
    })
    .catch(error => {
        console.error('Bookmark error:', error);
        showToast('An error occurred', 'error');
    });
}

// Copy to Clipboard
function copyToClipboard(text) {
    if (navigator.clipboard && window.isSecureContext) {
        return navigator.clipboard.writeText(text);
    } else {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        textArea.style.top = '-999999px';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        document.execCommand('copy');
        textArea.remove();
        return Promise.resolve();
    }
}

// Show Toast Notification
function showToast(message, type = 'info') {
    // Check if SweetAlert2 is available
    if (typeof Swal !== 'undefined') {
        const icons = {
            success: 'success',
            error: 'error',
            warning: 'warning',
            info: 'info'
        };

        Swal.fire({
            toast: true,
            position: 'top-end',
            icon: icons[type] || 'info',
            title: message,
            showConfirmButton: false,
            timer: 3000,
            timerProgressBar: true,
            background: '#fff',
            color: '#333',
            customClass: {
                popup: 'swal2-toast'
            }
        });
    } else {
        // Fallback to simple alert
        alert(message);
    }
}

// Loading Overlay
function showLoading(overlay) {
    if (overlay) {
        overlay.classList.remove('hidden');
    }
}

function hideLoading(overlay) {
    if (overlay) {
        overlay.classList.add('hidden');
    }
}

// Export Functions
function exportToPDF() {
    showToast('Generating PDF...', 'info');
    // Implementation would call API endpoint
    window.location.href = '/api/export/pdf';
}

function printRecommendation() {
    window.print();
}

// Utility Functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(amount);
}

function formatNumber(num) {
    return new Intl.NumberFormat('en-US').format(num);
}

// Initialize on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
        // Already handled above
    });
} else {
    // DOM already loaded
    initializeTheme();
    initializeTooltips();
    initializeDropdowns();
    initializeFormValidation();
    initializeRangeSliders();
    initializeCharts();
    initializeProgressBars();
    initializeLoadingStates();
    initializeSearchAutocomplete();
    setupEventListeners();
}