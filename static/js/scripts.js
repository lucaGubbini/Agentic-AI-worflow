class ChatInterface {
    constructor() {
        this.initEventListeners();
        this.isGeneratingCode = false;
    }

    initEventListeners() {
        document.getElementById('generateCode').addEventListener('click', () => this.generateCode());
        document.getElementById('saveChat').addEventListener('click', () => this.saveChatHistory());
        document.getElementById('newChat').addEventListener('click', () => this.resetChat());
        window.addEventListener('load', () => this.adjustChatHeight());
        window.addEventListener('resize', () => this.adjustChatHeight());
    }

    adjustChatHeight() {
        const chatHistory = document.getElementById('chatHistory');
        chatHistory.style.maxHeight = `${window.innerHeight - chatHistory.offsetTop - 60}px`;
    }

    async generateCode() {
        let prompt = document.getElementById('userPrompt').value.trim();
        if (!prompt) {
            // Default prompt if the user input is empty
            prompt = "make a simple code for calculating the area of a rectangle in python";
            document.getElementById('userPrompt').value = prompt;
        }
        this.clearAlert();
        this.setGeneratingCodeStatus(true);

        const message = await this.postDescriptionAndGetCode(prompt);
        this.appendMessage(prompt, 'user-message');
        this.appendMessage(message, 'ai-message');

        this.setGeneratingCodeStatus(false);
    }

    setGeneratingCodeStatus(isGenerating) {
        this.isGeneratingCode = isGenerating;
        const statusIndicator = document.getElementById('statusIndicator');
        if (isGenerating) {
            statusIndicator.textContent = 'Generating code...';
        } else {
            statusIndicator.textContent = '';
        }
    }

    async postDescriptionAndGetCode(description) {
        try {
            const response = await fetch('/generate-code', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ description, sessionId: 'your-session-id' }) // Ensure sessionId is managed appropriately
            });

            if (!response.ok) {
                throw new Error('Failed to generate code. Please try again.');
            }

            const data = await response.json();
            if (data.influencedByDbData) {
                this.displayAlert('Model used data from the database.', 'success'); // Success message in green
                // Optionally display database data details
                console.log('Details:', data.dbDataDetails);
            }
            return data.code;
        } catch (error) {
            this.displayAlert(error.message, 'error'); // Error message in red
            return 'Error: Could not retrieve code.';
        }
    }


    appendMessage(text, className) {
        const chatHistory = document.getElementById('chatHistory');
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('chat-message', className);
        messageDiv.textContent = text;
        chatHistory.appendChild(messageDiv);

        chatHistory.scrollTop = chatHistory.scrollHeight - chatHistory.clientHeight;

        if (className === 'ai-message' && text.startsWith("``` python")) {
            messageDiv.innerHTML = '';
            const code = text.substring(10, text.length - 3); // Extract code
            const pre = document.createElement('pre');
            pre.textContent = code;
            messageDiv.appendChild(pre);
            messageDiv.appendChild(this.createCopyButton(code));
        }
    }

    createCopyButton(textToCopy) {
        const button = document.createElement('button');
        button.textContent = 'Copy';
        button.classList.add('copy-button');
        button.onclick = () => navigator.clipboard.writeText(textToCopy);
        return button;
    }

    displayAlert(message, className) {
        const alertBox = document.getElementById('alertBox');
        alertBox.textContent = message;
        // Remove all alert classes
        alertBox.classList.remove('alert-success', 'alert-danger', 'alert-warning', 'alert-info');
        // Add the specified class
        alertBox.classList.add(className);
    }



    clearAlert() {
        document.getElementById('alertBox').classList.add('hidden');
    }

    async saveChatHistory() {
        const chatHistory = document.getElementById('chatHistory').innerText;
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
            // Add 'alert-success' class instead of the previous class (assuming it was 'alert-danger')
            this.displayAlert(data.message, 'alert-success');
        } catch (error) {
            console.error('Save chat error:', error);
            // Use the 'alert-danger' class for errors
            this.displayAlert(error.message, 'alert-danger');
        }
    }


    resetChat() {
        document.getElementById('chatHistory').innerHTML = '';
        document.getElementById('userPrompt').value = '';
        this.clearAlert();
    }
}

new ChatInterface();
