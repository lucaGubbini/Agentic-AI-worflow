// Improved scripts.js with enhanced structure, error handling, and modularity
class ChatInterface {
    constructor() {
        this.initEventListeners();
    }

    initEventListeners() {
        document.getElementById('generateCode').addEventListener('click', () => this.generateCode());
        document.getElementById('saveChat').addEventListener('click', () => this.saveChatHistory());
        document.getElementById('newChat').addEventListener('click', () => this.resetChat());
    }

    async generateCode() {
        const prompt = document.getElementById('prompt').value.trim();
        if (!prompt) {
            this.displayAlert('Please enter a project description.');
            return;
        }
        this.clearAlert();

        const message = await this.postDescriptionAndGetCode(prompt);
        this.appendMessage(message, 'ai-message');
    }

    async postDescriptionAndGetCode(description) {
        try {
            const response = await fetch('http://localhost:8000/generate-code', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ description })
            });

            if (!response.ok) {
                throw new Error('Failed to generate code. Please try again.');
            }

            const { code } = await response.json();
            return code;
        } catch (error) {
            this.displayAlert(error.message);
            return 'Error: Could not retrieve code.';
        }
    }

    appendMessage(text, className) {
        const chatHistory = document.getElementById('chatHistory');
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('chat-message', className);
        messageDiv.textContent = text;
        chatHistory.appendChild(messageDiv);

        if (className === 'ai-message') {
            this.enhanceAIMessage(messageDiv, text);
        }

        chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    enhanceAIMessage(messageDiv, code) {
        const codeContainer = document.createElement('pre');
        codeContainer.textContent = code;
        const copyBtn = this.createCopyButton(code);
        messageDiv.innerHTML = '';
        messageDiv.appendChild(codeContainer);
        messageDiv.appendChild(copyBtn);
    }

    createCopyButton(textToCopy) {
        const button = document.createElement('button');
        button.textContent = 'Copy';
        button.classList.add('copy-button');
        button.onclick = () => navigator.clipboard.writeText(textToCopy);
        return button;
    }

    displayAlert(message) {
        const alertBox = document.getElementById('alertBox');
        alertBox.innerText = message;
        alertBox.classList.remove('hidden');
    }

    clearAlert() {
        document.getElementById('alertBox').classList.add('hidden');
    }

    saveChatHistory() {
        const chatHistory = document.getElementById('chatHistory').innerText;
        const blob = new Blob([chatHistory], { type: 'text/plain' });
        const anchor = document.createElement('a');
        anchor.href = URL.createObjectURL(blob);
        anchor.download = 'chat_history.txt';
        anchor.click();
        URL.revokeObjectURL(anchor.href);
    }

    resetChat() {
        document.getElementById('chatHistory').innerHTML = '';
        document.getElementById('prompt').value = '';
        this.clearAlert();
    }
}

new ChatInterface();
