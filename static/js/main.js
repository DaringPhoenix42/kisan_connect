// Main JavaScript file for Kisan Mitra

// Global variables
let currentLocation = 'Nashik';
let isProcessing = false;
let currentTheme = 'light';

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    console.log('Kisan Mitra - Farmer\'s Friend initialized');
    
    // Initialize theme system
    initializeTheme();
    
    // Add fade-in animations to elements
    addFadeInAnimations();
    
    // Initialize tooltips
    initializeTooltips();
    
    // Set current date
    updateCurrentDate();
    
    // Initialize location detection
    detectLocation();
    
    // Initialize theme toggle
    initializeThemeToggle();

    // Initialize footer functionality
    initializeFooter();
});

// ===== THEME MANAGEMENT =====
function initializeTheme() {
    // Get saved theme from localStorage or default to light
    const savedTheme = Storage.get('theme') || 'light';
    
    // Ensure the theme is properly set
    setTheme(savedTheme);
    
    // Add a fallback to ensure theme is applied
    setTimeout(() => {
        if (!document.documentElement.getAttribute('data-theme')) {
            setTheme('light');
        }
    }, 100);
}

function initializeThemeToggle() {
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
    }
}

function toggleTheme() {
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
}

function setTheme(theme) {
    currentTheme = theme;
    
    // Update HTML data attribute
    document.documentElement.setAttribute('data-theme', theme);
    
    // Save to localStorage
    Storage.set('theme', theme);
    
    // Update theme toggle button state
    updateThemeToggleButton();
    
    // Trigger theme change event
    document.dispatchEvent(new CustomEvent('themeChange', { detail: { theme } }));
    
    // Force a repaint to ensure all styles are applied
    document.body.style.display = 'none';
    document.body.offsetHeight; // Trigger reflow
    document.body.style.display = '';
    
    console.log(`Theme changed to: ${theme}`);
}

function updateThemeToggleButton() {
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        const lightIcon = themeToggle.querySelector('.light-icon');
        const darkIcon = themeToggle.querySelector('.dark-icon');
        
        if (currentTheme === 'dark') {
            lightIcon.style.opacity = '0';
            darkIcon.style.opacity = '1';
        } else {
            lightIcon.style.opacity = '1';
            darkIcon.style.opacity = '0';
        }
    }
}

// ===== ANIMATIONS =====
function addFadeInAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
            }
        });
    }, observerOptions);
    
    // Observe all cards and sections
    document.querySelectorAll('.feature-card, .crop-card, .form-container, .results-container, .card').forEach(el => {
        observer.observe(el);
    });
}

// ===== UTILITIES =====
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

function updateCurrentDate() {
    const dateElements = document.querySelectorAll('.current-date');
    const currentDate = new Date().toLocaleDateString('en-IN', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
    
    dateElements.forEach(element => {
        element.textContent = currentDate;
    });
}

function detectLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            function(position) {
                console.log('Location detected:', position.coords);
                currentLocation = 'Nashik'; // Default for demo
            },
            function(error) {
                console.log('Location detection failed:', error);
                currentLocation = 'Nashik'; // Default fallback
            }
        );
    } else {
        currentLocation = 'Nashik'; // Default fallback
    }
}

// ===== LOADING STATES =====
function showLoading(element) {
    if (element) {
        element.innerHTML = '<div class="loading"></div> Processing...';
        element.disabled = true;
    }
    isProcessing = true;
}

function hideLoading(element, originalText) {
    if (element) {
        element.innerHTML = originalText;
        element.disabled = false;
    }
    isProcessing = false;
}

