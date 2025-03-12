// GSAP Animations
gsap.registerPlugin(ScrollTrigger);

// Card animations
gsap.from('.card', {
    duration: 0.6,
    opacity: 0,
    y: 30,
    stagger: 0.2,
    ease: 'power2.out'
});

// Result animation
if(document.querySelector('.result-animation')) {
    gsap.from('.result-icon', {
        duration: 0.5,
        scale: 0,
        opacity: 0,
        ease: 'back.out'
    });
    
    gsap.from('.result-details', {
        duration: 0.5,
        x: -30,
        opacity: 0,
        delay: 0.3,
        ease: 'power2.out'
    });
    
    gsap.from('.progress-bar', {
        duration: 1,
        width: 0,
        delay: 0.5,
        ease: 'power2.inOut'
    });
    
    // Recommendations animation
    gsap.from('.security-recommendations .card', {
        duration: 0.8,
        y: 50,
        opacity: 0,
        delay: 0.7,
        ease: 'power2.out'
    });
    
    gsap.from('.recommendation-list li', {
        duration: 0.5,
        x: -20,
        opacity: 0,
        stagger: 0.1,
        delay: 1,
        ease: 'power2.out'
    });
}

// Error page animation
if(document.querySelector('.error-card')) {
    gsap.from('.error-icon', {
        duration: 0.5,
        scale: 0,
        rotation: 180,
        ease: 'back.out'
    });
}
