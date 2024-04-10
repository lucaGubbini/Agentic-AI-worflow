// controllers/chatController.js
const db = require('../public/db').getDb; // Assuming you have a db module that exports a getDb function

// Save chat history to the database
async function saveChatHistory(chatHistory) {
    try {
        const database = db();
        const result = await database.collection('chats').insertOne({ chatHistory, createdAt: new Date() });
        return { message: 'Chat history saved successfully', _id: result.insertedId };
    } catch (error) {
        console.error('Error saving chat history:', error);
        throw new Error('Database operation failed');
    }
}

// Simulate generating code from an external service
async function generateCode(description) {
    try {
        // Here you would typically make an API call to generate the code
        // For the purposes of this example, we'll simulate a response
        const generatedCode = `Code for ${description}`; // Placeholder for actual code generation logic
        return generatedCode;
    } catch (error) {
        console.error('Error generating code:', error);
        throw new Error('Code generation failed');
    }
}

module.exports = { saveChatHistory, generateCode };
