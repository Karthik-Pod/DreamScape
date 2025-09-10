"""
DreamScape Flask Backend Application with Authentication
"""
import os
import json
import uuid
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from auth.user_manager import user_manager


app = Flask(__name__)
app.config['SECRET_KEY'] = 'dreamscape-secret-key-2025'
CORS(app)

@app.route('/')
def home():
    return jsonify({
        "message": "🎬 DreamScape AI Movie Platform - Backend Running!",
        "version": "1.1.0",
        "status": "online",
        "features": ["authentication", "story_management"],
        "day": 1
    })

@app.route('/api/status')
def api_status():
    return jsonify({
        "status": "online",
        "message": "DreamScape API operational - Day 1",
        "endpoints": [
            "POST /api/auth/register",
            "POST /api/auth/login", 
            "POST /api/auth/logout",
            "POST /api/auth/validate",
            "GET /api/user/<username>"
        ]
    })

# Authentication endpoints
@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        username = data.get('username', '').strip()
        password = data.get('password', '')
        email = data.get('email', '').strip()
        
        result = user_manager.register_user(username, password, email)
        
        if result["success"]:
            return jsonify(result), 201
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Registration error: {str(e)}"
        }), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        result = user_manager.login_user(username, password)
        
        if result["success"]:
            return jsonify(result), 200
        else:
            return jsonify(result), 401
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Login error: {str(e)}"
        }), 500

@app.route('/api/auth/validate', methods=['POST'])
def validate_session():
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        
        if not session_id:
            return jsonify({"valid": False, "error": "Session ID required"}), 400
        
        result = user_manager.validate_session(session_id)
        
        if result["valid"]:
            return jsonify(result), 200
        else:
            return jsonify(result), 401
            
    except Exception as e:
        return jsonify({
            "valid": False,
            "error": f"Validation error: {str(e)}"
        }), 500

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        
        result = user_manager.logout_user(session_id)
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Logout error: {str(e)}"
        }), 500

@app.route('/api/user/<username>')
def get_user_data(username):
    try:
        result = user_manager.get_user_data(username)
        
        if result["success"]:
            return jsonify(result), 200
        else:
            return jsonify(result), 404
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Error getting user data: {str(e)}"
        }), 500

@app.route('/api/test')
def test_endpoint():
    return jsonify({
        "test": "success",
        "message": "Day 1 backend is working!",
        "timestamp": "2025-09-10",
        "authentication": "enabled"
    })
@app.route('/api/story/create', methods=['POST'])
def create_story():
    data = request.get_json()
    title = data.get('title')
    genre = data.get('genre')
    mood = data.get('mood')
    idea = data.get('idea')
    username = data.get('username')

    if not (title and genre and mood and idea and username):
        return jsonify({"success": False, "error": "Missing fields"}), 400

    stories_file = "data/stories.json"
    try:
        with open(stories_file, 'r') as f:
            stories = json.load(f)
    except Exception:
        stories = {}

    story_id = str(uuid.uuid4())

    new_story = {
        "id": story_id,
        "title": title,
        "genre": genre,
        "mood": mood,
        "idea": idea,
        "created_at": datetime.now().isoformat(),
        "username": username,
        "status": "in_progress"
    }

    stories[story_id] = new_story
    with open(stories_file, 'w') as f:
        json.dump(stories, f, indent=2)

    return jsonify({"success": True, "story_id": story_id, "story": new_story})

@app.route('/api/story/analyze', methods=['POST'])
def analyze_story():
    """Run AI agent analysis on a story"""
    try:
        data = request.get_json()
        story_id = data.get('story_id')
        
        if not story_id:
            return jsonify({"success": False, "error": "Story ID required"}), 400
        
        # Load the story
        with open('data/stories.json', 'r') as f:
            stories = json.load(f)
        
        if story_id not in stories:
            return jsonify({"success": False, "error": "Story not found"}), 404
        
        story_data = stories[story_id]
        
        # Import agents
        from agents.conference_manager import conference_manager
        
        # Start agent conference
        conference_result = conference_manager.run_discussion_round(story_data, 1)
        
        return jsonify({
            "success": True,
            "story_id": story_id,
            "analysis": conference_result,
            "message": "AI agents have analyzed your story!"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Analysis failed: {str(e)}"
        }), 500

if __name__ == '__main__':
    # Create data directories
    os.makedirs('data', exist_ok=True)
    
    print("🎬 Starting DreamScape Backend - Day 1...")
    print("📡 Server: http://localhost:5000")
    print("🔐 Features: Authentication enabled")
    
    app.run(debug=True, port=5000, host='0.0.0.0')
