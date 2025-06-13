from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import User
from database import initialize_db, users  # Add users import here
from bson.objectid import ObjectId  # Add this import as well
from mental_health_bot import process_message, process_input, conversation_history
import pyttsx3
import threading
import os
from dotenv import load_dotenv
from datetime import datetime

import threading
from queue import Queue
import time


# Add a global variable for speech control
speech_control = {
    "is_speaking": False,
    "should_pause": False,
    "should_stop": False,
    "current_text": "",
    "queue": Queue()
}

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24))

# Initialize Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "Please log in to access this feature"
login_manager.login_message_category = "info"

# Initialize database
initialize_db()

# Initialize the text-to-speech engine
def initialize_tts_engine():
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 0.9)
    
    voices = engine.getProperty('voices')
    # For a female voice (index may vary by system)
    if len(voices) > 1:
        engine.setProperty('voice', voices[1].id)
    
    return engine

# # Text-to-speech function
# def speak_text(text):
#     engine = initialize_tts_engine() 
#     engine.say(text)
#     engine.runAndWait()




# Update your text-to-speech function
def speak_text(text, user_id=None):
    """Speak text with support for pausing and stopping"""
    global speech_control
    
    # Update the speech control state
    speech_control["is_speaking"] = True
    speech_control["should_pause"] = False
    speech_control["should_stop"] = False
    speech_control["current_text"] = text
    
    engine = initialize_tts_engine()
    
    # Split text into sentences for better pause control
    sentences = text.split('.')
    
    for sentence in sentences:
        if sentence.strip():
            # Check if we should stop completely
            if speech_control["should_stop"]:
                break
                
            # Handle pause state - wait until unpaused
            while speech_control["should_pause"] and not speech_control["should_stop"]:
                time.sleep(0.1)
                
            # If we're not stopping, speak the sentence
            if not speech_control["should_stop"]:
                engine.say(sentence.strip() + '.')
                engine.runAndWait()
    
    speech_control["is_speaking"] = False
    speech_control["current_text"] = ""

