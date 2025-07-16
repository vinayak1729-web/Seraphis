let currentQuestion = 1;
const totalQuestions = document.querySelectorAll('.question-container').length;

// Show initial question
document.querySelector(`[data-question="1"]`).classList.add('active');

function handleOptionSelect() {
    updateProgress();

    // Auto-progress to next question if not the last question
    const currentContainer = document.querySelector('.question-container.active');
    const currentQuestionNumber = parseInt(currentContainer.dataset.question);

    if (currentQuestionNumber < totalQuestions) {
        setTimeout(() => {
            showQuestion(currentQuestionNumber + 1);
        }, 500); // Half second delay before moving to next question
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
    const answeredQuestions = document.querySelectorAll('input[type="radio"]:checked').length;
    const progressPercentage = (answeredQuestions / totalQuestions) * 100;

    document.getElementById('progress').style.width = progressPercentage + '%';
    document.getElementById('progress-percentage').textContent = Math.round(progressPercentage);
}

updateProgress();