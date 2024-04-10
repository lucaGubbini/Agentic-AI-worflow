class ChatInterface {
    constructor() {
        this.apiEndpoint = '/generate-code'; // API endpoint to generate code
        this.saveChatEndpoint = '/chat/save-history'; // Endpoint for saving chat history
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
                throw new Error(`HTTP Error: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            this.displayAlert(`Error: ${error.message}`, 'error');
            console.error('Request Error:', error);
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
        const prompt = userPrompt || "Enter your code generation prompt here...";

        this.clearAlert();
        this.updateGeneratingCodeStatus(true);

        try {
            const data = await this.postRequest(this.apiEndpoint, { description: prompt });
            this.appendMessage(prompt, 'user-message');
            if (data && data.code) {
                this.appendMessage(data.code, 'ai-message');
            } else {
                this.appendMessage("Error: No code generated.", 'ai-message');
            }
        } catch (error) {
            // Error handling is already managed within postRequest
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
        const chatHistoryElements = document.querySelectorAll('.message');
        const chatHistory = Array.from(chatHistoryElements).map(msgDiv => msgDiv.textContent).join('\n');

        this.clearAlert();

        try {
            const data = await this.postRequest(this.saveChatEndpoint, { chatHistory });
            if (data && data.message) {
                this.displayAlert(data.message, 'success');
            } else {
                this.displayAlert("Error: Chat not saved.", 'error');
            }
        } catch (error) {
            // Error handling is already managed within postRequest
        }
    }

    handleNewChat() {
        document.getElementById('chatHistory').innerHTML = '';
        document.getElementById('userPrompt').value = '';
        this.clearAlert();
    }
}

document.addEventListener('DOMContentLoaded', () => new ChatInterface());
