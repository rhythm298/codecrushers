document.getElementById('reportForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const username = document.getElementById('username').value;
    const issue = document.getElementById('issue').value;
    const description = document.getElementById('description').value;

    // Simulate sending the report to the server
    console.log('Report submitted:', { username, issue, description });
    
    document.getElementById('responseMessage').innerText = 'Thank you for your report. We will review it shortly.';
    
    // Reset the form
    this.reset();
});
