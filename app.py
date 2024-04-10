from quart import Quart, request, jsonify, render_template
import logging
import os
import aiohttp  # For async HTTP requests
from dotenv import load_dotenv
import motor.motor_asyncio  # Asynchronous MongoDB driver

load_dotenv()  # Load environment variables from .env file

app = Quart(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# MongoDB setup
mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/chatApp')
mongo_client = motor.motor_asyncio.AsyncIOMotorClient(mongo_uri)
db = mongo_client.chatApp
agents_collection = db.agents

# Environment variables for LM Studio configuration
lm_studio_api_key = os.getenv('API_KEY', 'default_key_here')
lm_studio_api_base_url = os.getenv('BASE_URL', 'http://localhost:1234/v1')
default_model = os.getenv('DEFAULT_MODEL', 'TheBloke/Mistral-7B-Instruct-v0.2-GGUF/mistral-7b-instruct-v0.2.Q8_0.gguf')

# CORS configuration
@app.after_request
async def add_cors_headers(response):
    response.headers.update({
        'Access-Control-Allow-Origin': os.getenv('ALLOWED_ORIGIN', '*'),
        'Access-Control-Allow-Methods': 'GET, POST',
        'Access-Control-Allow-Headers': 'Content-Type,Authorization',
    })
    return response

@app.route('/')
async def home():
    """Serve the home page."""
    return await render_template('index.html')

@app.route('/generate-code', methods=['POST'])
async def generate_code():
    """Endpoint to generate code based on project description."""
    data = await request.get_json()
    project_description = data.get('description', '')

    if not project_description:
        logger.error("Project description is required.")
        return jsonify({'error': 'Project description is required.'}), 400

    try:
        code = await generate_code_from_lm_studio(project_description)
        return jsonify({'code': code}), 200
    except Exception as e:
        logger.error(f"LM Studio server error: {e}")
        return jsonify({'error': 'Failed to generate code from LM Studio server.'}), 500

@app.route('/create-agent', methods=['POST'])
async def create_agent():
    """Create a new agent with custom settings."""
    data = await request.get_json()

    try:
        # Insert new agent into MongoDB
        result = await agents_collection.insert_one(data)
        return jsonify({'message': 'Custom agent created successfully!', 'agentId': str(result.inserted_id)}), 201
    except Exception as e:
        logger.error(f"Error creating agent: {e}")
        return jsonify({'error': 'Failed to create custom agent.'}), 500

async def generate_code_from_lm_studio(description: str) -> str:
    """Generates code using LM Studio's local model."""
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{lm_studio_api_base_url}/completions",
            json={
                "model": default_model,
                "prompt": description,
                "temperature": 0.7,
                "max_tokens": 5000
            },
            headers={"Authorization": f"Bearer {lm_studio_api_key}"}
        ) as response:
            if response.status == 200:
                data = await response.json()
                return data['choices'][0]['text'] if data['choices'] else 'No code was generated.'
            else:
                raise Exception(f"Failed to fetch response from LM Studio, status: {response.status}")

@app.errorhandler(404)
async def page_not_found(e):
    """Handle 404 Not Found errors."""
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
async def server_error(e):
    """Handle 500 Internal Server errors."""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=int(os.getenv('PORT', 8000)))