// ===== NOTIFICATIONS =====
function showSuccess(message, duration = 3000) {
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-success alert-dismissible fade show';
    alertDiv.innerHTML = `
        <i class="fas fa-check-circle me-2"></i>${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    showNotification(alertDiv, duration);
}

function showError(message, duration = 5000) {
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-danger alert-dismissible fade show';
    alertDiv.innerHTML = `
        <i class="fas fa-exclamation-triangle me-2"></i>${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    showNotification(alertDiv, duration);
}

function showInfo(message, duration = 4000) {
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-info alert-dismissible fade show';
    alertDiv.innerHTML = `
        <i class="fas fa-info-circle me-2"></i>${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    showNotification(alertDiv, duration);
}

function showWarning(message, duration = 4000) {
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-warning alert-dismissible fade show';
    alertDiv.innerHTML = `
        <i class="fas fa-exclamation-triangle me-2"></i>${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    showNotification(alertDiv, duration);
}

function showNotification(alertDiv, duration) {
    // Insert at the top of the main content
    const mainContent = document.querySelector('.main-content');
    if (mainContent) {
        mainContent.insertBefore(alertDiv, mainContent.firstChild);
        
        // Auto-remove after duration
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, duration);
    }
}

// ===== FORMATTING =====
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR',
        minimumFractionDigits: 0
    }).format(amount);
}

function formatPercentage(value) {
    return `${value}%`;
}

function formatNumber(number) {
    return new Intl.NumberFormat('en-IN').format(number);
}

// ===== FORM VALIDATION =====
function validateForm(formElement) {
    const inputs = formElement.querySelectorAll('input[required], select[required], textarea[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

function clearFormValidation(formElement) {
    const inputs = formElement.querySelectorAll('.is-invalid');
    inputs.forEach(input => {
        input.classList.remove('is-invalid');
    });
}

// ===== FILE HANDLING =====
function handleFileUpload(input, previewElement) {
    const file = input.files[0];
    if (file) {
        // Validate file type
        const allowedTypes = ['image/jpeg', 'image/png', 'image/gif'];
        if (!allowedTypes.includes(file.type)) {
            showError('Please select a valid image file (JPEG, PNG, or GIF)');
            input.value = '';
            return false;
        }
        
        // Validate file size (max 5MB)
        if (file.size > 5 * 1024 * 1024) {
            showError('File size should be less than 5MB');
            input.value = '';
            return false;
        }
        
        // Show preview
        if (previewElement) {
            const reader = new FileReader();
            reader.onload = function(e) {
                previewElement.src = e.target.result;
                previewElement.style.display = 'block';
            };
            reader.readAsDataURL(file);
        }
        
        return true;
    }
    return false;
}

// ===== NAVIGATION =====
function scrollToElement(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// ===== UTILITY FUNCTIONS =====
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

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// ===== STORAGE UTILITIES =====
const Storage = {
    set: function(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
        } catch (e) {
            console.error('Error saving to localStorage:', e);
        }
    },
    
    get: function(key) {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : null;
        } catch (e) {
            console.error('Error reading from localStorage:', e);
            return null;
        }
    },
    
    remove: function(key) {
        try {
            localStorage.removeItem(key);
        } catch (e) {
            console.error('Error removing from localStorage:', e);
        }
    },
    
    clear: function() {
        try {
            localStorage.clear();
        } catch (e) {
            console.error('Error clearing localStorage:', e);
        }
    }
};

// ===== API UTILITIES =====
const API = {
    async get(url, params = {}) {
        try {
            const queryString = new URLSearchParams(params).toString();
            const fullUrl = queryString ? `${url}?${queryString}` : url;
            
            const response = await fetch(fullUrl);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('API GET error:', error);
            throw error;
        }
    },
    
    async post(url, data = {}) {
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('API POST error:', error);
            throw error;
        }
    },
    
    async uploadFile(url, formData) {
        try {
            const response = await fetch(url, {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('API Upload error:', error);
            throw error;
        }
    }
};

// ===== UI ENHANCEMENTS =====
function addSmoothScrolling() {
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

function addBackToTopButton() {
    const backToTopBtn = document.createElement('button');
    backToTopBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
    backToTopBtn.className = 'btn btn-primary position-fixed';
    backToTopBtn.style.cssText = 'bottom: 20px; right: 20px; z-index: 1000; width: 50px; height: 50px; border-radius: 50%; display: none;';
    backToTopBtn.onclick = scrollToTop;
    
    document.body.appendChild(backToTopBtn);
    
    // Show/hide based on scroll position
    window.addEventListener('scroll', throttle(() => {
        if (window.pageYOffset > 300) {
            backToTopBtn.style.display = 'block';
        } else {
            backToTopBtn.style.display = 'none';
        }
    }, 100));
}

// ===== FOOTER FUNCTIONALITY =====

// Newsletter subscription
function initializeNewsletterForm() {
    const newsletterForm = document.querySelector('.newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const emailInput = this.querySelector('.newsletter-input');
            const email = emailInput.value.trim();
            
            if (!email) {
                showError('Please enter your email address');
                return;
            }
            
            if (!isValidEmail(email)) {
                showError('Please enter a valid email address');
                return;
            }
            
            // Simulate newsletter subscription
            const submitBtn = this.querySelector('.newsletter-btn');
            const originalText = submitBtn.innerHTML;
            
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Subscribing...';
            submitBtn.disabled = true;
            
            setTimeout(() => {
                showSuccess('Thank you for subscribing to our newsletter! You\'ll receive updates about farming tips and market insights.');
                emailInput.value = '';
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            }, 2000);
        });
    }
}

// Email validation
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Social media links functionality
function initializeSocialLinks() {
    const socialIcons = document.querySelectorAll('.social-icon');
    
    socialIcons.forEach(icon => {
        icon.addEventListener('click', function(e) {
            e.preventDefault();
            
            const platform = this.getAttribute('title');
            const url = this.getAttribute('href');
            
            if (url === '#') {
                // Show platform-specific messages for demo
                const messages = {
                    'Facebook': 'Connect with us on Facebook for daily farming tips and community updates!',
                    'Twitter': 'Follow us on Twitter for real-time market updates and agricultural news!',
                    'Instagram': 'Follow us on Instagram for beautiful farm photos and success stories!',
                    'YouTube': 'Subscribe to our YouTube channel for farming tutorials and expert advice!',
                    'LinkedIn': 'Connect with us on LinkedIn for professional agricultural networking!',
                    'WhatsApp': 'Join our WhatsApp group for instant farming support and community chat!'
                };
                
                showInfo(messages[platform] || `Connect with us on ${platform}!`);
            } else {
                window.open(url, '_blank');
            }
        });
    });
}

// Footer link functionality
function initializeFooterLinks() {
    const footerLinks = document.querySelectorAll('.footer-link');
    
    footerLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            if (href === '#') {
                e.preventDefault();
                const linkText = this.textContent.trim();
                
                // Show appropriate messages for demo links
                const messages = {
                    'Help Center': 'Our comprehensive help center is coming soon! You\'ll find detailed guides and FAQs.',
                    'User Guide': 'Detailed user guides and tutorials will be available soon to help you make the most of Kisan Mitra.',
                    'Contact Us': 'Get in touch with our support team for personalized assistance with your farming needs.',
                    'Report Issue': 'Help us improve by reporting any issues you encounter while using the platform.',
                    'Feature Request': 'Have an idea for a new feature? We\'d love to hear from you!',
                    'Download App': 'Our mobile app is coming soon! Stay tuned for updates.'
                };
                
                showInfo(messages[linkText] || `The ${linkText} feature is coming soon!`);
            }
        });
    });
}

