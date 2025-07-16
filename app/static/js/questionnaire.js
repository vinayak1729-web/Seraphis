let currentStep = 1;
const totalSteps = 3;

// Update counter initially
updateCounter();

// Handle Enter key for all inputs
document.querySelectorAll('input, select').forEach(input => {
    input.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            if (this.value) {
                const currentButton = document.querySelector(`[data-step="${currentStep}"] .next-btn`);
                if (currentButton) {
                    currentButton.click();
                }
            }
        }
    });
});

// Handle next button clicks
document.querySelectorAll('.next-btn').forEach(button => {
    button.addEventListener('click', function(e) {
        e.preventDefault();
        const currentContainer = document.querySelector(`[data-step="${currentStep}"]`);
        const inputs = currentContainer.querySelectorAll('input:not([style*="display: none"]), select:not([style*="display: none"]');

        // Validate current inputs
        let isValid = true;
        inputs.forEach(input => {
            if (input.required && !input.value) {
                isValid = false;
            }
        });

        if (isValid) {
            if (currentStep < totalSteps) {
                currentStep++;
                updateUI();
            } else if (currentStep === totalSteps) {
                // For the last step, make sure the occupation is properly set
                const occupationSelect = document.getElementById('occupationSelect');
                const otherInput = document.getElementById('otherOccupation');

                if (occupationSelect.value === 'Other' && otherInput.value) {
                    // If "Other" is selected, use the text input value
                    document.getElementById('questionnaireForm').submit();
                } else if (occupationSelect.value && occupationSelect.value !== 'Other') {
                    // If a regular option is selected
                    document.getElementById('questionnaireForm').submit();
                }
            }
        }
    });
});

// Handle occupation select
document.getElementById('occupationSelect').addEventListener('change', function() {
    const otherInput = document.getElementById('otherOccupation');
    if (this.value === 'Other') {
        otherInput.style.display = 'block';
        otherInput.required = true;
        this.required = false;
    } else {
        otherInput.style.display = 'none';
        otherInput.required = false;
        otherInput.value = '';
        this.required = true;
    }
});

function updateCounter() {
    document.querySelector('.question-counter .current').textContent = currentStep;
    document.querySelector('.question-counter .total').textContent = totalSteps;
}

function updateUI() {
    updateCounter();

    const currentQuestion = document.querySelector('.question-container.active');
    const nextQuestion = document.querySelector(`[data-step="${currentStep}"]`);

    if (currentQuestion) {
        currentQuestion.classList.add('exit');
        currentQuestion.addEventListener('animationend', function handler() {
            currentQuestion.classList.remove('active', 'exit');
            nextQuestion.classList.add('active');
            currentQuestion.removeEventListener('animationend', handler);
        });
    } else {
        nextQuestion.classList.add('active');
    }
}

// Enhanced select event listeners
document.querySelectorAll('.custom-select').forEach(select => {
    // Initial state setup
    if (select.value === '') {
        select.style.color = '#999';
    }

    select.addEventListener('change', function() {
        const selectedOption = this.options[this.selectedIndex];

        // Update select styling when an option is chosen
        if (this.value) {
            this.style.color = '#2c3e50';
            this.style.fontWeight = 'bold';
        } else {
            this.style.color = '#999';
            this.style.fontWeight = 'normal';
        }

        // Handle occupation specific logic
        if (this.id === 'occupationSelect') {
            const otherInput = document.getElementById('otherOccupation');

            if (this.value === 'Other') {
                otherInput.style.display = 'block';
                otherInput.required = true;
                this.required = false;
            } else {
                otherInput.style.display = 'none';
                otherInput.required = false;
                otherInput.value = '';
                this.required = true;
            }
        }

        // Add visual feedback for selection
        this.style.borderColor = '#00C9FF';
        setTimeout(() => {
            this.style.borderColor = '#e0e0e0';
        }, 300);
    });

    // Add focus effects
    select.addEventListener('focus', function() {
        this.style.borderColor = '#00C9FF';
    });

    select.addEventListener('blur', function() {
        this.style.borderColor = '#e0e0e0';
    });
});