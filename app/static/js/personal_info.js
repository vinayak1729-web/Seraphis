// Chart configuration
const chartConfig = {
    meditation: {
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Seconds'
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    }
};

// Load meditation data
async function loadMeditationStats() {
    try {
        const response = await fetch('/get_meditation_stats');
        const data = await response.json();

        // Update stats
        document.getElementById('totalMinutes').textContent = data.total_minutes;
        document.getElementById('totalSessions').textContent = data.total_sessions;

        // Create chart
        const ctx = document.getElementById('meditationChart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.recent_sessions.map(session => 
                    new Date(session.timestamp).toLocaleDateString()
                ),
                datasets: [{
                    data: data.recent_sessions.map(session => session.duration),
                    borderColor: '#1565c0',
                    backgroundColor: 'rgba(21, 101, 192, 0.1)',
                    fill: true,
                    tension: 0.4
                }]
            },
            options: chartConfig.meditation.options
        });
    } catch (error) {
        console.error('Error loading meditation stats:', error);
    }
}

// Initialize dashboard
document.addEventListener('DOMContentLoaded', () => {
    loadMeditationStats();
});