document.getElementById('generateCode').addEventListener('click', async () => {
    const prompt = document.getElementById('prompt').value.trim();
    const alertBox = document.getElementById('alertBox');
    const chatHistory = document.getElementById('chatHistory');

    if (!prompt) {
        alertBox.innerText = 'Please enter a project description.';
        alertBox.classList.remove('hidden');
        return;
    }

    alertBox.classList.add('hidden');
    appendMessage(prompt, 'user-message');

    try {
        // Note that the endpoint should be updated to your actual server URL
        const response = await fetch('http://localhost:8000/generate-code', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ description: prompt })
        });

        if (!response.ok) {
            throw new Error('Failed to generate code.');
        }

        const data = await response.json();
        appendMessage(data.code, 'ai-message');
    } catch (error) {
        alertBox.innerText = error.message;
        alertBox.classList.remove('hidden');
    } finally {
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }
});

function appendMessage(text, className) {
    const message = document.createElement('div');
    message.classList.add('chat-message', className);
    if (className === 'ai-message') {
        const codeContainer = document.createElement('div');
        codeContainer.classList.add('code-container');
        const codeText = document.createElement('div');
        codeText.textContent = text.replace(/\\n/g, '\n').replace(/```/g, '');
        const copyBtn = document.createElement('button');
        copyBtn.textContent = 'Copy';
        copyBtn.classList.add('copy-button');
        copyBtn.onclick = function () {
            navigator.clipboard.writeText(codeText.textContent);
        };
        codeContainer.appendChild(codeText);
        codeContainer.appendChild(copyBtn);
        message.appendChild(codeContainer);
    } else {
        message.textContent = text;
    }
    chatHistory.appendChild(message);
}

document.getElementById('saveChat').addEventListener('click', function () {
    const chatHistory = document.getElementById('chatHistory').innerText;
    const blob = new Blob([chatHistory], { type: 'text/plain' });
    const anchor = document.createElement('a');
    anchor.href = URL.createObjectURL(blob);
    anchor.download = 'chat_history.txt';
    anchor.click();
    URL.revokeObjectURL(anchor.href);
});

document.getElementById('newChat').addEventListener('click', function () {
    document.getElementById('chatHistory').innerHTML = '';
    document.getElementById('prompt').value = '';
    document.getElementById('alertBox').classList.add('hidden');
});