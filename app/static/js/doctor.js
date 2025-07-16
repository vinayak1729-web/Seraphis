function updateAppointmentStatus(appointmentId, status) {
    fetch(`/api/appointments/${appointmentId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ status: status })
    })
        .then(response => {
            if (response.ok) {
                loadAppointments();
            } else {
                throw new Error('Failed to update appointment');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to update appointment status');
        });
}

function loadAppointments() {
    fetch('/api/doctor/appointments')
        .then(response => response.json())
        .then(appointments => {
            const list = document.getElementById('appointmentsList');
            list.innerHTML = appointments.map(appointment => `
                <div class="appointment-card status-${appointment.status.toLowerCase()}" data-patient="${appointment.patient}">
                    <div class="patient-info">
                        <div class="rating-indicator rating-${appointment.patient_rating}"></div>
                        <strong>Patient:</strong> ${appointment.patient}
                    </div>
                    <div class="appointment-details">
                        <p><strong>Date:</strong> ${appointment.date}</p>
                        <p><strong>Time:</strong> ${appointment.slot}</p>
                        <p><strong>Status:</strong> ${appointment.status}</p>
                        ${appointment.cancellation_reason ?
                            `<div class="cancellation-reason">
                                <strong>Cancellation Reason:</strong> ${appointment.cancellation_reason}
                            </div>` : ''
                        }
                    </div>
                    ${appointment.status === 'pending' ? `
                        <div class="actions">
                            <button class="accept-btn" onclick="updateAppointmentStatus(${appointment.id}, 'accepted')">
                                Accept
                            </button>
                            <button class="reject-btn" onclick="updateAppointmentStatus(${appointment.id}, 'rejected')">
                                Reject
                            </button>
                        </div>
                    ` : ''}
                    <button onclick="viewPatientInfo('${appointment.patient}')" class="info-btn">
                        View Patient Info
                    </button>
                </div>
            `).join('');
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to load appointments');
        });
}

function viewPatientInfo(username) {
    fetch(`/api/doctor/patient-info/${username}`)
        .then(res => res.json())
        .then(data => {
            // Clear previous content first
            document.getElementById('basicInfoContent').innerHTML = '';
            document.getElementById('wellnessReport').innerHTML = '';
            document.getElementById('closeEndedResponses').innerHTML = '';
            document.getElementById('openEndedResponses').innerHTML = '';

            // Display basic info
            const basicInfo = `
                <h4>Personal Details</h4>
                <p><strong>Name:</strong> ${username}</p>
                <p><strong>Age:</strong> ${data.basic_info.age || 'Not provided'}</p>
                <p><strong>Gender:</strong> ${data.basic_info.gender || 'Not provided'}</p>
                <p><strong>Occupation:</strong> ${data.basic_info.occupation || 'Not provided'}</p>
            `;
            document.getElementById('basicInfoContent').innerHTML = basicInfo;

            // Display wellness report only if it exists
            if (data.basic_info.wellness_report) {
                document.getElementById('wellnessReport').innerHTML = `
                    <h4>Wellness Report</h4>
                    <div style="max-height: 200px; overflow-y: auto; padding: 10px; background: #f8f9fa; border-radius: 4px;">
                        <p>${data.basic_info.wellness_report}</p>
                    </div>`;
            }

            // Display questionnaire responses if they exist
            if (data.questionnaire_responses) {
                const closeEnded = data.questionnaire_responses.close_ended;
                const openEnded = data.questionnaire_responses.open_ended;

                if (closeEnded.length > 0) {
                    document.getElementById('closeEndedResponses').innerHTML = formatResponses(closeEnded);
                }
                if (openEnded.length > 0) {
                    document.getElementById('openEndedResponses').innerHTML = formatResponses(openEnded);
                }
            }

            // Show the container
            document.querySelector('.patient-info-container').style.display = 'block';
        })
        .catch(error => {
            console.error('Error fetching patient info:', error);
            alert('Failed to load patient information');
        });
}

function formatResponses(responses) {
    return responses.map(r =>
        `<div class="response">
            <p><strong>Q:</strong> ${r.Question}</p>
            <p><strong>A:</strong> ${r.Answer || r.Response}</p>
        </div>`
    ).join('');
}

function showTab(tabId) {
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.getElementById(tabId).classList.add('active');
    event.target.classList.add('active');
}

function closePatientInfo() {
    document.querySelector('.patient-info-container').style.display = 'none';
}

// Initial load
loadAppointments();

// Refresh every 30 seconds
setInterval(loadAppointments, 30000);