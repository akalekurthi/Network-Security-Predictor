// Theme Toggle
document.querySelector('.theme-toggle').addEventListener('click', () => {
    const body = document.body;
    const currentTheme = body.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    
    body.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    
    // Update icon
    const icon = document.querySelector('.theme-toggle i');
    icon.className = newTheme === 'light' ? 'fas fa-moon' : 'fas fa-sun';
});

// Form Submission
document.getElementById('detection-form')?.addEventListener('submit', (e) => {
    const button = document.getElementById('analyze-btn');
    const spinner = button.querySelector('.spinner-border');
    
    // Show loading state
    button.disabled = true;
    spinner.classList.remove('d-none');
});

// Theme Toggle - Single unified implementation
document.addEventListener('DOMContentLoaded', function() {
    // Create theme toggle button if it doesn't exist
    let themeToggle = document.querySelector('.theme-toggle');
    if (!themeToggle) {
        themeToggle = document.createElement('button');
        themeToggle.className = 'theme-toggle';
        themeToggle.title = 'Toggle dark/light mode';
        themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
        document.body.appendChild(themeToggle);
    }
    
    // Check for saved theme
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.body.setAttribute('data-theme', savedTheme);
    
    // Update the icon based on current theme
    const themeToggleIcon = themeToggle.querySelector('i');
    if (themeToggleIcon) {
        themeToggleIcon.className = savedTheme === 'light' ? 'fas fa-moon' : 'fas fa-sun';
    }
    
    // Theme toggle functionality
    themeToggle.addEventListener('click', function() {
        const currentTheme = document.body.getAttribute('data-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        
        document.body.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        
        // Update icon
        const icon = themeToggle.querySelector('i');
        if (icon) {
            icon.className = newTheme === 'light' ? 'fas fa-moon' : 'fas fa-sun';
        }
    });
});
