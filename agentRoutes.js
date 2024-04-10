const express = require('express');
const { createAgent, listAgents } = require('../controllers/agentController');
const router = express.Router();

// Middleware to validate agent data
const validateAgentData = (req, res, next) => {
    const { agentName, modelName, maxTokens, description } = req.body;
    if (!agentName || !modelName || !maxTokens || !description) {
        return res.status(400).json({ error: 'All fields are required.' });
    }
    // Add more validation as needed
    next();
};

// Route to create a new agent
router.post('/create', validateAgentData, async (req, res) => {
    try {
        const agentData = req.body;
        const result = await createAgent(agentData);
        res.status(201).json(result);
    } catch (error) {
        console.error('Error creating agent:', error);
        res.status(500).json({ error: 'Failed to create agent.' });
    }
});

// Route to list all agents
router.get('/list', async (req, res) => {
    try {
        const agents = await listAgents();
        if (agents.length === 0) {
            return res.status(404).json({ message: 'No agents found.' });
        }
        res.json(agents);
    } catch (error) {
        console.error('Error listing agents:', error);
        res.status(500).json({ error: 'Failed to list agents.' });
    }
});

module.exports = router;
