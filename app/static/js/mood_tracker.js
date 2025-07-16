let moodChart;
const moodScores = {
    'happy': 2,
    'excited': 1.5,
    'neutral': 1,
    'sad': 0.5,
    'angry': -1
};

const moodEmojis = {
    'happy': '😊',
    'excited': '🤗',
    'neutral': '😐',
    'sad': '😔',
    'angry': '😠'
};

function createMoodChart(moodData) {
    const ctx = document.getElementById('moodChart').getContext('2d');

    const chartData = moodData.map(entry => ({
        x: new Date(entry.timestamp),
        y: moodScores[entry.mood],
        mood: entry.mood
    }));

    return new Chart(ctx, {
        type: 'line',
        data: {
            datasets: [{
                label: 'Mood Level',
                data: chartData,
                borderColor: '#7e57c2',
                backgroundColor: 'rgba(126, 87, 194, 0.1)',
                tension: 0.4,
                fill: true,
                pointBackgroundColor: '#7e57c2'
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    min: -2.5,
                    max: 2.5,
                    ticks: {
                        callback: function (value) {
                            const mood = Object.entries(moodScores).find(([k, v]) => v === value);
                            if (mood) {
                                return `${mood[0]} ${moodEmojis[mood[0]]}`;
                            }
                            return '';
                        },
                        font: {
                            family: 'Lora',
                            size: 14
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)'
                    }
                },
                x: {
                    type: 'time',
                    time: {
                        unit: 'day',
                        displayFormats: {
                            day: 'MMM d'
                        }
                    }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            const mood = context.raw.mood;
                            return `Mood: ${moodEmojis[mood]} (${mood})`;
                        }
                    }
                }
            }
        }
    });
}

function updateMoodHistory() {
    fetch('/get_moods')
        .then(response => response.json())
        .then(data => {
            // Update text history
            const historyDiv = document.getElementById('moodHistory');
            historyDiv.innerHTML = data.moods.map(mood => `
                <div class="d-flex align-items-center justify-content-between p-2 border-bottom">
                    <span>${moodEmojis[mood.mood]}</span>
                    <span>${new Date(mood.timestamp).toLocaleString()}</span>
                </div>
            `).join('');

            // Update chart
            if (moodChart) {
                moodChart.destroy();
            }
            moodChart = createMoodChart(data.moods);
        });
}

function logMood(mood) {
    const timestamp = new Date().toISOString();
    fetch('/log_mood', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            mood: mood,
            timestamp: timestamp
        })
    })
        .then(response => response.json())
        .then(() => updateMoodHistory());
}

// Initial load
document.addEventListener('DOMContentLoaded', updateMoodHistory);