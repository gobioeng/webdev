/**
 * GoBioEng Website Scripts
 */

// Mobile menu toggle
function toggleMenu() {
    const menu = document.getElementById('mobileMenu');
    if (menu.style.display === 'block') {
        menu.style.display = 'none';
    } else {
        menu.style.display = 'block';
    }
}

// Theme toggle
function toggleDarkMode() {
    const html = document.documentElement;
    if (html.getAttribute('data-theme') === 'dark') {
        html.removeAttribute('data-theme');
        localStorage.setItem('theme', 'light');
        document.querySelectorAll('.theme-toggle i').forEach(icon => {
            icon.className = 'fas fa-moon';
        });
    } else {
        html.setAttribute('data-theme', 'dark');
        localStorage.setItem('theme', 'dark');
        document.querySelectorAll('.theme-toggle i').forEach(icon => {
            icon.className = 'fas fa-sun';
        });
    }
}

// Set initial theme based on saved preference
document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
        document.documentElement.setAttribute('data-theme', 'dark');
        document.querySelectorAll('.theme-toggle i').forEach(icon => {
            icon.className = 'fas fa-sun';
        });
    }

    // Handle FAQ items
    const faqItems = document.querySelectorAll('.faq-item');
    if (faqItems.length > 0) {
        faqItems.forEach(item => {
            const question = item.querySelector('.faq-question');
            const answer = item.querySelector('.faq-answer');
            
            question.addEventListener('click', () => {
                // Toggle current item
                const isExpanded = item.classList.contains('active');
                
                // Close all items
                faqItems.forEach(faqItem => {
                    faqItem.classList.remove('active');
                    faqItem.querySelector('.faq-answer').style.maxHeight = null;
                });
                
                // If clicked item wasn't expanded, expand it
                if (!isExpanded) {
                    item.classList.add('active');
                    answer.style.maxHeight = answer.scrollHeight + 'px';
                }
            });
        });
    }

    // Modal handling
    window.openModal = function(modalId) {
        document.getElementById(modalId).style.display = 'flex';
        document.body.style.overflow = 'hidden';
    };
    
    window.closeModal = function(modalId) {
        document.getElementById(modalId).style.display = 'none';
        document.body.style.overflow = '';
    };
    
    // Close modals when clicking outside
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        modal.addEventListener('click', (event) => {
            if (event.target === modal) {
                modal.style.display = 'none';
                document.body.style.overflow = '';
            }
        });
    });
});
