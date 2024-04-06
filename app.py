from quart import Quart, request, jsonify, render_template
import logging
import openai  # Import the OpenAI package

app = Quart(__name__)

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Set OpenAI API key and base URL
openai.api_key = "lm-studio"
openai.api_base = "http://localhost:1234/v1"  # Local server base URL

# Add CORS headers to allow cross-origin access
@app.after_request
async def add_cors_headers(response):
    response.headers.update({
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST',
        'Access-Control-Allow-Headers': 'Content-Type,Authorization'
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
        response = await generate_code_from_openai(project_description)
        return jsonify({'code': response}), 200
    except openai.error.OpenAIError as e:
        logger.error(f"LM Studio server error: {str(e)}")
        return jsonify({'error': 'Failed to generate code from LM Studio server.'}), 500

async def generate_code_from_openai(description: str) -> str:
    """Generates code using OpenAI's API."""
    response = openai.Completion.create(
        model="TheBloke/Mistral-7B-Instruct-v0.2-GGUF/mistral-7b-instruct-v0.2.Q8_0.gguf",
        prompt=description,
        temperature=0.7,
        max_tokens=5000
    )
    return response['choices'][0]['text'] if response['choices'] else 'No code was generated.'

@app.errorhandler(404)
async def page_not_found(e):
    """Handle 404 Not Found errors."""
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
async def server_error(e):
    """Handle 500 Internal Server errors."""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8000)
