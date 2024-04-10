// controllers/agentController.js
const db = require('../db').getDb; // Ensure this points to your db module with getDb function

// Create a new agent in the database
async function createAgent(agentData) {
    try {
        const database = db();
        const collection = database.collection('agents');

        // Perform data validation or transformation as needed
        validateAgentData(agentData);

        // Insert the new agent
        const result = await collection.insertOne(agentData);
        return { message: 'Agent created successfully', _id: result.insertedId };
    } catch (error) {
        console.error('Error creating agent:', error);
        throw new Error('Database operation failed');
    }
}

// List all agents from the database
async function listAgents() {
    try {
        const database = db();
        const collection = database.collection('agents');

        const agents = await collection.find({}).toArray();
        return agents;
    } catch (error) {
        console.error('Error listing agents:', error);
        throw new Error('Database operation failed');
    }
}

// Example validation function, extend this as necessary
function validateAgentData(agentData) {
    if (!agentData.agentName || !agentData.modelName || !agentData.maxTokens) {
        throw new Error('Validation failed: all fields are required.');
    }
    // Add additional validation as needed
}

module.exports = { createAgent, listAgents };
