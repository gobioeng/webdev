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

// Scroll-based header behavior
function handleHeaderScroll() {
    const header = document.querySelector('header');
    if (window.scrollY > 50) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
}

// Lazy loading for images
function handleLazyLoading() {
    const images = document.querySelectorAll('img[loading="lazy"]');
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src || img.src;
                    img.classList.add('loaded');
                    observer.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    } else {
        // Fallback for older browsers
        images.forEach(img => {
            img.src = img.dataset.src || img.src;
            img.classList.add('loaded');
        });
    }
}

// Handle missing images with placeholders
function handleMissingImages() {
    const images = document.querySelectorAll('img');
    
    images.forEach(img => {
        img.addEventListener('error', function() {
            if (!this.classList.contains('placeholder-handled')) {
                this.classList.add('placeholder-handled');
                
                // Create placeholder div
                const placeholder = document.createElement('div');
                placeholder.className = 'image-placeholder';
                placeholder.style.width = this.style.width || this.getAttribute('width') || '100%';
                placeholder.style.height = this.style.height || this.getAttribute('height') || '200px';
                placeholder.innerHTML = '<i class="fas fa-image"></i><br>Image placeholder';
                
                // Replace image with placeholder
                this.parentNode.replaceChild(placeholder, this);
            }
        });
    });
}

// Smooth scroll for anchor links
function handleSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Intersection Observer for animations
function handleScrollAnimations() {
    const animatedElements = document.querySelectorAll('.feature-card, .article-card, .resource-card, .member-card');
    
    if ('IntersectionObserver' in window) {
        const animationObserver = new IntersectionObserver((entries) => {
            entries.forEach((entry, index) => {
                if (entry.isIntersecting) {
                    // Stagger animation for member cards
                    if (entry.target.classList.contains('member-card')) {
                        setTimeout(() => {
                            entry.target.classList.add('animate-in');
                        }, index * 150); // 150ms delay between each card
                    } else {
                        entry.target.style.opacity = '1';
                        entry.target.style.transform = 'translateY(0)';
                    }
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });
        
        animatedElements.forEach(el => {
            if (!el.classList.contains('member-card')) {
                el.style.opacity = '0';
                el.style.transform = 'translateY(30px)';
                el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            }
            animationObserver.observe(el);
        });
    }
}

// Member popup functionality
function openMemberPopup(memberElement) {
    const memberData = {
        name: memberElement.querySelector('.member-name').textContent,
        designation: memberElement.querySelector('.member-designation').textContent,
        company: memberElement.querySelector('.member-company').textContent,
        avatar: getImageSrc(memberElement),
        interests: Array.from(memberElement.querySelectorAll('.interest-tag')).map(tag => tag.textContent),
        extendedInfo: memberElement.querySelector('.member-extended-info')
    };

    // Populate popup
    document.getElementById('popupName').textContent = memberData.name;
    document.getElementById('popupDesignation').textContent = memberData.designation;
    document.getElementById('popupCompany').textContent = memberData.company;
    
    const popupAvatar = document.getElementById('popupAvatar');
    if (popupAvatar) {
        popupAvatar.src = memberData.avatar;
        popupAvatar.alt = memberData.name;
    }

    // Extended bio
    const bioContent = memberData.extendedInfo.querySelector('.extended-bio').innerHTML;
    document.getElementById('popupBio').innerHTML = bioContent;

    // Hobbies
    const hobbiesContent = memberData.extendedInfo.querySelector('.extended-hobbies').innerHTML;
    document.getElementById('popupHobbies').innerHTML = hobbiesContent;

    // Interests
    const interestsHtml = memberData.interests.map(interest => 
        `<span class="interest-tag">${interest}</span>`
    ).join('');
    document.getElementById('popupInterests').innerHTML = '<h4>Expertise</h4>' + interestsHtml;

    // Social links
    const basicSocial = memberElement.querySelector('.member-social').innerHTML;
    const extendedSocial = memberData.extendedInfo.querySelector('.extended-social').innerHTML;
    document.getElementById('popupBasicSocial').innerHTML = basicSocial;
    document.getElementById('popupExtendedSocial').innerHTML = extendedSocial;

    // Show popup
    const popup = document.getElementById('memberPopup');
    popup.style.display = 'flex';
    setTimeout(() => {
        popup.classList.add('show');
    }, 10);
    
    document.body.style.overflow = 'hidden';
}

function getImageSrc(memberElement) {
    const img = memberElement.querySelector('.member-avatar img');
    if (img && img.src) {
        return img.src;
    }
    // Fallback for when image is replaced with placeholder
    return 'https://via.placeholder.com/120x120/0053b3/ffffff?text=USER';
}

function closeMemberPopup() {
    const popup = document.getElementById('memberPopup');
    popup.classList.remove('show');
    setTimeout(() => {
        popup.style.display = 'none';
    }, 300);
    document.body.style.overflow = '';
}

// Initialize member card click handlers
function initializeMemberCards() {
    const memberCards = document.querySelectorAll('.member-card');
    memberCards.forEach(card => {
        card.addEventListener('click', (e) => {
            // Prevent opening popup if clicking on social links
            if (e.target.closest('.social-icon')) {
                return;
            }
            openMemberPopup(card);
        });
    });
}

// --- Mobile Nav: Collapse on link click or scroll (for mobile view) ---
document.addEventListener('DOMContentLoaded', function() {
    const mobileMenu = document.getElementById('mobileMenu');
    if (mobileMenu) {
        // Collapse menu when any nav link is clicked
        mobileMenu.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', function() {
                // Only collapse if the menu is open
                if (window.innerWidth <= 768 && mobileMenu.style.display === 'block') {
                    mobileMenu.style.display = 'none';
                }
            });
        });
    }

    // Collapse mobile menu on scroll
    window.addEventListener('scroll', function() {
        if (window.innerWidth <= 768 && mobileMenu && mobileMenu.style.display === 'block') {
            mobileMenu.style.display = 'none';
        }
    });
});

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

    // Initialize all functionality
    handleLazyLoading();
    handleMissingImages();
    handleSmoothScroll();
    handleScrollAnimations();
    
    // Initialize member cards if on members page
    if (document.querySelector('.members-grid')) {
        initializeMemberCards();
    }
    
    // Add scroll listener for header
    window.addEventListener('scroll', handleHeaderScroll);

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
    
    // Close modals when clicking outside or pressing escape
    const modals = document.querySelectorAll('.modal, .member-popup-overlay');
    modals.forEach(modal => {
        modal.addEventListener('click', (event) => {
            if (event.target === modal) {
                if (modal.classList.contains('member-popup-overlay')) {
                    closeMemberPopup();
                } else {
                    modal.style.display = 'none';
                    document.body.style.overflow = '';
                }
            }
        });
    });

    // Close popup on escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            const memberPopup = document.getElementById('memberPopup');
            if (memberPopup && memberPopup.style.display === 'flex') {
                closeMemberPopup();
            }
        }
    });
});
