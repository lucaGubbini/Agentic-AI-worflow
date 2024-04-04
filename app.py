from quart import Quart, request, jsonify, render_template
import logging
from openai import OpenAI
import asyncio

app = Quart(__name__)
logging.basicConfig(level=logging.INFO)

# Configuration for the LM-Studio server
LM_STUDIO_BASE_URL = "http://localhost:1234/v1"
LM_STUDIO_API_KEY = "lm-studio"
MODEL = "TheBloke/Mistral-7B-Instruct-v0.2-GGUF/mistral-7b-instruct-v0.2.Q8_0.gguf"

# Initialize OpenAI client for LM-Studio
client = OpenAI(base_url=LM_STUDIO_BASE_URL, api_key=LM_STUDIO_API_KEY)

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
        completion = await asyncio.to_thread(
            client.chat.completions.create,
            model=MODEL,
            messages=[
                {"role": "system", "content": "Generate a code based on the following project description."},
                {"role": "user", "content": project_description}
            ],
            temperature=0.7
        )

        # Extract the assistant's response from the completion object
        if completion.choices and completion.choices[0].message:
            assistant_message = completion.choices[0].message.content
        else:
            assistant_message = "No response generated."

        # Return the extracted message as part of the JSON response
        return jsonify({'code': assistant_message}), 200

    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred.'}), 500


@app.errorhandler(404)
async def page_not_found(e):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
async def server_error(e):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8000)
