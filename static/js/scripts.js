class ChatInterface {
    constructor() {
        this.apiEndpoint = '/generate-code'; // Centralize API endpoint
        this.bindEventListeners();
        this.isGeneratingCode = false;
    }

    bindEventListeners() {
        document.getElementById('generateCode').addEventListener('click', () => this.handleGenerateCode());
        document.getElementById('saveChat').addEventListener('click', () => this.handleSaveChat());
        document.getElementById('newChat').addEventListener('click', () => this.handleNewChat());
        window.addEventListener('load', () => this.adjustChatHeight());
        window.addEventListener('resize', () => this.adjustChatHeight());
    }

    adjustChatHeight() {
        const chatHistory = document.getElementById('chatHistory');
        chatHistory.style.maxHeight = `${window.innerHeight - chatHistory.offsetTop - 60}px`;
    }

    displayAlert(message, type) {
        const alertBox = document.getElementById('alertBox');
        alertBox.textContent = message;
        alertBox.className = `alertBox ${type}`;
        alertBox.classList.remove('hidden');

        clearTimeout(this.alertTimeout);
        this.alertTimeout = setTimeout(() => this.clearAlert(), 5000);
    }

    clearAlert() {
        const alertBox = document.getElementById('alertBox');
        alertBox.classList.add('hidden');
    }

    async postRequest(url, data) {
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                throw new Error(`Failed to fetch: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            this.displayAlert(error.message, 'error');
            throw error; // Re-throw to allow caller to handle as well
        }
    }

    appendMessage(text, className) {
        const chatHistory = document.getElementById('chatHistory');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${className}`;
        messageDiv.textContent = text;

        chatHistory.appendChild(messageDiv);
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    async handleGenerateCode() {
        const userPrompt = document.getElementById('userPrompt').value.trim();
        const prompt = userPrompt || "make a simple code for calculating the area of a rectangle in python";
        if (!userPrompt) document.getElementById('userPrompt').value = prompt;

        this.clearAlert();
        this.updateGeneratingCodeStatus(true);

        try {
            const data = await this.postRequest(this.apiEndpoint, { description: prompt });
            this.appendMessage(prompt, 'user-message');
            this.appendMessage(data.generatedCode, 'ai-message');
        } catch (error) {
            // Error handling is managed within postRequest
        } finally {
            this.updateGeneratingCodeStatus(false);
        }
    }

    updateGeneratingCodeStatus(isGenerating) {
        this.isGeneratingCode = isGenerating;
        const generateButton = document.getElementById('generateCode');
        generateButton.textContent = isGenerating ? 'Generating...' : 'Generate Code';
        generateButton.disabled = isGenerating;
    }

    async handleSaveChat() {
        const chatHistory = Array.from(document.querySelectorAll('.message'))
            .map(msgDiv => msgDiv.textContent)
            .join('\n');
        try {
            const data = await this.postRequest('http://localhost:8001/save-chat', { chatHistory });
            this.displayAlert(data.message, 'success');
        } catch (error) {
            // Error handling is managed within postRequest
        }
    }

    handleNewChat() {
        document.getElementById('chatHistory').innerHTML = '';
        document.getElementById('userPrompt').value = '';
        this.clearAlert();
    }
}

document.addEventListener('DOMContentLoaded', () => new ChatInterface());
