const express = require('express');
const { saveChatHistory, generateCode } = require('../controllers/chatController');

const router = express.Router();

// Middleware to validate chat history
const validateChatHistory = (req, res, next) => {
    const { chatHistory } = req.body;
    if (!chatHistory || typeof chatHistory !== 'string') {
        return res.status(400).json({ error: 'Valid chat history is required.' });
    }
    next();
};

// Middleware to validate code generation input
const validateCodeGeneration = (req, res, next) => {
    const { description } = req.body;
    if (!description || typeof description !== 'string') {
        return res.status(400).json({ error: 'Valid description is required.' });
    }
    // Add more validation as needed
    next();
};

// Route to save chat history
router.post('/save-history', validateChatHistory, async (req, res) => {
    try {
        const { chatHistory } = req.body;
        const result = await saveChatHistory(chatHistory);
        res.json(result);
    } catch (error) {
        console.error('Error saving chat history:', error);
        res.status(500).json({ error: 'Failed to save chat history.' });
    }
});

// Route to generate code based on user prompt
router.post('/generate-code', validateCodeGeneration, async (req, res) => {
    try {
        const { description } = req.body;
        const generatedCode = await generateCode(description);
        res.json({ generatedCode });
    } catch (error) {
        console.error('Error generating code:', error);
        res.status(500).json({ error: 'Failed to generate code.' });
    }
});

module.exports = router;
