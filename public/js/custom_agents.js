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
                throw new Error(`Error: ${response.status}. Please try again.`);
            }

            const result = await response.json();
            console.log(result.message);
            displaySuccessMessage('Custom agent created successfully!');
            form.reset();
        } catch (error) {
            console.error('An error occurred:', error);
            displayErrorMessage(error.message);
        }
    });

    function displayErrorMessage(message) {
        const toastContainer = getToastContainer();
        const toastMessage = createToastMessage(message, 'error');
        toastContainer.appendChild(toastMessage);
        setTimeout(() => toastMessage.remove(), 5000);
    }

    function displaySuccessMessage(message) {
        const toastContainer = getToastContainer();
        const toastMessage = createToastMessage(message, 'success');
        toastContainer.appendChild(toastMessage);
        setTimeout(() => toastMessage.remove(), 5000);
    }

    function getToastContainer() {
        let toastContainer = document.getElementById('toastContainer');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.id = 'toastContainer';
            toastContainer.style.position = 'fixed';
            toastContainer.style.bottom = '20px';
            toastContainer.style.right = '20px';
            toastContainer.style.zIndex = '1000';
            document.body.appendChild(toastContainer);
        }
        return toastContainer;
    }

    function createToastMessage(message, type) {
        const toast = document.createElement('div');
        toast.textContent = message;
        toast.style.background = type === 'error' ? '#f44336' : '#4CAF50';
        toast.style.color = 'white';
        toast.style.padding = '10px';
        toast.style.marginTop = '10px';
        toast.style.borderRadius = '5px';
        toast.style.opacity = '0';
        toast.style.transition = 'opacity 0.5s';

        // Trigger the opacity transition after adding the element to the DOM
        setTimeout(() => toast.style.opacity = '1', 0);

        return toast;
    }
});
