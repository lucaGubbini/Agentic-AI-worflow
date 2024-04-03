from quart import Quart, request, jsonify, render_template, abort
import os
import logging
from coder_agent import CoderAgent
from project_manager_agent import ProjectManagerAgent
from reviewer_agent import ReviewerAgent

# Initialize Quart app
app = Quart(__name__)

# Setup logging
logging.basicConfig(level=logging.INFO)

# Load environment variables for API configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:1234/v1")
API_KEY = os.getenv("API_KEY", "lm-studio")
TESTING_SERVICE_URL = os.getenv("TESTING_SERVICE_URL", "http://localhost:1234/v1")

# Initialize agents
project_manager = ProjectManagerAgent("Project Manager", API_BASE_URL, API_KEY)
coder = CoderAgent("Coder", API_BASE_URL, API_KEY, TESTING_SERVICE_URL)
reviewer = ReviewerAgent("Reviewer", API_BASE_URL, API_KEY)

@app.route('/')
async def home():
    return await render_template('index.html')

@app.route('/generate-code', methods=['POST'])
async def generate_code():
    data = await request.get_json()
    project_description = data.get('prompt', '')

    if not project_description:
        # Returning an error response if the project description is missing.
        app.logger.error('Prompt is required for project plan generation.')
        return jsonify({'error': 'Prompt is required for project plan generation.'}), 400

    try:
        project_plan = await project_manager.generate_project_plan(project_description)
        
        if not project_plan:
            # Handling the case where a project plan cannot be generated.
            app.logger.error('Failed to generate a project plan.')
            return jsonify({'error': 'Failed to generate a project plan.'}), 500
        
        task = {'project_plan': project_plan}
        code = await coder.perform_task(task)
        
        # Ensure to return a response even if code generation was not successful.
        return jsonify({'code': code}), 200

    except Exception as e:
        app.logger.error(f'An unexpected error occurred: {e}')
        return jsonify({'error': 'Failed to generate code due to an internal error.'}), 500



@app.errorhandler(404)
async def page_not_found(e):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
async def server_error(e):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8000)
