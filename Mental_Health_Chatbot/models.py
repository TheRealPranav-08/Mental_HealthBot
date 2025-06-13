from database import users, chat_history, chat_messages, bcrypt
from bson.objectid import ObjectId
from datetime import datetime
import uuid
from flask_login import UserMixin

class User(UserMixin):
    """User model for authentication"""
    
    def __init__(self, username, email, password=None, _id=None):
        self.username = username
        self.email = email
        self.password = password
        self._id = _id
        
    def get_id(self):
        """Return the user ID as a string for Flask-Login"""
        return str(self._id)
    
    def save(self):
        """Save user to database"""
        if not self.password:
            raise ValueError("Password is required")
            
        # Hash the password before storing
        hashed_password = bcrypt.generate_password_hash(self.password).decode('utf-8')
        
        user_data = {
            "username": self.username,
            "email": self.email,
            "password": hashed_password,
            "created_at": datetime.utcnow(),
            "last_login": datetime.utcnow(),
            "active_session_id": None,
            "chat_histories": []
        }
        
        try:
            result = users.insert_one(user_data)
            self._id = result.inserted_id
            return True
        except Exception as e:
            print(f"Error saving user: {e}")
            return False
    
    def start_new_chat_session(self):
        """Start a new chat session and return the session ID"""
        if not self._id:
            return None
            
        session_id = str(uuid.uuid4())
        session_data = {
            "user_id": ObjectId(self._id),
            "session_id": session_id,
            "title": f"Chat on {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}",
            "started_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "message_count": 0
        }
        
        try:
            # Save the new session
            chat_history.insert_one(session_data)
            
            # Update user's active session
            users.update_one(
                {"_id": ObjectId(self._id)},
                {"$set": {"active_session_id": session_id}}
            )
            
            return session_id
        except Exception as e:
            print(f"Error creating chat session: {e}")
            return None
    
    def get_active_session_id(self):
        """Get the user's current active chat session ID"""
        if not self._id:
            return None
            
        user_data = users.find_one({"_id": ObjectId(self._id)})
        if user_data and user_data.get("active_session_id"):
            return user_data["active_session_id"]
            
        # No active session, create one
        return self.start_new_chat_session()
        
    def save_message(self, role, content):
        """Save a single message to the chat history"""
        if not self._id:
            return False
            
        # Get or create session ID
        session_id = self.get_active_session_id()
        if not session_id:
            return False
            
        timestamp = datetime.utcnow()
        
        # Create the message document
        message_data = {
            "user_id": ObjectId(self._id),
            "session_id": session_id,
            "role": role,  # "user" or "assistant"
            "content": content,
            "timestamp": timestamp
        }
        
        try:
            # Insert the message
            from database import chat_messages, chat_history
            chat_messages.insert_one(message_data)
            
            # Update the session's updated_at time and message count
            chat_history.update_one(
                {"user_id": ObjectId(self._id), "session_id": session_id},
                {
                    "$set": {"updated_at": timestamp},
                    "$inc": {"message_count": 1}
                }
            )
            
            return True
        except Exception as e:
            print(f"Error saving message: {e}")
            return False
    
    def save_chat_history(self, conversation):
        """Save entire conversation history"""
        if not self._id:
            return False
            
        # Get or create session ID
        session_id = self.get_active_session_id()
        if not session_id:
            return False
        
        # Skip the system prompt (first message) as it's not part of the conversation
        if len(conversation) > 1:
            for message in conversation[1:]:
                self.save_message(message["role"], message["content"])
        
        return True
    
    def get_chat_sessions(self, limit=10):
        """Get user's chat sessions"""
        if not self._id:
            return []
            
        try:
            sessions = list(chat_history.find(
                {"user_id": ObjectId(self._id)}
            ).sort("updated_at", -1).limit(limit))
            
            return sessions
        except Exception as e:
            print(f"Error retrieving chat sessions: {e}")
            return []
    
    def get_chat_messages(self, session_id=None, limit=50):
        """Get messages from a specific chat session or the active one"""
        if not self._id:
            return []
            
        # If no session_id provided, use the active one
        if not session_id:
            session_id = self.get_active_session_id()
            
        if not session_id:
            return []
            
        try:
            messages = list(chat_messages.find(
                {"user_id": ObjectId(self._id), "session_id": session_id}
            ).sort("timestamp", 1).limit(limit))
            
            return messages
        except Exception as e:
            print(f"Error retrieving chat messages: {e}")
            return []
    
    def rename_chat_session(self, session_id, new_title):
        """Rename a chat session"""
        if not self._id:
            return False
            
        try:
            result = chat_history.update_one(
                {"user_id": ObjectId(self._id), "session_id": session_id},
                {"$set": {"title": new_title}}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error renaming chat session: {e}")
            return False
    
    def delete_chat_session(self, session_id):
        """Delete a chat session and its messages"""
        if not self._id:
            return False
            
        try:
            # Delete the session
            chat_history.delete_one({"user_id": ObjectId(self._id), "session_id": session_id})
            
            # Delete all messages in the session
            chat_messages.delete_many({"user_id": ObjectId(self._id), "session_id": session_id})
            
            # If this was the active session, clear the active session ID
            users.update_one(
                {"_id": ObjectId(self._id), "active_session_id": session_id},
                {"$set": {"active_session_id": None}}
            )
            
            return True
        except Exception as e:
            print(f"Error deleting chat session: {e}")
            return False
            
    @staticmethod
    def get_by_username(username):
        """Get a user by username"""
        user_data = users.find_one({"username": username})
        if user_data:
            return User(
                username=user_data.get("username"),
                email=user_data.get("email"),
                _id=user_data.get("_id")
            )
        return None
    
    @staticmethod
    def get_by_email(email):
        """Get a user by email"""
        user_data = users.find_one({"email": email})
        if user_data:
            return User(
                username=user_data.get("username"),
                email=user_data.get("email"), 
                _id=user_data.get("_id")
            )
        return None
        
    @staticmethod
    def get_by_id(user_id):
        """Get a user by ID"""
        if not ObjectId.is_valid(user_id):
            return None
            
        user_data = users.find_one({"_id": ObjectId(user_id)})
        if user_data:
            return User(
                username=user_data.get("username"),
                email=user_data.get("email"),
                _id=user_data.get("_id")
            )
        return None
        
    @staticmethod
    def authenticate(username, password):
        """Authenticate a user by username/email and password"""
        # Try to find user by username or email
        user_data = users.find_one({"$or": [{"username": username}, {"email": username}]})
        
        if user_data and bcrypt.check_password_hash(user_data["password"], password):
            # Update last login
            users.update_one(
                {"_id": user_data["_id"]},
                {"$set": {"last_login": datetime.utcnow()}}
            )
            return User(
                username=user_data.get("username"),
                email=user_data.get("email"),
                _id=user_data.get("_id")
            )
        return None