// Footer bottom links functionality
function initializeFooterBottomLinks() {
    const bottomLinks = document.querySelectorAll('.footer-bottom-link');
    
    bottomLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const linkText = this.textContent.trim();
            
            const messages = {
                'Privacy Policy': 'Our privacy policy ensures your data is protected and used responsibly.',
                'Terms of Service': 'Our terms of service outline the rules and guidelines for using Kisan Mitra.',
                'Cookie Policy': 'We use cookies to enhance your experience and provide personalized content.',
                'Sitemap': 'Navigate through all our pages and features with our comprehensive sitemap.'
            };
            
            showInfo(messages[linkText] || `The ${linkText} page is coming soon!`);
        });
    });
}

// Contact information functionality
function initializeContactInfo() {
    const contactItems = document.querySelectorAll('.contact-item');
    
    contactItems.forEach(item => {
        item.addEventListener('click', function() {
            const icon = this.querySelector('i');
            const text = this.querySelector('span').textContent;
            
            if (icon.classList.contains('fa-phone')) {
                showInfo(`Call us at ${text} for immediate support. Our team is available during business hours.`);
            } else if (icon.classList.contains('fa-envelope')) {
                showInfo(`Email us at ${text} for detailed inquiries. We typically respond within 24 hours.`);
            } else if (icon.classList.contains('fa-map-marker-alt')) {
                showInfo(`Visit us at ${text}. We welcome farmers to our office for in-person consultations.`);
            } else if (icon.classList.contains('fa-clock')) {
                showInfo(`Our support hours: ${text}. We're here to help you during these times.`);
            }
        });
    });
}

