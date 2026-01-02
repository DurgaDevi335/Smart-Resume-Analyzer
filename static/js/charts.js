// Function to initialize the ATS Score Gauge
function initScoreChart(scoreValue) {
    const ctx = document.getElementById('atsScoreChart').getContext('2d');
    
    // Determine color based on score
    let color = '#e74c3c'; // Red
    if (scoreValue >= 70) color = '#2ecc71'; // Green
    else if (scoreValue >= 40) color = '#f1c40f'; // Yellow

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            datasets: [{
                data: [scoreValue, 100 - scoreValue],
                backgroundColor: [color, '#e0e0e0'],
                borderWidth: 0,
                circumference: 180,
                rotation: 270
            }]
        },
        options: {
            cutout: '80%',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                tooltip: { enabled: false },
                legend: { display: false }
            }
        }
    });
}

// Function to handle the Resume Builder dynamic fields (if adding more)
function addExperienceField() {
    console.log("Adding new experience field...");
    // Logic for dynamic form fields can go here
}