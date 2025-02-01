document.getElementById('reportForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const username = document.getElementById('username').value.trim();
    const issue = document.getElementById('issue').value.trim();
    const description = document.getElementById('description').value.trim();

    // Simple client-side validation
    if (!username || !issue || !description) {
        displayMessage('Please fill in all fields.', 'error');
        return;
    }

    // Prepare the report data
    const reportData = {
        username,
        issue,
        description
    };

    try {
        // Send the report to the server (replace with your server endpoint)
        const response = await fetch('https://your-api-endpoint.com/report', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(reportData)
        });

        if (response.ok) {
            const result = await response.json();
            displayMessage(`Report submitted successfully! Report ID: ${result.report_id}`, 'success');
            document.getElementById('reportForm').reset(); // Reset form after submission
        } else {
            throw new Error('Failed to submit report.');
        }
        
    } catch (error) {
        displayMessage(error.message, 'error');
    }
});

function displayMessage(message, type) {
    const responseMessage = document.getElementById('responseMessage');
    
    responseMessage.textContent = message;
    
    // Set class based on type
    responseMessage.className = `response-message ${type}`;
}