// Footer animations
function initializeFooterAnimations() {
    const footer = document.querySelector('.footer');
    if (footer) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });
        
        observer.observe(footer);
    }
}

// Initialize all footer functionality
function initializeFooter() {
    initializeNewsletterForm();
    initializeSocialLinks();
    initializeFooterLinks();
    initializeFooterBottomLinks();
    initializeContactInfo();
    initializeFooterAnimations();
}

// ===== INITIALIZATION =====
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Kisan Mitra - Initializing application...');
    
    // Initialize theme
    initializeTheme();
    
    // Initialize all components
    addSmoothScrolling();
    addBackToTopButton();
    ensureLinksWork();
    
    // Debug: Log that the page is loaded
    console.log('✅ Kisan Mitra page loaded successfully');
    
    // Test hero buttons specifically
    testHeroButtons();
});

// ===== HERO BUTTON TESTING =====
function testHeroButtons() {
    const heroButtons = document.querySelectorAll('.hero-section .btn');
    console.log(`🔍 Found ${heroButtons.length} hero buttons`);
    
    heroButtons.forEach((button, index) => {
        console.log(`Button ${index + 1}:`, {
            text: button.textContent.trim(),
            href: button.href,
            classes: button.className
        });
        
        // Add click event listener
        button.addEventListener('click', function(e) {
            console.log('🎯 Hero button clicked:', {
                text: this.textContent.trim(),
                href: this.href,
                target: this.target
            });
            
            // Prevent default only if we need to handle it manually
            // e.preventDefault();
            
            // Log the click for debugging
            console.log('📍 Navigating to:', this.href);
        });
    });
}

// ===== LINK VERIFICATION =====
function ensureLinksWork() {
    // Check if all navigation links are working
    const navLinks = document.querySelectorAll('a[href]');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            console.log('Link clicked:', this.href);
            // Let the default behavior happen
        });
    });
    
    // Check if all buttons are working
    const buttons = document.querySelectorAll('button');
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            console.log('Button clicked:', this.textContent.trim());
            // Let the default behavior happen
        });
    });
    
    // Special handling for main page hero buttons
    const heroButtons = document.querySelectorAll('.hero-section .btn');
    heroButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            console.log('Hero button clicked:', this.textContent.trim(), 'URL:', this.href);
            // Ensure the link works
            if (this.href) {
                window.location.href = this.href;
            }
        });
    });
    
    // Special handling for feature cards
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach(card => {
        card.addEventListener('click', function(e) {
            console.log('Feature card clicked:', this.querySelector('h3')?.textContent, 'URL:', this.href);
            // Ensure the link works
            if (this.href) {
                window.location.href = this.href;
            }
        });
    });
    
    console.log(`Found ${navLinks.length} links, ${buttons.length} buttons, ${heroButtons.length} hero buttons, and ${featureCards.length} feature cards`);
}

// ===== EXPORT FUNCTIONS =====
window.KisanMitra = {
    // Theme management
    setTheme,
    toggleTheme,
    currentTheme,
    
    // Loading states
    showLoading,
    hideLoading,
    
    // Notifications
    showSuccess,
    showError,
    showInfo,
    showWarning,
    
    // Formatting
    formatCurrency,
    formatPercentage,
    formatNumber,
    
    // Form handling
    validateForm,
    clearFormValidation,
    handleFileUpload,
    
    // Navigation
    scrollToElement,
    scrollToTop,
    
    // Utilities
    debounce,
    throttle,
    Storage,
    API,
    
    // Global variables
    currentLocation
}; 