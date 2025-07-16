document.addEventListener('DOMContentLoaded', () => {
    const micButton = document.getElementById('mic-btn');
    const voiceAnimation = document.getElementById('voiceAnimation');
    const video = document.getElementById('video');

    video.src = "/video_feed";

    micButton.addEventListener('click', function () {
        startListening();
        this.classList.add('listening');
    });

    function sendMessage(userInput) {
        if (userInput.trim() === "") return;

        const chatbox = document.getElementById('chatbox');
        chatbox.innerHTML += `<div class="message user-msg"><div class="message-content">${userInput}</div></div>`;
        chatbox.scrollTop = chatbox.scrollHeight;

        fetch('/talk_to_me', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `user_input=${encodeURIComponent(userInput)}`
        })
            .then(response => response.json())
            .then(data => {
                chatbox.innerHTML += `<div class="message bot-msg"><div class="message-content">${data.response}</div></div>`;
                chatbox.scrollTop = chatbox.scrollHeight;
                speak(data.response);
            })
            .catch(error => console.error('Error:', error));
    }

    function startListening() {
        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = 'en-US';
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;

        recognition.start();
        voiceAnimation.classList.add('listening');

        recognition.onresult = function (event) {
            const userInput = event.results[0][0].transcript;
            micButton.classList.remove('listening');
            voiceAnimation.classList.remove('listening');
            sendMessage(userInput);
        };

        recognition.onerror = function (event) {
            console.error('Speech recognition error:', event.error);
            micButton.classList.remove('listening');
            voiceAnimation.classList.remove('listening');
        };

        recognition.onend = function () {
            micButton.classList.remove('listening');
            voiceAnimation.classList.remove('listening');
        };
    }

    function speak(text) {
        const utterance = new SpeechSynthesisUtterance(text);
        speechSynthesis.speak(utterance);
    }

    // Add subtle animation to orb on mousemove
    document.addEventListener('mousemove', (e) => {
        const orb = document.querySelector('.orb');
        const rect = orb.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;

        const deltaX = (e.clientX - centerX) * 0.01;
        const deltaY = (e.clientY - centerY) * 0.01;

        orb.style.transform = `translate(calc(-50% + ${deltaX}px), calc(-50% + ${deltaY}px))`;
    });
});