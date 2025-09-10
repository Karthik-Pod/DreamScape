"""
User authentication and management system for DreamScape
"""
import json
import os
import hashlib
import uuid
from datetime import datetime, timedelta
from pathlib import Path

class UserManager:
    def __init__(self):
        self.users_file = "data/users.json"
        self.sessions_file = "data/sessions.json"
        self.ensure_data_files()
    
    def ensure_data_files(self):
        """Create data files if they don't exist"""
        Path("data").mkdir(exist_ok=True)
        
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                json.dump({}, f)
        
        if not os.path.exists(self.sessions_file):
            with open(self.sessions_file, 'w') as f:
                json.dump({}, f)
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, username, password, email):
        """Register new user"""
        try:
            # Validate input
            if not username or not password or not email:
                return {"success": False, "error": "All fields are required"}
            
            if len(username) < 3:
                return {"success": False, "error": "Username must be at least 3 characters"}
            
            if len(password) < 6:
                return {"success": False, "error": "Password must be at least 6 characters"}
            
            # Load existing users
            with open(self.users_file, 'r') as f:
                users = json.load(f)
            
            # Check if username exists
            if username in users:
                return {"success": False, "error": "Username already exists"}
            
            # Check if email exists
            for user_data in users.values():
                if user_data.get("email") == email:
                    return {"success": False, "error": "Email already registered"}
            
            # Create new user
            password_hash = self.hash_password(password)
            
            users[username] = {
                "username": username,
                "email": email,
                "password_hash": password_hash,
                "created_at": datetime.now().isoformat(),
                "last_login": None,
                "stories": {},
                "preferences": {
                    "default_genre": "fantasy",
                    "default_mood": "epic",
                    "preferred_duration": "medium"
                },
                "statistics": {
                    "stories_created": 0,
                    "stories_completed": 0,
                    "discussion_rounds": 0,
                    "total_time_spent": 0
                }
            }
            
            # Save users
            with open(self.users_file, 'w') as f:
                json.dump(users, f, indent=2)
            
            return {"success": True, "message": "User registered successfully"}
            
        except Exception as e:
            return {"success": False, "error": f"Registration failed: {str(e)}"}
    
    def login_user(self, username, password):
        """Login user and create session"""
        try:
            # Load users
            with open(self.users_file, 'r') as f:
                users = json.load(f)
            
            if username not in users:
                return {"success": False, "error": "Invalid username or password"}
            
            # Verify password
            password_hash = self.hash_password(password)
            if users[username]["password_hash"] != password_hash:
                return {"success": False, "error": "Invalid username or password"}
            
            # Create session
            session_id = str(uuid.uuid4())
            
            with open(self.sessions_file, 'r') as f:
                sessions = json.load(f)
            
            sessions[session_id] = {
                "username": username,
                "created_at": datetime.now().isoformat(),
                "last_active": datetime.now().isoformat(),
                "expires_at": (datetime.now() + timedelta(hours=24)).isoformat()
            }
            
            with open(self.sessions_file, 'w') as f:
                json.dump(sessions, f, indent=2)
            
            # Update user last login
            users[username]["last_login"] = datetime.now().isoformat()
            with open(self.users_file, 'w') as f:
                json.dump(users, f, indent=2)
            
            return {
                "success": True,
                "session_id": session_id,
                "username": username,
                "user_data": {
                    "email": users[username]["email"],
                    "preferences": users[username]["preferences"],
                    "statistics": users[username]["statistics"]
                },
                "message": "Login successful"
            }
            
        except Exception as e:
            return {"success": False, "error": f"Login failed: {str(e)}"}
    
    def validate_session(self, session_id):
        """Validate user session"""
        try:
            with open(self.sessions_file, 'r') as f:
                sessions = json.load(f)
            
            if session_id not in sessions:
                return {"valid": False, "error": "Session not found"}
            
            session = sessions[session_id]
            
            # Check if session expired
            expires_at = datetime.fromisoformat(session["expires_at"])
            if datetime.now() > expires_at:
                # Remove expired session
                del sessions[session_id]
                with open(self.sessions_file, 'w') as f:
                    json.dump(sessions, f, indent=2)
                return {"valid": False, "error": "Session expired"}
            
            # Update last active
            session["last_active"] = datetime.now().isoformat()
            sessions[session_id] = session
            
            with open(self.sessions_file, 'w') as f:
                json.dump(sessions, f, indent=2)
            
            return {
                "valid": True,
                "username": session["username"],
                "session_data": session
            }
            
        except Exception as e:
            return {"valid": False, "error": f"Validation failed: {str(e)}"}
    
    def logout_user(self, session_id):
        """Logout user and remove session"""
        try:
            with open(self.sessions_file, 'r') as f:
                sessions = json.load(f)
            
            if session_id in sessions:
                del sessions[session_id]
                
                with open(self.sessions_file, 'w') as f:
                    json.dump(sessions, f, indent=2)
            
            return {"success": True, "message": "Logged out successfully"}
            
        except Exception as e:
            return {"success": False, "error": f"Logout failed: {str(e)}"}
    
    def get_user_data(self, username):
        """Get user data"""
        try:
            with open(self.users_file, 'r') as f:
                users = json.load(f)
            
            if username not in users:
                return {"success": False, "error": "User not found"}
            
            user_data = users[username].copy()
            # Remove sensitive data
            del user_data["password_hash"]
            
            return {"success": True, "user_data": user_data}
            
        except Exception as e:
            return {"success": False, "error": f"Failed to get user data: {str(e)}"}

# Global instance
user_manager = UserManager()
