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

        // Placeholder logic to simulate form submission
        try {
            console.log('Submitting form data:', formData);

            // Simulate a network request with a timeout
            await new Promise(resolve => setTimeout(resolve, 1000));

            // This is where you would typically make an API call
            // For example:
            // const response = await fetch('/api/create-agent', {
            //     method: 'POST',
            //     headers: {
            //         'Content-Type': 'application/json',
            //     },
            //     body: JSON.stringify(formData),
            // });

            // Let's assume everything went well
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
