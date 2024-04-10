document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('customAgentForm');

    form.addEventListener('submit', async (event) => {
        event.preventDefault(); // Prevent the form from submitting the traditional way

        // Collect form data into an object
        let formData = {
            agentName: document.getElementById('agentName').value,
            modelName: document.getElementById('modelName').value,
            maxTokens: document.getElementById('maxTokens').value,
            description: document.getElementById('description').value
        };

        // Logic to send a POST request to the server
        try {
            console.log('Submitting form data:', formData);

            const response = await fetch('http://localhost:8001/create-agent', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            });

            if (!response.ok) {
                // If the response is not ok, throw an error to jump to the catch block
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            console.log(result.message); // Log the success message from the server
            alert('Custom agent created successfully!');

            // Reset form after successful submission
            form.reset();
        } catch (error) {
            // Handle errors here
            console.error('An error occurred:', error);
            alert('Failed to create custom agent. Please try again.');
        }
    });
});
