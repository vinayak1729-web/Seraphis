let isBreathing = false;
let timer;
let startTime;
let meditationChart;

function startMeditation() {
    if (isBreathing) return;
    isBreathing = true;
    startTime = new Date();
    
    document.getElementById('startBtn').style.display = 'none';
    document.getElementById('stopBtn').style.display = 'inline-block';
    
    const instruction = document.getElementById('instruction');
    instruction.style.opacity = 1;
    
    let timeLeft = 300;
    const timerDisplay = document.getElementById('timer');
    
    function updateTimer() {
        const minutes = Math.floor(timeLeft / 60);
        const seconds = timeLeft % 60;
        timerDisplay.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
    }
    
    timer = setInterval(() => {
        if (timeLeft <= 0) {
            completeMeditation();
            return;
        }
        
        timeLeft--;
        updateTimer();
        instruction.textContent = Math.floor(timeLeft) % 8 < 4 ? "Breathe In" : "Breathe Out";
    }, 1000);
}

function stopMeditation() {
    completeMeditation(false);
}

function completeMeditation(completed = true) {
    clearInterval(timer);
    const duration = Math.floor((new Date() - startTime) / 1000);
    
    fetch('/log_meditation', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            duration: duration,
            completed: completed
        })
    })
    .then(response => response.json())
    .then(() => {
        updateMeditationStats();
        resetUI();
    });
}

function resetUI() {
    isBreathing = false;
    document.getElementById('instruction').style.opacity = 0;
    document.getElementById('timer').textContent = '5:00';
    document.getElementById('startBtn').style.display = 'inline-block';
    document.getElementById('stopBtn').style.display = 'none';
}

function updateMeditationStats() {
    fetch('/get_meditation_stats')
    .then(response => response.json())
    .then(data => {
        const statsDiv = document.getElementById('meditationStats');
        statsDiv.innerHTML = `
            <p>Total Sessions: ${data.total_sessions}</p>
            <p>Total Minutes: ${Math.floor(data.total_minutes / 60)}</p>
        `;
        
        updateChart(data.recent_sessions);
    });
}

function updateChart(sessions) {
    const ctx = document.getElementById('meditationChart').getContext('2d');
    
    if (meditationChart) {
        meditationChart.destroy();
    }

    meditationChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: sessions.map(s => new Date(s.timestamp).toLocaleDateString()),
            datasets: [{
                label: 'Meditation Duration (minutes)',
                data: sessions.map(s => s.duration / 60),
                borderColor: '#3498db',
                backgroundColor: 'rgba(52, 152, 219, 0.1)',
                fill: true
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Minutes'
                    }
                }
            }
        }
    });
}

// Load initial stats
updateMeditationStats();