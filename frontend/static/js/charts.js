/**
 * Chart.js Visualizations for Student Assessment Results.
 * Renders Multi-Dimensional Radar Aptitude Chart and Bar Chart for Interests
 * with dynamic Light/Dark mode adaptability.
 */

let activeRadarChart = null;
let activeBarChart = null;
let lastCognitiveData = null;
let lastInterestData = null;

function getChartColors() {
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    return {
        textColor: isDark ? '#CBD5E1' : '#334155',
        gridColor: isDark ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.08)',
        radarFill: isDark ? 'rgba(118, 146, 255, 0.25)' : 'rgba(27, 44, 193, 0.15)',
        radarBorder: isDark ? '#7692FF' : '#1B2CC1',
        radarPoint: isDark ? '#98ACFF' : '#15229E'
    };
}

function renderAssessmentCharts(cognitiveData, interestData) {
    lastCognitiveData = cognitiveData || lastCognitiveData;
    lastInterestData = interestData || lastInterestData;

    const colors = getChartColors();

    // 1. Radar Chart: Cognitive & Aptitude Strengths
    const radarCtx = document.getElementById('cognitiveRadarChart');
    if (radarCtx && lastCognitiveData) {
        if (activeRadarChart) {
            activeRadarChart.destroy();
        }

        const labels = [
            'Math Ability',
            'Logical Reasoning',
            'Scientific Thinking',
            'Problem Solving',
            'Analytical Ability',
            'Communication',
            'Creativity',
            'Digital Ability',
            'Learning Agility'
        ];

        const values = [
            lastCognitiveData.mathematical_ability || 50,
            lastCognitiveData.logical_reasoning || 50,
            lastCognitiveData.scientific_reasoning || 50,
            lastCognitiveData.problem_solving || 50,
            lastCognitiveData.analytical_ability || 50,
            lastCognitiveData.communication || 50,
            lastCognitiveData.creativity || 50,
            lastCognitiveData.digital_ability || 50,
            lastCognitiveData.learning_ability || 50
        ];

        activeRadarChart = new Chart(radarCtx, {
            type: 'radar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Demonstrated Aptitude',
                    data: values,
                    backgroundColor: colors.radarFill,
                    borderColor: colors.radarBorder,
                    pointBackgroundColor: colors.radarPoint,
                    pointBorderColor: '#FFFFFF',
                    pointHoverBackgroundColor: '#FFFFFF',
                    pointHoverBorderColor: colors.radarBorder,
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    r: {
                        angleLines: { color: colors.gridColor },
                        grid: { color: colors.gridColor },
                        pointLabels: {
                            font: { size: 11, family: "'Inter', sans-serif", weight: '600' },
                            color: colors.textColor
                        },
                        suggestedMin: 0,
                        suggestedMax: 100,
                        ticks: {
                            stepSize: 20,
                            display: true,
                            backdropColor: 'transparent',
                            color: colors.textColor
                        }
                    }
                },
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        padding: 10,
                        cornerRadius: 6
                    }
                }
            }
        });
    }

    // 2. Bar Chart: Disciplinary & Career Interests
    const barCtx = document.getElementById('interestBarChart');
    if (barCtx && lastInterestData) {
        if (activeBarChart) {
            activeBarChart.destroy();
        }

        const intLabels = [
            'Technology',
            'Engineering',
            'Healthcare',
            'Business',
            'Finance',
            'Arts & Creative',
            'Research'
        ];

        const intValues = [
            lastInterestData.technology_interest || 50,
            lastInterestData.engineering_interest || lastInterestData.science_interest || 50,
            lastInterestData.healthcare_interest || 50,
            lastInterestData.business_interest || 50,
            lastInterestData.finance_interest || 50,
            lastInterestData.arts_interest || lastInterestData.creative_interest || 50,
            lastInterestData.research_interest || 50
        ];

        // Solid flat colors (No gradients)
        const barColors = [
            '#1B2CC1', '#2563EB', '#15803D', '#B45309', '#7C3AED', '#DB2777', '#0891B2'
        ];

        activeBarChart = new Chart(barCtx, {
            type: 'bar',
            data: {
                labels: intLabels,
                datasets: [{
                    label: 'Affinity Score (0-100)',
                    data: intValues,
                    backgroundColor: barColors,
                    borderRadius: 4,
                    borderSkipped: false
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        grid: { color: colors.gridColor },
                        ticks: {
                            stepSize: 20,
                            color: colors.textColor,
                            font: { family: "'Inter', sans-serif" }
                        }
                    },
                    x: {
                        grid: { display: false },
                        ticks: {
                            font: { size: 11, family: "'Inter', sans-serif", weight: '500' },
                            color: colors.textColor
                        }
                    }
                },
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        padding: 10,
                        cornerRadius: 6
                    }
                }
            }
        });
    }
}

// Listen to theme changes to re-render charts dynamically
window.addEventListener('themechange', () => {
    if (lastCognitiveData || lastInterestData) {
        renderAssessmentCharts(lastCognitiveData, lastInterestData);
    }
});

window.renderAssessmentCharts = renderAssessmentCharts;
