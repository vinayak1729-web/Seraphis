function showComplete() {
    document.getElementById("judgeGemini").innerHTML = "Your feedback is complete!";
    setTimeout(function () {
        window.location.reload();
    }, 100);
}

class RatingSystem {
    constructor() {
        this.ratingElements = document.querySelectorAll('.rating input');
        this.username = document.querySelector('.rating').dataset.username;
        this.initialize();
    }

    initialize() {
        this.ratingElements.forEach(input => {
            input.addEventListener('change', (e) => {
                this.saveRating(e.target.value);
            });
        });
    }

    async saveRating(rating) {
        try {
            const response = await fetch('/save_rating', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_name: this.username,
                    rating: parseInt(rating)
                })
            });

            if (response.ok) {
                const result = await response.json();
                console.log('Rating saved successfully:', result);
                showComplete(); // Trigger feedback completion
            }
        } catch (error) {
            console.error('Error saving rating:', error);
        }
    }
}

// Initialize rating system
document.addEventListener('DOMContentLoaded', () => {
    new RatingSystem();
});