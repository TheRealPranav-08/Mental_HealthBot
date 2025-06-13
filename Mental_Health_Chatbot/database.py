from pymongo import MongoClient
from flask_bcrypt import Bcrypt
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get MongoDB URI from environment variables or use a default for development
MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://pranavshinde0810:0Nbv5NHvilX1dzYZ@mental-health-bot.xhqbioz.mongodb.net/?retryWrites=true&w=majority&appName=mental-health-bot")

# Initialize the MongoDB client
client = MongoClient(MONGO_URI)

# Define the database
db = client.mental_health_chatbot

# Collections
users = db.users
chat_history = db.chat_history
chat_messages = db.chat_messages  # New collection for individual messages

# Initialize Bcrypt for password hashing
bcrypt = Bcrypt()

def initialize_db():
    """Initialize database with indexes and default data if needed"""
    # Create a unique index on username to prevent duplicates
    users.create_index("username", unique=True)
    users.create_index("email", unique=True)
    
    # Create indexes for chat history
    chat_history.create_index([("user_id", 1), ("timestamp", -1)])
    
    # Create indexes for chat messages
    chat_messages.create_index([("user_id", 1), ("session_id", 1), ("timestamp", 1)])
    chat_messages.create_index([("user_id", 1), ("timestamp", -1)])
    
    print("Database initialized successfully")

if __name__ == "__main__":
    # This will run if this script is executed directly
    initialize_db()