let currentQuestion = 1;
const totalQuestions = document.querySelectorAll('.question-container').length;

// Show initial question
document.querySelector(`[data-question="1"]`).classList.add('active');

// Handle Enter key press
document.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        e.preventDefault();
        const currentInput = document.querySelector('.question-container.active input');
        if (currentInput && currentInput.value.trim()) {
            handleNextQuestion();
        }
    }
});

function handleNextQuestion() {
    const currentInput = document.querySelector('.question-container.active input');
    if (currentInput && currentInput.value.trim() && currentQuestion < totalQuestions) {
        showQuestion(currentQuestion + 1);
    }
}

function showQuestion(number) {
    const currentContainer = document.querySelector('.question-container.active');
    const nextContainer = document.querySelector(`[data-question="${number}"]`);

    if (currentContainer) {
        currentContainer.classList.add('exit');
        setTimeout(() => {
            currentContainer.classList.remove('active', 'exit');
            nextContainer.classList.add('active');
        }, 300);
    } else {
        nextContainer.classList.add('active');
    }

    currentQuestion = number;
    updateProgress();
}

function showPreviousQuestion() {
    if (currentQuestion > 1) {
        showQuestion(currentQuestion - 1);
    }
}

function updateProgress() {
    const filledInputs = Array.from(document.querySelectorAll('input[type="text"]'))
        .filter(input => input.value.trim() !== '').length;
    const progress = Math.floor((filledInputs / totalQuestions) * 100);

    document.getElementById('progress').style.width = `${progress}%`;
    document.getElementById('progress-percentage').textContent = `${progress}%`;
}