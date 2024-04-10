from quart import Quart, request, jsonify, render_template
import os
from dotenv import load_dotenv
import motor.motor_asyncio
from quart_cors import cors
from aiohttp import ClientSession
from bson.objectid import ObjectId

load_dotenv()

app = Quart(__name__, template_folder='public', static_folder='public')
app = cors(app, allow_origin=os.getenv('ALLOWED_ORIGIN', '*'))

mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/chatApp')
mongo_client = motor.motor_asyncio.AsyncIOMotorClient(mongo_uri)
db = mongo_client.get_default_database()
agents_collection = db.agents

api_key = os.getenv('API_KEY')
api_base_url = os.getenv('BASE_URL')
default_model = os.getenv('DEFAULT_MODEL')

@app.route('/')
async def home():
    return await render_template('index.html')

@app.route('/generate-code', methods=['POST'])
async def generate_code():
    data = await request.get_json()
    project_description = data.get('description', '')
    if not project_description:
        return jsonify({'error': 'Project description is required.'}), 400

    async with ClientSession() as session:
        try:
            code = await generate_code_from_api(session, project_description)
            return jsonify({'code': code}), 200
        except Exception as e:
            return jsonify({'error': 'Failed to generate code from API server.'}), 500

@app.route('/create-agent', methods=['POST'])
async def create_agent():
    data = await request.get_json()
    required_fields = ['agentName', 'modelName', 'maxTokens', 'description']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing fields for creating an agent.'}), 400

    try:
        result = await agents_collection.insert_one(data)
        return jsonify({'message': 'Custom agent created successfully!', 'agentId': str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({'error': 'Failed to create custom agent.'}), 500

async def generate_code_from_api(session: ClientSession, description: str) -> str:
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
    async with session.post(
        f"{api_base_url}/completions",
        json={"model": default_model, "prompt": description, "temperature": 0.7, "max_tokens": 5000},
        headers=headers
    ) as response:
        if response.status == 200:
            data = await response.json()
            return data['choices'][0]['text'] if data['choices'] else 'No code was generated.'
        else:
            raise Exception(f"Failed to fetch response from API, status: {response.status}")

@app.errorhandler(404)
async def page_not_found(e):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
async def server_error(e):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    debug_mode = os.getenv('DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8000)), debug=debug_mode)
