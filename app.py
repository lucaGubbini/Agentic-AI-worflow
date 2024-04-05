from quart import Quart, request, jsonify, render_template
import logging
import openai  # Import the openai package

app = Quart(__name__)
logging.basicConfig(level=logging.INFO)

# Set the API key and base URL directly on the openai module
openai.api_key = "lm-studio"
openai.api_base = "http://localhost:1234/v1"  # Set the OpenAI API base URL to the local server

# CORS decorator to allow cross-origin access to your Quart app
@app.after_request
async def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    return response

@app.route('/')
async def home():
    return await render_template('index.html')

@app.route('/generate-code', methods=['POST'])
async def generate_code():
    data = await request.get_json()
    project_description = data.get('description', '')

    if not project_description:
        return jsonify({'error': 'Project description is required.'}), 400

    try:
        # Use the openai.Completion.create method to interact with the API
        response = openai.Completion.create(
            model="TheBloke/Mistral-7B-Instruct-v0.2-GGUF/mistral-7b-instruct-v0.2.Q8_0.gguf",
            prompt=project_description,
            temperature=0.7,
            max_tokens=5000 # You can adjust max_tokens as needed
        )
        # Extract the generated text from the response
        generated_text = response['choices'][0]['text'] if response['choices'] else 'No code was generated.'
        return jsonify({'code': generated_text}), 200
    except openai.error.OpenAIError as e:
        logging.error(f"LM Studio server error: {str(e)}")
        return jsonify({'error': 'Failed to generate code from LM Studio server.'}), 500

@app.errorhandler(404)
async def page_not_found(e):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
async def server_error(e):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8000)
