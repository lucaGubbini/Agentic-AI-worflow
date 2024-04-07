class ChatInterface {
    constructor() {
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

    async handleGenerateCode() {
        const userPrompt = document.getElementById('userPrompt').value.trim();
        const prompt = userPrompt || "make a simple code for calculating the area of a rectangle in python";
        if (!userPrompt) document.getElementById('userPrompt').value = prompt;

        this.clearAlert();
        this.updateGeneratingCodeStatus(true);

        try {
            const code = await this.fetchGeneratedCode(prompt);
            this.appendMessage(prompt, 'user-message');
            this.appendMessage(code, 'ai-message');
        } catch (error) {
            this.displayAlert(error, 'error');
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

    async fetchGeneratedCode(description) {
        try {
            const response = await fetch('/generate-code', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ description })
            });

            if (!response.ok) {
                throw new Error('Failed to generate code. Please try again.');
            }

            const data = await response.json();
            return data.code;
        } catch (error) {
            this.displayAlert(error.message, 'error');
            throw error;
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

    async handleSaveChat() {
        const chatHistory = Array.from(document.querySelectorAll('.message'))
            .map(msgDiv => msgDiv.textContent)
            .join('\n');
        try {
            const response = await fetch('http://localhost:8001/save-chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ chatHistory })
            });

            if (!response.ok) {
                throw new Error('Failed to save chat history. Please try again.');
            }

            const data = await response.json();
            this.displayAlert(data.message, 'success');
            // set allert opacity to 1
            document.getElementById('alertBox').style.opacity = 1;
        } catch (error) {
            this.displayAlert(error.message, 'error');
            document.getElementById('alertBox').style.opacity = 1;
        }
    }


    handleNewChat() {
        document.getElementById('chatHistory').innerHTML = '';
        document.getElementById('userPrompt').value = '';
        this.clearAlert();
    }
}

document.addEventListener('DOMContentLoaded', () => new ChatInterface());
