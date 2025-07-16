const tutorialSteps = [
    {
        icon: '<i class="fas fa-brain"></i>',
        title: 'AI Chat Support 🤖',
        description: 'Engage in supportive conversations with our empathetic AI assistant.'
    },
    {
        icon: '<i class="fas fa-microphone-alt"></i>',
        title: 'Voice Interaction 🎤',
        description: 'Natural voice conversations with emotion recognition technology.'
    },
    {
        icon: '<i class="fas fa-chart-line"></i>',
        title: 'Mood Tracking 📊',
        description: 'Monitor and understand your emotional patterns over time.'
    },
    {
        icon: '<i class="fas fa-meditation"></i>',
        title: 'Guided Meditation 🧘',
        description: 'Find peace with our guided breathing and meditation exercises.'
    },
    {
        icon: '<i class="fas fa-notes-medical"></i>',
        title: 'Health Analysis 🏥',
        description: 'Comprehensive mental health assessments and personalized insights.'
    },
    {
        icon: '<i class="fas fa-shield-alt"></i>',
        title: 'Privacy First 🔒',
        description: 'Your mental health data is encrypted and completely confidential.'
    }
];

// Tutorial System
class TutorialSystem {
    constructor(steps) {
        this.steps = steps;
        this.currentStep = 0;
        this.overlay = document.getElementById('tutorialOverlay');
        this.box = document.querySelector('.tutorial-box');
        this.closeBtn = document.querySelector('.tutorial-close');
        this.nextBtn = document.getElementById('tutorialNext');
        this.prevBtn = document.getElementById('tutorialPrev');
        this.progressContainer = document.querySelector('.tutorial-progress');

        this.initialize();
    }

    initialize() {
        // Setup event listeners
        document.getElementById('tutorialTrigger').addEventListener('click', () => this.show());
        this.closeBtn.addEventListener('click', () => this.hide());
        this.nextBtn.addEventListener('click', () => this.next());
        this.prevBtn.addEventListener('click', () => this.previous());
        this.overlay.addEventListener('click', (e) => {
            if (e.target === this.overlay) this.hide();
        });

        // Create progress indicators
        this.createProgressDots();
    }

    show() {
        this.overlay.style.display = 'flex';
        requestAnimationFrame(() => {
            this.overlay.classList.add('active');
            this.box.classList.add('active');
        });
        this.updateContent();
    }

    hide() {
        this.overlay.classList.remove('active');
        this.box.classList.remove('active');
        setTimeout(() => {
            this.overlay.style.display = 'none';
            this.currentStep = 0;
            this.updateContent();
        }, 300);
    }

    next() {
        if (this.currentStep < this.steps.length - 1) {
            this.currentStep++;
            this.updateContent();
            this.animateTransition('next');
        } else {
            this.hide();
        }
    }

    previous() {
        if (this.currentStep > 0) {
            this.currentStep--;
            this.updateContent();
            this.animateTransition('prev');
        }
    }

    updateContent() {
        const { icon, title, description } = this.steps[this.currentStep];

        // Update content with fade effect
        this.fadeContent(() => {
            document.getElementById('tutorialIcon').innerHTML = icon;
            document.getElementById('tutorialTitle').textContent = title;
            document.getElementById('tutorialContent').textContent = description;
        });

        // Update navigation
        this.prevBtn.style.visibility = this.currentStep === 0 ? 'hidden' : 'visible';
        this.nextBtn.textContent = this.currentStep === this.steps.length - 1 ? 'Get Started' : 'Next';

        // Update progress dots
        this.updateProgressDots();
    }

    fadeContent(callback) {
        const content = document.querySelector('.tutorial-content');
        content.style.opacity = '0';
        setTimeout(() => {
            callback();
            content.style.opacity = '1';
        }, 200);
    }

    animateTransition(direction) {
        const content = document.querySelector('.tutorial-content');
        content.style.transform = `translateX(${direction === 'next' ? '-10px' : '10px'})`;
        setTimeout(() => {
            content.style.transform = 'translateX(0)';
        }, 200);
    }

    createProgressDots() {
        this.progressContainer.innerHTML = this.steps.map((_, index) =>
            `<div class="progress-dot ${index === 0 ? 'active' : ''}" 
              onclick="tutorial.goToStep(${index})"></div>`
        ).join('');
    }

    updateProgressDots() {
        const dots = document.querySelectorAll('.progress-dot');
        dots.forEach((dot, index) => {
            dot.classList.toggle('active', index === this.currentStep);
        });
    }

    goToStep(step) {
        this.currentStep = step;
        this.updateContent();
    }
}

// Initialize the tutorial
const tutorial = new TutorialSystem(tutorialSteps);