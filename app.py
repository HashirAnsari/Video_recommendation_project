from flask import Flask, request, jsonify, render_template
from models.content_based import get_recommendations  # Import recommendation logic
from flask import Flask, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def home():
    """
    Serve the frontend homepage.
    """
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/recommendations', methods=['POST'])
def recommendations():
    try:
        # Example input parsing
        data = request.get_json()
        username = data.get('username')
        category_id = data.get('category_id')
        mood = data.get('mood')

        # Debugging inputs
        print(f"Inputs - username: {username}, category_id: {category_id}, mood: {mood}")

        # Generate recommendations
        recommendations = get_recommendations(username=username, category_id=category_id, mood=mood)

        # Debugging recommendations
        print(f"Generated recommendations: {recommendations}")

        if not recommendations:
            return jsonify({"message": "No recommendations found."}), 200

        return jsonify({"recommendations": recommendations}), 200
    except Exception as e:
        print(f"Error in /recommendations: {e}")
        return jsonify({"error": "Internal server error"}), 500




if __name__ == '__main__':
    # Ensure necessary folders and files exist
    if not os.path.exists('templates/index.html'):
        print("Error: index.html not found in templates folder.")
    app.run(debug=True)





