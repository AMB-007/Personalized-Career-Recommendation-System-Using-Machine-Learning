/**
 * Main application JavaScript: Theme Switcher, Notifications, Form Handlers.
 */

// 1. Theme Management (Light / Dark)
(function initTheme() {
    const savedTheme = localStorage.getItem('app_theme');
    const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    const initialTheme = savedTheme || (prefersDark ? 'dark' : 'light');
    document.documentElement.setAttribute('data-theme', initialTheme);
})();

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('app_theme', newTheme);
    updateThemeToggleButtons(newTheme);

    // Dispatch global event for Chart.js updates
    window.dispatchEvent(new CustomEvent('themechange', { detail: { theme: newTheme } }));
}

function updateThemeToggleButtons(theme) {
    const toggles = document.querySelectorAll('.theme-toggle-btn');
    toggles.forEach(btn => {
        if (theme === 'dark') {
            btn.innerHTML = '<i class="bi bi-sun-fill text-warning me-1"></i> <span class="d-none d-sm-inline">Light</span>';
            btn.setAttribute('aria-label', 'Switch to light mode');
        } else {
            btn.innerHTML = '<i class="bi bi-moon-fill text-primary me-1"></i> <span class="d-none d-sm-inline">Dark</span>';
            btn.setAttribute('aria-label', 'Switch to dark mode');
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    // Sync theme buttons on load
    const activeTheme = document.documentElement.getAttribute('data-theme') || 'light';
    updateThemeToggleButtons(activeTheme);

    // Attach click listeners to all theme toggle buttons
    const themeButtons = document.querySelectorAll('.theme-toggle-btn');
    themeButtons.forEach(btn => {
        btn.addEventListener('click', toggleTheme);
    });

    // Dynamic stream selector toggle based on Class Level (for Register and Profile forms)
    const classSelect = document.getElementById('class_level');
    const streamContainer = document.getElementById('stream_container');
    const streamSelect = document.getElementById('stream');

    if (classSelect && streamContainer) {
        const updateStreamVisibility = () => {
            const classVal = parseInt(classSelect.value, 10);
            if (classVal >= 11) {
                streamContainer.style.display = 'block';
                if (streamSelect) streamSelect.required = true;
            } else {
                streamContainer.style.display = 'none';
                if (streamSelect) {
                    streamSelect.required = false;
                    streamSelect.value = 'General';
                }
            }
        };

        classSelect.addEventListener('change', updateStreamVisibility);
        updateStreamVisibility(); // initial run
    }

    // Auto-dismiss alerts after 5 seconds
    const autoDismissAlerts = document.querySelectorAll('.alert-dismissible');
    autoDismissAlerts.forEach(alertEl => {
        setTimeout(() => {
            if (window.bootstrap && window.bootstrap.Alert) {
                const bsAlert = bootstrap.Alert.getOrCreateInstance(alertEl);
                if (bsAlert) bsAlert.close();
            }
        }, 5000);
    });
});

window.toggleTheme = toggleTheme;