# Add routes for controlling speech
@app.route('/speak', methods=['POST'])
@login_required
def text_to_speech():
    data = request.json
    text = data.get('text', '')
    
    try:
        # Clear any previous speech and queue this new one
        speech_control["should_stop"] = True
        time.sleep(0.2)  # Give time for previous speech to stop
        
        # Start speaking in a new thread
        speech_thread = threading.Thread(target=speak_text, args=(text, current_user.get_id()))
        speech_thread.daemon = True  # Thread will close when app closes
        speech_thread.start()
        
        return jsonify({
            'status': 'speaking', 
            'text': text
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/pause-speech', methods=['POST'])
@login_required
def pause_speech():
    global speech_control
    
    if speech_control["is_speaking"]:
        speech_control["should_pause"] = not speech_control["should_pause"]
        status = "paused" if speech_control["should_pause"] else "resumed"
    else:
        status = "not_speaking"
    
    return jsonify({'status': status})

@app.route('/stop-speech', methods=['POST'])
@login_required
def stop_speech():
    global speech_control
    
    was_speaking = speech_control["is_speaking"]
    speech_control["should_stop"] = True
    speech_control["should_pause"] = False
    
    return jsonify({'status': 'stopped' if was_speaking else 'not_speaking'})

@app.route('/speech-status', methods=['GET'])
@login_required
def speech_status():
    return jsonify({
        'is_speaking': speech_control["is_speaking"],
        'is_paused': speech_control["should_pause"],
        'current_text': speech_control["current_text"]
    })

@login_manager.user_loader
def load_user(user_id):
    if not user_id or not isinstance(user_id, str):
        return None
    try:
        return User.get_by_id(user_id)
    except Exception as e:
        print(f"Error loading user: {e}")
        return None

@app.route('/')
def index():
    print(f"Is authenticated: {current_user.is_authenticated}")
    if hasattr(current_user, '_id'):
        print(f"User ID: {current_user._id}")
    print(f"Session data: {session}")
    
    if current_user.is_authenticated and hasattr(current_user, '_id') and current_user._id is not None:
        # Check if we need to start a new chat session
        if not current_user.get_active_session_id():
            current_user.start_new_chat_session()
        return render_template('index.html')
    
    # If we got here, the user isn't properly authenticated
    if current_user.is_authenticated:  # User is authenticated but missing proper attributes
        logout_user()  # Force logout
    
    session.clear()  # Clear the session
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = 'remember' in request.form
        
        user = User.authenticate(username, password)
        
        if user:
            login_user(user, remember=remember)
            # When user logs in, ensure they have an active session
            if not user.get_active_session_id():
                user.start_new_chat_session()
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Basic validation
        if not username or not email or not password:
            flash('All fields are required', 'danger')
            return render_template('signup.html')
            
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template('signup.html')
            
        # Check if user already exists
        if User.get_by_username(username):
            flash('Username already exists', 'danger')
            return render_template('signup.html')
            
        if User.get_by_email(email):
            flash('Email already exists', 'danger')
            return render_template('signup.html')
        
        # Create new user
        user = User(username=username, email=email, password=password)
        if user.save():
            flash('Account created successfully. Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Error creating account', 'danger')
    
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/clear-session')
def clear_session():
    """Development route to clear session data"""
    session.clear()
    logout_user()
    flash('Session cleared', 'info')
    return redirect(url_for('login'))

@app.route('/chat', methods=['POST'])
@login_required
def chat():
    data = request.json
    input_type = data.get('input_type', 'text')
    user_message = data.get('message', '')
    
    # Save the user message first
    current_user.save_message("user", user_message)
    
    # Process the message using your existing mental health bot logic
    if input_type == 'voice':
        response = process_message(user_message)
    else:
        response = process_message(user_message)
    
    # Save the assistant's response
    current_user.save_message("assistant", response)
    
    return jsonify({"response": response})

@app.route('/voice_input', methods=['GET'])
@login_required
def voice_input_endpoint():
    """Endpoint to capture voice from the server's microphone"""
    # This endpoint is for direct server-side voice capture
    from voice_input import get_voice_input
    voice_text = get_voice_input()
    
    if voice_text.startswith(("Sorry", "No speech")):
        return jsonify({"success": False, "message": voice_text})
    
    # Save the user's voice input
    current_user.save_message("user", voice_text)
    
    # Process the message
    response = process_message(voice_text)
    
    # Save the assistant's response
    current_user.save_message("assistant", response)
    
    return jsonify({"success": True, "voice_text": voice_text, "response": response})



@app.route('/start-new-chat')
@login_required
def start_new_chat():
    """Start a new chat session"""
    session_id = current_user.start_new_chat_session()
    if session_id:
        return redirect(url_for('index'))
    flash('Failed to create a new chat session', 'danger')
    return redirect(url_for('index'))

@app.route('/chat-history')
@login_required
def chat_history_page():
    """Show the user's chat history"""
    sessions = current_user.get_chat_sessions()
    return render_template('chat_history.html', sessions=sessions)

@app.route('/view-chat/<session_id>')
@login_required
def view_chat(session_id):
    """View a specific chat session"""
    # Activate this session for the user
    users.update_one(
        {"_id": ObjectId(current_user._id)},
        {"$set": {"active_session_id": session_id}}
    )
    
    # Load messages from this session
    messages = current_user.get_chat_messages(session_id)
    
    # Reset the conversation_history in memory with these messages
    global conversation_history
    conversation_history = [{"role": "system", "content": "You are a supportive mental health chatbot..."}]
    
    for msg in messages:
        conversation_history.append({"role": msg["role"], "content": msg["content"]})
    
    return render_template('view_chat.html', messages=messages, session_id=session_id)

@app.route('/delete-chat/<session_id>', methods=['POST'])
@login_required
def delete_chat(session_id):
    """Delete a chat session"""
    if current_user.delete_chat_session(session_id):
        flash('Chat session deleted successfully', 'success')
    else:
        flash('Failed to delete chat session', 'danger')
    return redirect(url_for('chat_history_page'))

@app.route('/rename-chat/<session_id>', methods=['POST'])
@login_required
def rename_chat(session_id):
    """Rename a chat session"""
    new_title = request.form.get('title')
    if new_title and current_user.rename_chat_session(session_id, new_title):
        flash('Chat session renamed successfully', 'success')
    else:
        flash('Failed to rename chat session', 'danger')
    return redirect(url_for('chat_history_page'))

if __name__ == '__main__':
    app.run(debug=True)