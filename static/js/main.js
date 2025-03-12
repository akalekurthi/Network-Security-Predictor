// Animation for cards and elements
document.addEventListener('DOMContentLoaded', function() {
    // Init any animations or UI elements
    const cards = document.querySelectorAll('.card');

    cards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-5px)';
            card.style.boxShadow = '0 6px 12px rgba(0,0,0,0.15)';
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0)';
            card.style.boxShadow = '0 4px 8px rgba(0,0,0,0.1)';
        });
    });

    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Login page animation
    if (document.querySelector('.login-container')) {
        const formContainer = document.querySelector('.auth-form');
        formContainer.style.opacity = '0';
        formContainer.style.transform = 'translateY(20px)';

        setTimeout(() => {
            formContainer.style.opacity = '1';
            formContainer.style.transform = 'translateY(0)';
            formContainer.style.transition = 'all 0.5s ease';
        }, 200);
    }
});

// Form Submission
document.getElementById('detection-form')?.addEventListener('submit', (e) => {
    const button = document.getElementById('analyze-btn');
    const spinner = button.querySelector('.spinner-border');
    
    // Show loading state
    button.disabled = true;
    spinner.classList.remove('d-none');
});