from quart import Quart, request, jsonify, render_template
from coder_agent import CoderAgent
from project_manager_agent import ProjectManagerAgent
from reviewer_agent import ReviewerAgent

# Instantiate the Quart app
app = Quart(__name__)

# Instantiate your agents here
project_manager = ProjectManagerAgent("Project Manager")
coder = CoderAgent("Coder")
reviewer = ReviewerAgent("Reviewer")

# Define your Quart route for serving the index.html
@app.route('/')
async def home():
    # Use render_template to render the index.html file
    return await render_template('index.html')

# Define a Quart route to serve the favicon
@app.route('/favicon.ico')
async def favicon():
    return '', 204

import traceback

@app.route('/generate-code', methods=['POST'])
async def generate_code():
    data = await request.get_json()
    prompt = data.get('prompt')

    try:
        project_plan = await project_manager.generate_project_plan(prompt)
        code = await coder.generate_code(project_plan)  # Use the new generate_code method
        review = await reviewer.review_code(code)  # Make sure this method exists

        return jsonify({'code': code, 'review': review})
    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        return jsonify({'error': str(e)}), 500
# Run the Quart app if the script is executed directly
if __name__ == '__main__':
    app.run(debug=True, port=8000)
