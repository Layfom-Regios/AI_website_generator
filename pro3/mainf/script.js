
// Smooth scrolling for navigation links
document.querySelectorAll('nav ul li a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();

        const targetId = this.getAttribute('href');
        const targetElement = document.querySelector(targetId);

        if (targetElement) {
            targetElement.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Optional: Add a subtle animation to elements as they scroll into view
const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            observer.unobserve(entry.target); // Stop observing once visible
        }
    });
}, { threshold: 0.1 }); // Trigger when 10% of the element is visible

document.querySelectorAll('section > div > h2, .about-content, .skills-grid, .project-card, .skill-item, .contact-info').forEach(element => {
    observer.observe(element);
});

// Add a CSS class for visible elements
// In your CSS, you'd add a rule like:
// .is-visible { opacity: 1; transform: translateY(0); transition: opacity 0.6s ease-out, transform 0.6s ease-out; }
// And the initial state for these elements would be:
// opacity: 0; transform: translateY(20px);
