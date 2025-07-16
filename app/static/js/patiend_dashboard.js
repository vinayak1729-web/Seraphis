// Set min date to today
const today = new Date().toISOString().split('T')[0];
document.getElementById('dateSelect').min = today;

function generateTimeSlots() {
    fetch('/api/available-slots')
        .then(response => response.json())
        .then(slots => {
            const slotGrid = document.getElementById('slotGrid');
            slotGrid.innerHTML = slots.map(time => `
                <div class="slot" data-time="${time}">${time}</div>
            `).join('');
            updateSlots();
        });
}

function updateSlots() {
    const date = document.getElementById('dateSelect').value;
    fetch('/api/appointments')
        .then(response => response.json())
        .then(appointments => {
            const slots = document.querySelectorAll('.slot');
            slots.forEach(slot => {
                slot.className = 'slot';
                const isBooked = appointments.some(a =>
                    a.date === date &&
                    a.slot === slot.dataset.time
                );
                if (isBooked) {
                    slot.classList.add('booked');
                }
            });
        });
}

function loadUserStats() {
    fetch('/api/user/stats')
        .then(response => response.json())
        .then(stats => {
            const statsDiv = document.getElementById('userStats');
            statsDiv.innerHTML = `
                <div class="rating-${stats.rating}">
                    Patient Rating: ${stats.rating.toUpperCase()}
                    (Total Appointments: ${stats.total_appointments}, 
                    Cancellations: ${stats.total_cancellations})
                </div>
            `;
        });
}

function bookAppointment(date, slot) {
    if (!date) {
        showError('Please select a date');
        return;
    }

    const selectedDate = new Date(date);
    const selectedTime = slot.split('-')[0];
    const [hours, minutes] = selectedTime.split(':');
    selectedDate.setHours(parseInt(hours), parseInt(minutes));
    const now = new Date();

    if (selectedDate < today) {
        showError('Cannot book appointments in the past');
        return;
    }

    if (selectedDate.getDay() === 0 || selectedDate.getDay() === 6) {
        showError('Appointments not available on weekends');
        return;
    }

    fetch('/api/appointments', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ date, slot })
    })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => {
                    throw new Error(err.error || 'Booking failed');
                });
            }
            return response.json();
        })
        .then(data => {
            showSuccess('Appointment booked successfully');
            loadAppointments();
            updateSlots();
        })
        .catch(error => {
            showError(error.message);
        });
}

function showError(message) {
    const alert = document.createElement('div');
    alert.className = 'alert alert-error';
    alert.textContent = message;
    document.querySelector('.container').prepend(alert);
    setTimeout(() => alert.remove(), 5000);
}

function showSuccess(message) {
    const alert = document.createElement('div');
    alert.className = 'alert alert-success';
    alert.textContent = message;
    document.querySelector('.container').prepend(alert);
    setTimeout(() => alert.remove(), 5000);
}

function cancelAppointment(appointmentId) {
    const form = document.getElementById(`cancelForm-${appointmentId}`);
    form.style.display = 'block';
}

function submitCancellation(appointmentId) {
    const reason = document.getElementById(`cancelReason-${appointmentId}`).value;
    if (!reason) {
        alert('Please provide a reason for cancellation');
        return;
    }

    fetch(`/api/appointments/cancel/${appointmentId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ reason })
    })
        .then(response => {
            if (response.ok) {
                loadAppointments();
                loadUserStats();
            }
        });
}

function loadAppointments() {
    fetch('/api/appointments')
        .then(response => response.json())
        .then(appointments => {
            const list = document.getElementById('appointmentsList');
            list.innerHTML = appointments.map(appointment => {
                const appointmentDate = new Date(appointment.date);
                const [startTime] = appointment.slot.split('-');
                const [hours, minutes] = startTime.split(':');
                appointmentDate.setHours(parseInt(hours), parseInt(minutes));

                const now = new Date();
                const endTime = new Date(appointmentDate);
                endTime.setHours(endTime.getHours() + 1);

                const showMeetLink = appointment.status === 'accepted' &&
                    now >= appointmentDate &&
                    now <= endTime;

                return `
                    <div class="appointment-card status-${appointment.status}">
                        <div>Date: ${appointment.date}</div>
                        <div>Time: ${appointment.slot}</div>
                        <div>Status: ${appointment.status}</div>
                        ${appointment.cancellation_reason ?
                            `<div>Cancellation Reason: ${appointment.cancellation_reason}</div>` : ''}
                        ${showMeetLink && appointment.meet_link ?
                            `<a href="${appointment.meet_link}" target="_blank" class="btn btn-primary">
                                Enter Room
                             </a>` : ''}
                        ${appointment.status === 'pending' ? `
                            <button onclick="cancelAppointment(${appointment.id})">Cancel</button>
                            <div id="cancelForm-${appointment.id}" class="cancel-form" style="display: none;">
                                <textarea id="cancelReason-${appointment.id}" 
                                    placeholder="Please provide reason for cancellation"></textarea>
                                <button onclick="submitCancellation(${appointment.id})">Submit</button>
                            </div>
                        ` : ''}
                    </div>
                `;
            }).join('');
        });
}

document.getElementById('slotGrid').addEventListener('click', (e) => {
    if (e.target.classList.contains('slot') && !e.target.classList.contains('booked')) {
        const date = document.getElementById('dateSelect').value;
        if (!date) {
            alert('Please select a date first');
            return;
        }
        bookAppointment(date, e.target.dataset.time);
    }
});

// Initial load
generateTimeSlots();
loadUserStats();
loadAppointments();