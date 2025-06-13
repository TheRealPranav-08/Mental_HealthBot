# import os
# from groq import Groq
# from dotenv import load_dotenv
# from flask import Flask, request, jsonify, render_template
# import io  # Add this for UTF-8 file handling
# from voice_input import get_voice_input  # Import the voice input function

# # --- begin addition ---
# # Load mental-health keywords from a separate text file
# import io

# def load_keywords(path: str):
#     kw = []
#     with io.open(path, 'r', encoding='utf-8') as f:
#         for line in f:
#             w = line.strip().lower()
#             if w and not w.startswith('#'):
#                 kw.append(w)
#     return kw

# MENTAL_HEALTH_KEYWORDS = load_keywords('mental_health_keywords.txt')

# def is_relevant_to_mental_health(message: str) -> bool:
#     msg = message.lower()
#     # returns True if *any* mental-health keyword appears
#     return any(keyword in msg for keyword in MENTAL_HEALTH_KEYWORDS)
# # --- end addition ---



# def is_relevant_to_mental_health(message: str) -> bool:
#     msg = message.lower()
#     # returns True if *any* mental-health keyword appears
#     return any(keyword in msg for keyword in MENTAL_HEALTH_KEYWORDS)
# # --- end addition ---


# # Load environment variables
# load_dotenv()

# # Initialize Flask app
# app = Flask(__name__)

# # Initialize Groq client
# client = Groq(
#     api_key="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"
# )

# # System prompt for mental health focus
# SYSTEM_PROMPT = """You are a supportive mental health chatbot. Your goal is to provide empathetic 
# responses and helpful resources. You are not a replacement for professional mental health services, 
# but you can offer a compassionate ear and general guidance. Respond with empathy, avoid judgment, 
# and encourage professional help when appropriate. Focus on being supportive, kind, and understanding.
# Always prioritize user safety. If someone expresses thoughts of self-harm or harm to others, 
# gently encourage them to seek immediate professional help."""
  
# # Make conversation_history a global variable
# # Initialize it with the system prompt
# conversation_history = [{"role": "system", "content": SYSTEM_PROMPT}]

# def process_message(user_message):
#     """Process a message through the Groq API and return the response"""
#     global conversation_history

#         # --- begin patch ---
#     # If the user asks something off-topic, refuse and steer them back
#     if not is_relevant_to_mental_health(user_message):
#         return (
#             "I’m here to support you with mental health concerns—"
#             "let’s keep our conversation focused on that. "
#             "If you have other questions, you might seek more relevant resources."
#         )
#     # --- end patch ---
    
#     # Add user message to conversation history
#     conversation_history.append({"role": "user", "content": user_message})
    
#     # Get response from Groq's LLaMa model
#     try:
#         chat_completion = client.chat.completions.create(
#             messages=conversation_history,
#             model="llama-3.3-70b-versatile",
#             temperature=0.7,
#             max_tokens=500,
#         )
        
#         # Extract the assistant's response
#         assistant_message = chat_completion.choices[0].message.content
        
#         # Add assistant response to conversation history
#         conversation_history.append({"role": "assistant", "content": assistant_message})
        
#         # Keep conversation history at a reasonable length
#         if len(conversation_history) > 20:
#             # Keep system prompt and last 9 exchanges (18 messages)
#             conversation_history = [conversation_history[0]] + conversation_history[-18:]
        
#         return assistant_message
    
#     except Exception as e:
#         print(f"Error communicating with Groq API: {str(e)}")
#         return "I'm having trouble connecting to my language model right now. Could you please try again in a moment?"

# # Function to handle voice or text input
# def process_input(input_type="text", text_input=None):
#     """Process either voice or text input through the chatbot pipeline"""
#     if input_type == "voice":
#         user_input = get_voice_input()
#         print(f"Voice input received: {user_input}")
        
#         # Check if voice recognition failed
#         if user_input.startswith(("Sorry", "No speech")):
#             return user_input
#     else:
#         user_input = text_input
    
#     # Process through our existing Groq API integration
#     return process_message(user_input)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/chat', methods=['POST'])
# def chat():
#     data = request.json
#     input_type = data.get('input_type', 'text')
    
#     if input_type == 'voice':
#         # For web-based voice input, the transcription already happened client-side
#         user_message = data.get('message', '')
#     else:
#         user_message = data.get('message', '')
    
#     response = process_message(user_message)
#     return jsonify({"response": response})

# @app.route('/voice_input', methods=['GET'])
# def voice_input_endpoint():
#     """Endpoint to capture voice from the server's microphone"""
#     # This endpoint is for direct server-side voice capture
#     # Not typically used in web apps but useful for testing
#     voice_text = get_voice_input()
    
#     if voice_text.startswith(("Sorry", "No speech")):
#         return jsonify({"success": False, "message": voice_text})
    
#     response = process_message(voice_text)
#     return jsonify({"success": True, "voice_text": voice_text, "response": response})

# if __name__ == '__main__':
#     # Create templates directory if it doesn't exist
#     os.makedirs('templates', exist_ok=True)
    
#     # Create HTML interface with voice button
#     # Use io.open with utf-8 encoding
#     with io.open('templates/index.html', 'w', encoding='utf-8') as f:
#         f.write("""
# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Mental Health Chatbot</title>
#     <style>
#         body {
#             font-family: Arial, sans-serif;
#             margin: 0;
#             padding: 0;
#             background-color: #f0f5ff;
#         }
#         .chat-container {
#             max-width: 800px;
#             margin: 30px auto;
#             border-radius: 10px;
#             box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
#             overflow: hidden;
#             display: flex;
#             flex-direction: column;
#             height: 80vh;
#             background-color: white;
#         }
#         .chat-header {
#             background-color: #4267B2;
#             color: white;
#             padding: 15px;
#             text-align: center;
#         }
#         .chat-header h1 {
#             margin: 0;
#             font-size: 1.5rem;
#         }
#         .chat-messages {
#             flex: 1;
#             padding: 15px;
#             overflow-y: auto;
#         }
#         .message {
#             margin-bottom: 15px;
#             padding: 10px 15px;
#             border-radius: 20px;
#             max-width: 70%;
#             word-wrap: break-word;
#         }
#         .user-message {
#             background-color: #DCF8C6;
#             margin-left: auto;
#         }
#         .bot-message {
#             background-color: #E9EBEE;
#             position: relative; /* Added for speak button positioning */
#         }
#         .chat-input {
#             display: flex;
#             padding: 15px;
#             border-top: 1px solid #e0e0e0;
#         }
#         .chat-input input {
#             flex: 1;
#             padding: 10px;
#             border: 1px solid #e0e0e0;
#             border-radius: 20px;
#             outline: none;
#         }
#         .chat-input button {
#             margin-left: 10px;
#             background-color: #4267B2;
#             color: white;
#             border: none;
#             padding: 10px 15px;
#             border-radius: 20px;
#             cursor: pointer;
#         }
#         .chat-input button:hover {
#             background-color: #365899;
#         }
#         .disclaimer {
#             text-align: center;
#             margin-top: 10px;
#             font-size: 0.8rem;
#             color: #666;
#         }
#         #voice-btn {
#             background-color: #5CB85C;
#         }
#         #voice-btn:hover {
#             background-color: #4CAE4C;
#         }
#         #voice-btn.listening {
#             background-color: #D9534F;
#             animation: pulse 1.5s infinite;
#         }
#         /* Added styles for speak button */
#         .speak-btn {
#             background-color: #F7A84B;
#             color: white;
#             border: none;
#             width: 30px;
#             height: 30px;
#             border-radius: 50%;
#             display: flex;
#             align-items: center;
#             justify-content: center;
#             position: absolute;
#             right: -15px;
#             bottom: -10px;
#             cursor: pointer;
#             font-size: 12px;
#             box-shadow: 0 2px 4px rgba(0,0,0,0.2);
#         }
#         .speak-btn:hover {
#             background-color: #E69639;
#         }
#         .speaking {
#             animation: pulse 1.5s infinite;
#         }
#         @keyframes pulse {
#             0% { opacity: 1; }
#             50% { opacity: 0.5; }
#             100% { opacity: 1; }
#         }
#     </style>
# </head>
# <body>
#     <div class="chat-container">
#         <div class="chat-header">
#             <h1>Mental Health Assistant</h1>
#         </div>
#         <div class="chat-messages" id="chat-messages">
#             <div class="message bot-message">
#                 Hello! I'm here to listen and support you. How are you feeling today? You can type or click the microphone button to speak.
#                 <button class="speak-btn" onclick="speakText(this.parentNode.textContent.trim())">🔊</button>
#             </div>
#         </div>
#         <div class="chat-input">
#             <input type="text" id="user-input" placeholder="Type your message...">
#             <button id="voice-btn"><i>Mic</i></button>
#             <button id="send-btn">Send</button>
#         </div>
#     </div>
#     <div class="disclaimer">
#         This chatbot is not a substitute for professional mental health services. 
#         If you're in crisis, please call a crisis helpline or speak with a healthcare professional.
#     </div>

#     <script>
#         document.addEventListener('DOMContentLoaded', function() {
#             const chatMessages = document.getElementById('chat-messages');
#             const userInput = document.getElementById('user-input');
#             const sendBtn = document.getElementById('send-btn');
#             const voiceBtn = document.getElementById('voice-btn');

#             function addMessage(message, isUser) {
#                 const messageDiv = document.createElement('div');
#                 messageDiv.classList.add('message');
#                 messageDiv.classList.add(isUser ? 'user-message' : 'bot-message');
#                 messageDiv.textContent = message;
                
#                 // Add speak button for bot messages
#                 if (!isUser) {
#                     const speakBtn = document.createElement('button');
#                     speakBtn.classList.add('speak-btn');
#                     speakBtn.innerHTML = '🔊';
#                     speakBtn.onclick = function() {
#                         speakText(message);
#                     };
#                     messageDiv.appendChild(speakBtn);
#                 }
                
#                 chatMessages.appendChild(messageDiv);
#                 chatMessages.scrollTop = chatMessages.scrollHeight;
#             }

#             function sendMessage(message, inputType = 'text') {
#                 if (message && message.trim()) {
#                     addMessage(message, true);
                    
#                     // Show typing indicator
#                     const typingDiv = document.createElement('div');
#                     typingDiv.classList.add('message', 'bot-message');
#                     typingDiv.textContent = 'Typing...';
#                     typingDiv.id = 'typing-indicator';
#                     chatMessages.appendChild(typingDiv);
#                     chatMessages.scrollTop = chatMessages.scrollHeight;
                    
#                     // Call API
#                     fetch('/chat', {
#                         method: 'POST',
#                         headers: {
#                             'Content-Type': 'application/json',
#                         },
#                         body: JSON.stringify({ 
#                             message: message,
#                             input_type: inputType
#                         }),
#                     })
#                     .then(response => response.json())
#                     .then(data => {
#                         // Remove typing indicator
#                         const typingIndicator = document.getElementById('typing-indicator');
#                         if (typingIndicator) {
#                             typingIndicator.remove();
#                         }
                        
#                         // Add bot response
#                         if (data.response) {
#                             addMessage(data.response, false);
#                         } else {
#                             addMessage("I'm sorry, I couldn't process your request. Please try again.", false);
#                         }
#                     })
#                     .catch(error => {
#                         // Remove typing indicator
#                         const typingIndicator = document.getElementById('typing-indicator');
#                         if (typingIndicator) {
#                             typingIndicator.remove();
#                         }
                        
#                         addMessage("I'm having trouble connecting. Please check your connection and try again.", false);
#                         console.error('Error:', error);
#                     });
#                 }
#             }

#             // Text input submission
#             sendBtn.addEventListener('click', function() {
#                 const message = userInput.value.trim();
#                 if (message) {
#                     sendMessage(message);
#                     userInput.value = '';
#                 }
#             });
            
#             userInput.addEventListener('keypress', function(e) {
#                 if (e.key === 'Enter') {
#                     const message = userInput.value.trim();
#                     if (message) {
#                         sendMessage(message);
#                         userInput.value = '';
#                     }
#                 }
#             });
            
#             // Voice input handling
#             voiceBtn.addEventListener('click', function() {
#                 if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
#                     const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
#                     const recognition = new SpeechRecognition();
                    
#                     recognition.lang = 'en-US';
#                     recognition.interimResults = false;
                    
#                     // Start listening
#                     voiceBtn.classList.add('listening');
#                     voiceBtn.innerHTML = '<i>Recording...</i>'; // Changed from emoji
                    
#                     recognition.onstart = function() {
#                         addMessage("Listening...", false);
#                     };
                    
#                     recognition.onresult = function(event) {
#                         const transcript = event.results[0][0].transcript;
#                         userInput.value = transcript;
                        
#                         // Remove the "Listening..." message
#                         const messages = chatMessages.getElementsByClassName('message');
#                         if (messages.length > 0) {
#                             const lastMessage = messages[messages.length - 1];
#                             if (lastMessage.textContent === "Listening...") {
#                                 lastMessage.remove();
#                             }
#                         }
                        
#                         // Send the transcribed message
#                         sendMessage(transcript, 'voice');
#                         userInput.value = '';
#                     };
                    
#                     recognition.onerror = function(event) {
#                         voiceBtn.classList.remove('listening');
#                         voiceBtn.innerHTML = '<i>Mic</i>'; // Changed from emoji
                        
#                         // Remove the "Listening..." message
#                         const messages = chatMessages.getElementsByClassName('message');
#                         if (messages.length > 0) {
#                             const lastMessage = messages[messages.length - 1];
#                             if (lastMessage.textContent === "Listening...") {
#                                 lastMessage.remove();
#                             }
#                         }
                        
#                         addMessage("Sorry, I couldn't understand that. Please try again.", false);
#                         console.error('Speech recognition error', event.error);
#                     };
                    
#                     recognition.onend = function() {
#                         voiceBtn.classList.remove('listening');
#                         voiceBtn.innerHTML = '<i>Mic</i>'; // Changed from emoji
#                     };
                    
#                     recognition.start();
                    
#                 } else {
#                     alert("Speech recognition is not supported in your browser. Try Chrome or Edge for best results.");
#                 }
#             });
#         });

#         // Text-to-Speech function using the Web Speech API
#         function speakText(text) {
#             // Clean the text - remove the speaker emoji if it's in the text
#             text = text.replace('🔊', '');
            
#             // Get all speak buttons and remove any 'speaking' class
#             const allSpeakButtons = document.querySelectorAll('.speak-btn');
#             allSpeakButtons.forEach(btn => btn.classList.remove('speaking'));
            
#             // Add 'speaking' class to the clicked button
#             event.target.classList.add('speaking');
            
#             // Create speech synthesis
#             const speech = new SpeechSynthesisUtterance();
#             speech.text = text;
#             speech.volume = 1;
#             speech.rate = 1;
#             speech.pitch = 1;
            
#             // Get available voices and set a nice one
#             let voices = window.speechSynthesis.getVoices();
#             if (voices.length === 0) {
#                 // If voices aren't loaded yet, wait for them
#                 window.speechSynthesis.onvoiceschanged = function() {
#                     voices = window.speechSynthesis.getVoices();
#                     setVoice();
#                 };
#             } else {
#                 setVoice();
#             }
            
#             function setVoice() {
#                 // Try to find a female voice
#                 let voice = voices.find(v => v.name.includes('female') || v.name.includes('Female'));
#                 // If no female voice, get a nice default
#                 if (!voice) {
#                     voice = voices.find(v => v.lang.includes('en-US') || v.lang.includes('en-GB'));
#                 }
#                 if (voice) {
#                     speech.voice = voice;
#                 }
#             }
            
#             // When speech ends, remove the speaking class
#             speech.onend = function() {
#                 const speakingBtn = document.querySelector('.speak-btn.speaking');
#                 if (speakingBtn) {
#                     speakingBtn.classList.remove('speaking');
#                 }
#             };
            
#             // Start speaking
#             window.speechSynthesis.speak(speech);
            
#             // Also add a server-side option
#             fetch('/speak', {
#                 method: 'POST',
#                 headers: {
#                     'Content-Type': 'application/json',
#                 },
#                 body: JSON.stringify({ text: text })
#             }).catch(error => {
#                 console.log('Server-side speech not available, using browser speech only');
#             });
#         }
#     </script>
# </body>
# </html>
#         """)
    
#     # Add command-line interface option
#     import sys
#     if len(sys.argv) > 1 and sys.argv[1] == "--cli":
#         print("=" * 50)
#         print("Mental Health Chatbot with Voice Support (CLI Mode)")
#         print("=" * 50)
#         print("Type your message or enter 'voice' to use voice input.")
#         print("Type 'exit' or 'quit' to end the conversation.")
#         print("=" * 50)
        
#         # Reset conversation history for CLI
#         conversation_history = [{"role": "system", "content": SYSTEM_PROMPT}]
        
#         print("Bot: Hello! I'm here to listen and support you. How are you feeling today?")
        
#         while True:
#             user_choice = input("\nYou: ")
            
#             if user_choice.lower() == "voice":
#                 print("Activating voice input...")
#                 response = process_input(input_type="voice")
#             elif user_choice.lower() in ["exit", "quit", "bye"]:
#                 print("Thank you for using the Mental Health Chatbot. Take care!")
#                 break
#             else:
#                 response = process_input(input_type="text", text_input=user_choice)
            
#             print(f"Bot: {response}")
#     else:
#         print("Starting the Mental Health Chatbot server...")
#         app.run(debug=True)






































































# import os
# from groq import Groq
# from dotenv import load_dotenv
# from flask import Flask, request, jsonify, render_template
# import io  # Add this for UTF-8 file handling
# from voice_input import get_voice_input  # Import the voice input function

# # Load environment variables
# load_dotenv()

# # Initialize Flask app
# app = Flask(__name__)

# # Initialize Groq client
# client = Groq(
#     api_key="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"
# )

# # System prompt for mental health focus
# SYSTEM_PROMPT = """You are a supportive mental health chatbot. Your goal is to provide empathetic 
# responses and helpful resources. You are not a replacement for professional mental health services, 
# but you can offer a compassionate ear and general guidance. Respond with empathy, avoid judgment, 
# and encourage professional help when appropriate. Focus on being supportive, kind, and understanding.
# Always prioritize user safety. If someone expresses thoughts of self-harm or harm to others, 
# gently encourage them to seek immediate professional help."""
  
# # Make conversation_history a global variable
# # Initialize it with the system prompt
# conversation_history = [{"role": "system", "content": SYSTEM_PROMPT}]

# def process_message(user_message):
#     """Process a message through the Groq API and return the response"""
#     global conversation_history
    
#     # Add user message to conversation history
#     conversation_history.append({"role": "user", "content": user_message})
    
#     # Get response from Groq's LLaMa model
#     try:
#         chat_completion = client.chat.completions.create(
#             messages=conversation_history,
#             model="llama-3.3-70b-versatile",
#             temperature=0.7,
#             max_tokens=500,
#         )
        
#         # Extract the assistant's response
#         assistant_message = chat_completion.choices[0].message.content
        
#         # Add assistant response to conversation history
#         conversation_history.append({"role": "assistant", "content": assistant_message})
        
#         # Keep conversation history at a reasonable length
#         if len(conversation_history) > 20:
#             # Keep system prompt and last 9 exchanges (18 messages)
#             conversation_history = [conversation_history[0]] + conversation_history[-18:]
        
#         return assistant_message
    
#     except Exception as e:
#         print(f"Error communicating with Groq API: {str(e)}")
#         return "I'm having trouble connecting to my language model right now. Could you please try again in a moment?"

# # Function to handle voice or text input
# def process_input(input_type="text", text_input=None):
#     """Process either voice or text input through the chatbot pipeline"""
#     if input_type == "voice":
#         user_input = get_voice_input()
#         print(f"Voice input received: {user_input}")
        
#         # Check if voice recognition failed
#         if user_input.startswith(("Sorry", "No speech")):
#             return user_input
#     else:
#         user_input = text_input
    
#     # Process through our existing Groq API integration
#     return process_message(user_input)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/chat', methods=['POST'])
# def chat():
#     data = request.json
#     input_type = data.get('input_type', 'text')
    
#     if input_type == 'voice':
#         # For web-based voice input, the transcription already happened client-side
#         user_message = data.get('message', '')
#     else:
#         user_message = data.get('message', '')
    
#     response = process_message(user_message)
#     return jsonify({"response": response})

# @app.route('/voice_input', methods=['GET'])
# def voice_input_endpoint():
#     """Endpoint to capture voice from the server's microphone"""
#     # This endpoint is for direct server-side voice capture
#     # Not typically used in web apps but useful for testing
#     voice_text = get_voice_input()
    
#     if voice_text.startswith(("Sorry", "No speech")):
#         return jsonify({"success": False, "message": voice_text})
    
#     response = process_message(voice_text)
#     return jsonify({"success": True, "voice_text": voice_text, "response": response})

# if __name__ == '__main__':
#     # Create templates directory if it doesn't exist
#     os.makedirs('templates', exist_ok=True)
    
#     # Create HTML interface with voice button
#     # Using r prefix to prevent unicode escape issues
#     html_content = r"""
# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Mental Health Chatbot</title>
#     <style>
#         body {
#             font-family: Arial, sans-serif;
#             margin: 0;
#             padding: 0;
#             background-color: #f0f5ff;
#         }
#         .chat-container {
#             max-width: 800px;
#             margin: 30px auto;
#             border-radius: 10px;
#             box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
#             overflow: hidden;
#             display: flex;
#             flex-direction: column;
#             height: 80vh;
#             background-color: white;
#         }
#         .chat-header {
#             background-color: #4267B2;
#             color: white;
#             padding: 15px;
#             text-align: center;
#         }
#         .chat-header h1 {
#             margin: 0;
#             font-size: 1.5rem;
#         }
#         .chat-messages {
#             flex: 1;
#             padding: 15px;
#             overflow-y: auto;
#         }
#         .message {
#             margin-bottom: 15px;
#             padding: 10px 15px;
#             border-radius: 20px;
#             max-width: 70%;
#             word-wrap: break-word;
#         }
#         .user-message {
#             background-color: #DCF8C6;
#             margin-left: auto;
#         }
#         .bot-message {
#             background-color: #E9EBEE;
#             position: relative; /* Added for speak button positioning */
#         }
#         .chat-input {
#             display: flex;
#             padding: 15px;
#             border-top: 1px solid #e0e0e0;
#         }
#         .chat-input input {
#             flex: 1;
#             padding: 10px;
#             border: 1px solid #e0e0e0;
#             border-radius: 20px;
#             outline: none;
#         }
#         .chat-input button {
#             margin-left: 10px;
#             background-color: #4267B2;
#             color: white;
#             border: none;
#             padding: 10px 15px;
#             border-radius: 20px;
#             cursor: pointer;
#         }
#         .chat-input button:hover {
#             background-color: #365899;
#         }
#         .disclaimer {
#             text-align: center;
#             margin-top: 10px;
#             font-size: 0.8rem;
#             color: #666;
#         }
#         #voice-btn {
#             background-color: #5CB85C;
#         }
#         #voice-btn:hover {
#             background-color: #4CAE4C;
#         }
#         #voice-btn.listening {
#             background-color: #D9534F;
#             animation: pulse 1.5s infinite;
#         }
#         /* Audio control buttons styling */
#         .audio-controls {
#             display: flex;
#             align-items: center;
#             position: absolute;
#             right: -15px;
#             bottom: -10px;
#         }
#         .speak-btn, .pause-btn {
#             width: 30px;
#             height: 30px;
#             border-radius: 50%;
#             display: flex;
#             align-items: center;
#             justify-content: center;
#             cursor: pointer;
#             font-size: 12px;
#             box-shadow: 0 2px 4px rgba(0,0,0,0.2);
#             margin-left: 5px;
#             border: none;
#             color: white;
#         }
#         .speak-btn {
#             background-color: #F7A84B;
#         }
#         .speak-btn:hover {
#             background-color: #E69639;
#         }
#         .pause-btn {
#             background-color: #4267B2;
#             display: none; /* Hidden by default */
#         }
#         .pause-btn:hover {
#             background-color: #365899;
#         }
#         .speaking {
#             animation: pulse 1.5s infinite;
#         }
#         @keyframes pulse {
#             0% { opacity: 1; }
#             50% { opacity: 0.5; }
#             100% { opacity: 1; }
#         }
#     </style>
# </head>
# <body>
#     <div class="chat-container">
#         <div class="chat-header">
#             <h1>Mental Health Assistant</h1>
#         </div>
#         <div class="chat-messages" id="chat-messages">
#             <div class="message bot-message">
#                 Hello! I'm here to listen and support you. How are you feeling today? You can type or click the microphone button to speak.
#                 <div class="audio-controls">
#                     <button class="speak-btn" onclick="speakText(this.parentNode.parentNode)">🔊</button>
#                     <button class="pause-btn" onclick="pauseSpeech(this.parentNode.parentNode)">⏸️</button>
#                 </div>
#             </div>
#         </div>
#         <div class="chat-input">
#             <input type="text" id="user-input" placeholder="Type your message...">
#             <button id="voice-btn"><i>Mic</i></button>
#             <button id="send-btn">Send</button>
#         </div>
#     </div>
#     <div class="disclaimer">
#         This chatbot is not a substitute for professional mental health services. 
#         If you're in crisis, please call a crisis helpline or speak with a healthcare professional.
#     </div>

#     <script>
#         // Store speech synthesis objects globally
#         let currentSpeech = null;
#         let selectedVoice = null;

#         document.addEventListener('DOMContentLoaded', function() {
#             const chatMessages = document.getElementById('chat-messages');
#             const userInput = document.getElementById('user-input');
#             const sendBtn = document.getElementById('send-btn');
#             const voiceBtn = document.getElementById('voice-btn');

#             // Initialize speech synthesis and preload voices
#             initSpeechSynthesis();
            
#             function addMessage(message, isUser) {
#                 const messageDiv = document.createElement('div');
#                 messageDiv.classList.add('message');
#                 messageDiv.classList.add(isUser ? 'user-message' : 'bot-message');
#                 messageDiv.textContent = message;
                
#                 // Add audio controls for bot messages
#                 if (!isUser) {
#                     const audioControls = document.createElement('div');
#                     audioControls.classList.add('audio-controls');
                    
#                     const speakBtn = document.createElement('button');
#                     speakBtn.classList.add('speak-btn');
#                     speakBtn.innerHTML = '🔊';
#                     speakBtn.onclick = function() {
#                         speakText(messageDiv);
#                     };
                    
#                     const pauseBtn = document.createElement('button');
#                     pauseBtn.classList.add('pause-btn');
#                     pauseBtn.innerHTML = '⏸️';
#                     pauseBtn.onclick = function() {
#                         pauseSpeech(messageDiv);
#                     };
                    
#                     audioControls.appendChild(speakBtn);
#                     audioControls.appendChild(pauseBtn);
#                     messageDiv.appendChild(audioControls);
#                 }
                
#                 chatMessages.appendChild(messageDiv);
#                 chatMessages.scrollTop = chatMessages.scrollHeight;
#             }

#             function sendMessage(message, inputType = 'text') {
#                 if (message && message.trim()) {
#                     addMessage(message, true);
                    
#                     // Show typing indicator
#                     const typingDiv = document.createElement('div');
#                     typingDiv.classList.add('message', 'bot-message');
#                     typingDiv.textContent = 'Typing...';
#                     typingDiv.id = 'typing-indicator';
#                     chatMessages.appendChild(typingDiv);
#                     chatMessages.scrollTop = chatMessages.scrollHeight;
                    
#                     // Call API
#                     fetch('/chat', {
#                         method: 'POST',
#                         headers: {
#                             'Content-Type': 'application/json',
#                         },
#                         body: JSON.stringify({ 
#                             message: message,
#                             input_type: inputType
#                         }),
#                     })
#                     .then(response => response.json())
#                     .then(data => {
#                         // Remove typing indicator
#                         const typingIndicator = document.getElementById('typing-indicator');
#                         if (typingIndicator) {
#                             typingIndicator.remove();
#                         }
                        
#                         // Add bot response
#                         if (data.response) {
#                             addMessage(data.response, false);
#                         } else {
#                             addMessage("I'm sorry, I couldn't process your request. Please try again.", false);
#                         }
#                     })
#                     .catch(error => {
#                         // Remove typing indicator
#                         const typingIndicator = document.getElementById('typing-indicator');
#                         if (typingIndicator) {
#                             typingIndicator.remove();
#                         }
                        
#                         addMessage("I'm having trouble connecting. Please check your connection and try again.", false);
#                         console.error('Error:', error);
#                     });
#                 }
#             }

#             // Text input submission
#             sendBtn.addEventListener('click', function() {
#                 const message = userInput.value.trim();
#                 if (message) {
#                     sendMessage(message);
#                     userInput.value = '';
#                 }
#             });
            
#             userInput.addEventListener('keypress', function(e) {
#                 if (e.key === 'Enter') {
#                     const message = userInput.value.trim();
#                     if (message) {
#                         sendMessage(message);
#                         userInput.value = '';
#                     }
#                 }
#             });
            
#             // Voice input handling
#             voiceBtn.addEventListener('click', function() {
#                 if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
#                     const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
#                     const recognition = new SpeechRecognition();
                    
#                     recognition.lang = 'en-US';
#                     recognition.interimResults = false;
                    
#                     // Start listening
#                     voiceBtn.classList.add('listening');
#                     voiceBtn.innerHTML = '<i>Recording...</i>';
                    
#                     recognition.onstart = function() {
#                         addMessage("Listening...", false);
#                     };
                    
#                     recognition.onresult = function(event) {
#                         const transcript = event.results[0][0].transcript;
#                         userInput.value = transcript;
                        
#                         // Remove the "Listening..." message
#                         const messages = chatMessages.getElementsByClassName('message');
#                         if (messages.length > 0) {
#                             const lastMessage = messages[messages.length - 1];
#                             if (lastMessage.textContent === "Listening...") {
#                                 lastMessage.remove();
#                             }
#                         }
                        
#                         // Send the transcribed message
#                         sendMessage(transcript, 'voice');
#                         userInput.value = '';
#                     };
                    
#                     recognition.onerror = function(event) {
#                         voiceBtn.classList.remove('listening');
#                         voiceBtn.innerHTML = '<i>Mic</i>';
                        
#                         // Remove the "Listening..." message
#                         const messages = chatMessages.getElementsByClassName('message');
#                         if (messages.length > 0) {
#                             const lastMessage = messages[messages.length - 1];
#                             if (lastMessage.textContent === "Listening...") {
#                                 lastMessage.remove();
#                             }
#                         }
                        
#                         addMessage("Sorry, I couldn't understand that. Please try again.", false);
#                         console.error('Speech recognition error', event.error);
#                     };
                    
#                     recognition.onend = function() {
#                         voiceBtn.classList.remove('listening');
#                         voiceBtn.innerHTML = '<i>Mic</i>';
#                     };
                    
#                     recognition.start();
                    
#                 } else {
#                     alert("Speech recognition is not supported in your browser. Try Chrome or Edge for best results.");
#                 }
#             });
#         });

#         // Initialize speech synthesis and preload voices
#         function initSpeechSynthesis() {
#             // Load voices as soon as possible
#             function loadVoices() {
#                 let voices = window.speechSynthesis.getVoices();
#                 if (voices.length > 0) {
#                     // Try to find a nice female voice
#                     selectedVoice = voices.find(v => 
#                         (v.name.includes('female') || v.name.includes('Female')) && 
#                         (v.lang.includes('en-US') || v.lang.includes('en-GB'))
#                     );
                    
#                     // If no female voice found, try to get any English voice
#                     if (!selectedVoice) {
#                         selectedVoice = voices.find(v => 
#                             v.lang.includes('en-US') || v.lang.includes('en-GB')
#                         );
#                     }
                    
#                     // If still no voice, just use the first available voice
#                     if (!selectedVoice && voices.length > 0) {
#                         selectedVoice = voices[0];
#                     }
                    
#                     console.log("Selected voice:", selectedVoice ? selectedVoice.name : "None");
#                 }
#             }
            
#             // Load voices initially
#             loadVoices();
            
#             // Re-load voices if they weren't ready initially
#             if (window.speechSynthesis.onvoiceschanged !== undefined) {
#                 window.speechSynthesis.onvoiceschanged = loadVoices;
#             }
#         }

#         // Text-to-Speech function using the Web Speech API
#         function speakText(messageDiv) {
#             // Stop any previous speech
#             if (window.speechSynthesis.speaking) {
#                 window.speechSynthesis.cancel();
#             }
            
#             // Get the text content without the buttons
#             let text = messageDiv.textContent.trim();
            
#             // Create a copy of the text without emoji characters
#             text = text.replace(/[\u{1F600}-\u{1F64F}\u{1F300}-\u{1F5FF}\u{1F680}-\u{1F6FF}\u{1F700}-\u{1F77F}\u{1F780}-\u{1F7FF}\u{1F800}-\u{1F8FF}\u{1F900}-\u{1F9FF}\u{1FA00}-\u{1FA6F}\u{1FA70}-\u{1FAFF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}]/gu, '');
            
#             // Get elements
#             const speakBtn = messageDiv.querySelector('.speak-btn');
#             const pauseBtn = messageDiv.querySelector('.pause-btn');
            
#             // Add speaking class to the speak button
#             speakBtn.classList.add('speaking');
            
#             // Show pause button
#             pauseBtn.style.display = 'flex';
            
#             // Create speech synthesis
#             currentSpeech = new SpeechSynthesisUtterance();
#             currentSpeech.text = text;
#             currentSpeech.volume = 1;
#             currentSpeech.rate = 1;
#             currentSpeech.pitch = 1;
            
#             // Set the consistent voice
#             if (selectedVoice) {
#                 currentSpeech.voice = selectedVoice;
#             }
            
#             // When speech ends, reset UI
#             currentSpeech.onend = function() {
#                 resetSpeechUI(messageDiv);
#             };
            
#             // Start speaking
#             window.speechSynthesis.speak(currentSpeech);
            
#             // Also add a server-side option (if available)
#             fetch('/speak', {
#                 method: 'POST',
#                 headers: {
#                     'Content-Type': 'application/json',
#                 },
#                 body: JSON.stringify({ text: text })
#             }).catch(error => {
#                 console.log('Server-side speech not available, using browser speech only');
#             });
#         }
        
#         // Pause speech function
#         function pauseSpeech(messageDiv) {
#             if (window.speechSynthesis.speaking) {
#                 if (window.speechSynthesis.paused) {
#                     // If paused, resume
#                     window.speechSynthesis.resume();
#                     messageDiv.querySelector('.pause-btn').innerHTML = '⏸️';
#                 } else {
#                     // If playing, pause
#                     window.speechSynthesis.pause();
#                     messageDiv.querySelector('.pause-btn').innerHTML = '▶️';
#                 }
#             }
#         }
        
#         // Reset speech UI after speech completes
#         function resetSpeechUI(messageDiv) {
#             const speakBtn = messageDiv.querySelector('.speak-btn');
#             const pauseBtn = messageDiv.querySelector('.pause-btn');
            
#             if (speakBtn) speakBtn.classList.remove('speaking');
#             if (pauseBtn) {
#                 pauseBtn.style.display = 'none';
#                 pauseBtn.innerHTML = '⏸️';
#             }
#         }
#     </script>
# </body>
# </html>
# """
    
#     # Write the HTML content to a file
#     with io.open('templates/index.html', 'w', encoding='utf-8') as f:
#         f.write(html_content)
    
#     # Add command-line interface option
#     import sys
#     if len(sys.argv) > 1 and sys.argv[1] == "--cli":
#         print("=" * 50)
#         print("Mental Health Chatbot with Voice Support (CLI Mode)")
#         print("=" * 50)
#         print("Type your message or enter 'voice' to use voice input.")
#         print("Type 'exit' or 'quit' to end the conversation.")
#         print("=" * 50)
        
#         # Reset conversation history for CLI
#         conversation_history = [{"role": "system", "content": SYSTEM_PROMPT}]
        
#         print("Bot: Hello! I'm here to listen and support you. How are you feeling today?")
        
#         while True:
#             user_choice = input("\nYou: ")
            
#             if user_choice.lower() == "voice":
#                 print("Activating voice input...")
#                 response = process_input(input_type="voice")
#             elif user_choice.lower() in ["exit", "quit", "bye"]:
#                 print("Thank you for using the Mental Health Chatbot. Take care!")
#                 break
#             else:
#                 response = process_input(input_type="text", text_input=user_choice)
            
#             print(f"Bot: {response}")
#     else:
#         print("Starting the Mental Health Chatbot server...")
#         app.run(debug=True)






































import os
from groq import Groq
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
import io  # Add this for UTF-8 file handling
from voice_input import get_voice_input  # Import the voice input function

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Initialize Groq client
client = Groq(
    api_key="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"
)

# System prompt for mental health focus
SYSTEM_PROMPT = """You are a supportive mental health chatbot. Your goal is to provide empathetic 
responses and helpful resources. You are not a replacement for professional mental health services, 
but you can offer a compassionate ear and general guidance. Respond with empathy, avoid judgment, 
and encourage professional help when appropriate. Focus on being supportive, kind, and understanding.
Always prioritize user safety. If someone expresses thoughts of self-harm or harm to others, 
gently encourage them to seek immediate professional help."""
  
# Make conversation_history a global variable
# Initialize it with the system prompt
conversation_history = [{"role": "system", "content": SYSTEM_PROMPT}]

def process_message(user_message):
    """Process a message through the Groq API and return the response"""
    global conversation_history
    
    # Add user message to conversation history
    conversation_history.append({"role": "user", "content": user_message})
    
    # Get response from Groq's LLaMa model
    try:
        chat_completion = client.chat.completions.create(
            messages=conversation_history,
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=500,
        )
        
        # Extract the assistant's response
        assistant_message = chat_completion.choices[0].message.content
        
        # Add assistant response to conversation history
        conversation_history.append({"role": "assistant", "content": assistant_message})
        
        # Keep conversation history at a reasonable length
        if len(conversation_history) > 20:
            # Keep system prompt and last 9 exchanges (18 messages)
            conversation_history = [conversation_history[0]] + conversation_history[-18:]
        
        return assistant_message
    
    except Exception as e:
        print(f"Error communicating with Groq API: {str(e)}")
        return "I'm having trouble connecting to my language model right now. Could you please try again in a moment?"

# Function to handle voice or text input
def process_input(input_type="text", text_input=None):
    """Process either voice or text input through the chatbot pipeline"""
    if input_type == "voice":
        user_input = get_voice_input()
        print(f"Voice input received: {user_input}")
        
        # Check if voice recognition failed
        if user_input.startswith(("Sorry", "No speech")):
            return user_input
    else:
        user_input = text_input
    
    # Process through our existing Groq API integration
    return process_message(user_input)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    input_type = data.get('input_type', 'text')
    
    if input_type == 'voice':
        # For web-based voice input, the transcription already happened client-side
        user_message = data.get('message', '')
    else:
        user_message = data.get('message', '')
    
    response = process_message(user_message)
    return jsonify({"response": response})

@app.route('/voice_input', methods=['GET'])
def voice_input_endpoint():
    """Endpoint to capture voice from the server's microphone"""
    # This endpoint is for direct server-side voice capture
    # Not typically used in web apps but useful for testing
    voice_text = get_voice_input()
    
    if voice_text.startswith(("Sorry", "No speech")):
        return jsonify({"success": False, "message": voice_text})
    
    response = process_message(voice_text)
    return jsonify({"success": True, "voice_text": voice_text, "response": response})

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Create modern HTML interface with enhanced UI
    with io.open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mental Health Companion</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        :root {
            --primary-color: #6C63FF;
            --primary-light: #E6E5FF;
            --secondary-color: #4ECDC4;
            --user-message: #D9FFF5;
            --bot-message: #F4F6FF;
            --text-color: #333333;
            --light-text: #666666;
            --bg-color: #F9FAFC;
            --border-radius: 16px;
            --shadow: 0 4px 12px rgba(0,0,0,0.08);
            --transition: all 0.3s ease;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Poppins', sans-serif;
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-color);
            line-height: 1.6;
            overflow-x: hidden;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            display: grid;
            grid-template-columns: 1fr;
            gap: 20px;
        }

        @media (min-width: 992px) {
            .container {
                grid-template-columns: 300px 1fr;
                height: 100vh;
                padding: 30px;
            }
        }

        .sidebar {
            background: white;
            border-radius: var(--border-radius);
            box-shadow: var(--shadow);
            padding: 25px;
            height: fit-content;
        }

        @media (min-width: 992px) {
            .sidebar {
                height: calc(100vh - 60px);
                position: sticky;
                top: 30px;
                display: flex;
                flex-direction: column;
            }
        }

        .logo {
            display: flex;
            align-items: center;
            margin-bottom: 30px;
        }

        .logo img {
            width: 40px;
            height: 40px;
            margin-right: 10px;
        }

        .logo h1 {
            font-size: 1.5rem;
            font-weight: 600;
            color: var(--primary-color);
        }

        .menu {
            list-style: none;
            margin-bottom: 30px;
        }

        .menu li {
            margin-bottom: 15px;
        }

        .menu a {
            display: flex;
            align-items: center;
            text-decoration: none;
            color: var(--light-text);
            padding: 10px 15px;
            border-radius: 8px;
            transition: var(--transition);
        }

        .menu a:hover, .menu a.active {
            background-color: var(--primary-light);
            color: var(--primary-color);
        }

        .menu a i {
            margin-right: 10px;
            width: 20px;
            text-align: center;
        }

        .info-box {
            background-color: var(--primary-light);
            padding: 20px;
            border-radius: var(--border-radius);
            margin-top: auto;
        }

        .info-box h3 {
            font-weight: 600;
            font-size: 1rem;
            margin-bottom: 10px;
            color: var(--primary-color);
        }

        .info-box p {
            font-size: 0.9rem;
            color: var(--light-text);
            margin-bottom: 15px;
        }

        .info-box a {
            display: inline-block;
            padding: 8px 16px;
            background-color: var(--primary-color);
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-size: 0.9rem;
            transition: var(--transition);
        }

        .info-box a:hover {
            opacity: 0.9;
            transform: translateY(-2px);
        }

        .chat-container {
            background: white;
            border-radius: var(--border-radius);
            box-shadow: var(--shadow);
            display: flex;
            flex-direction: column;
            height: calc(100vh - 40px);
            overflow: hidden;
        }

        .chat-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 20px 25px;
            border-bottom: 1px solid #f0f0f0;
        }

        .chat-header-title {
            display: flex;
            align-items: center;
        }

        .chat-header-avatar {
            width: 40px;
            height: 40px;
            background-color: var(--primary-color);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 1.2rem;
            margin-right: 12px;
        }

        .chat-header-info h2 {
            font-size: 1.1rem;
            font-weight: 600;
        }

        .chat-header-info p {
            font-size: 0.8rem;
            color: var(--light-text);
        }

        .chat-header-actions button {
            background: none;
            border: none;
            color: var(--light-text);
            cursor: pointer;
            margin-left: 15px;
            font-size: 1.1rem;
            transition: var(--transition);
        }

        .chat-header-actions button:hover {
            color: var(--primary-color);
        }

        .chat-messages {
            flex: 1;
            padding: 25px;
            overflow-y: auto;
            background-color: var(--bg-color);
            background-image: 
                radial-gradient(var(--primary-light) 1px, transparent 1px),
                radial-gradient(var(--primary-light) 1px, transparent 1px);
            background-size: 25px 25px;
            background-position: 0 0, 12.5px 12.5px;
        }

        .message {
            margin-bottom: 20px;
            max-width: 80%;
            position: relative;
        }

        .message-content {
            padding: 15px 20px;
            border-radius: var(--border-radius);
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            position: relative;
            line-height: 1.5;
        }

        .user-message {
            margin-left: auto;
        }

        .user-message .message-content {
            background-color: var(--user-message);
            border-bottom-right-radius: 0;
        }

        .bot-message .message-content {
            background-color: var(--bot-message);
            border-bottom-left-radius: 0;
        }

        .message-avatar {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            position: absolute;
            bottom: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 0.9rem;
            box-shadow: var(--shadow);
        }

        .bot-message .message-avatar {
            background-color: var(--primary-color);
            left: -48px;
        }

        .user-message .message-avatar {
            background-color: var(--secondary-color);
            right: -48px;
        }

        .message-time {
            font-size: 0.7rem;
            color: var(--light-text);
            margin-top: 4px;
            text-align: right;
        }

        .message-actions {
            position: absolute;
            display: flex;
            align-items: center;
            bottom: -12px;
            opacity: 0;
            transform: translateY(5px);
            transition: var(--transition);
        }

        .message:hover .message-actions {
            opacity: 1;
            transform: translateY(0);
        }

        .bot-message .message-actions {
            right: 10px;
        }
        
        .user-message .message-actions {
            left: 10px;
        }

        .message-actions button {
            width: 28px;
            height: 28px;
            border-radius: 50%;
            background-color: white;
            border: none;
            box-shadow: 0 2px 6px rgba(0,0,0,0.15);
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            margin-left: 6px;
            color: var(--light-text);
            transition: var(--transition);
            font-size: 0.8rem;
        }

        .message-actions button:hover {
            background-color: var(--primary-color);
            color: white;
            transform: translateY(-2px);
        }

        .chat-input-container {
            padding: 20px 25px;
            border-top: 1px solid #f0f0f0;
            background-color: white;
            display: flex;
            align-items: center;
        }

        .chat-input-wrapper {
            flex: 1;
            position: relative;
            border-radius: 24px;
            background-color: var(--bg-color);
            overflow: hidden;
            display: flex;
            align-items: center;
            transition: var(--transition);
            border: 1px solid transparent;
        }

        .chat-input-wrapper:focus-within {
            border-color: var(--primary-color);
            box-shadow: 0 0 0 3px rgba(108, 99, 255, 0.2);
        }

        .chat-input {
            flex: 1;
            border: none;
            padding: 14px 20px;
            font-size: 1rem;
            background: none;
            outline: none;
        }

        .chat-input-actions {
            display: flex;
            padding: 0 10px;
        }

        .chat-input-actions button {
            background: none;
            border: none;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            color: var(--light-text);
            transition: var(--transition);
        }

        .chat-input-actions button:hover {
            background-color: rgba(0,0,0,0.05);
            color: var(--primary-color);
        }

        .send-btn {
            width: 50px !important;
            height: 50px !important;
            background-color: var(--primary-color) !important;
            color: white !important;
            margin-left: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            border: none;
            cursor: pointer;
            box-shadow: 0 3px 8px rgba(108, 99, 255, 0.3);
            transition: var(--transition);
        }

        .send-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 12px rgba(108, 99, 255, 0.4);
        }

        .send-btn i {
            font-size: 1.2rem;
        }

        .voice-btn.listening {
            background-color: #ff4d4f !important;
            animation: pulse 1.5s infinite;
        }

        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(255, 77, 79, 0.4); }
            70% { box-shadow: 0 0 0 10px rgba(255, 77, 79, 0); }
            100% { box-shadow: 0 0 0 0 rgba(255, 77, 79, 0); }
        }

        .speaking {
            animation: speaking-pulse 1.5s infinite;
        }

        @keyframes speaking-pulse {
            0% { box-shadow: 0 0 0 0 rgba(108, 99, 255, 0.4); }
            70% { box-shadow: 0 0 0 10px rgba(108, 99, 255, 0); }
            100% { box-shadow: 0 0 0 0 rgba(108, 99, 255, 0); }
        }

        .typing-indicator {
            display: flex;
            padding: 12px 20px;
        }

        .typing-indicator span {
            height: 8px;
            width: 8px;
            margin: 0 2px;
            background-color: #bbb;
            border-radius: 50%;
            display: inline-block;
            animation: typing 1.4s infinite ease-in-out both;
        }

        .typing-indicator span:nth-child(1) {
            animation-delay: -0.32s;
        }

        .typing-indicator span:nth-child(2) {
            animation-delay: -0.16s;
        }

        @keyframes typing {
            0%, 80%, 100% { transform: scale(0); }
            40% { transform: scale(1); }
        }

        .control-overlay {
            position: absolute;
            bottom: 15px;
            right: 15px;
            background-color: white;
            border-radius: var(--border-radius);
            box-shadow: var(--shadow);
            padding: 10px;
            display: flex;
            opacity: 0;
            transform: translateY(10px);
            transition: var(--transition);
            z-index: 100;
        }

        .message-content:hover + .control-overlay,
        .control-overlay:hover {
            opacity: 1;
            transform: translateY(0);
        }

        .speech-controls {
            display: flex;
            gap: 5px;
        }

        .speech-controls button {
            width: 36px;
            height: 36px;
            border: none;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            background-color: var(--primary-color);
            color: white;
            transition: var(--transition);
        }

        .speech-controls button:hover {
            transform: translateY(-2px);
            box-shadow: 0 3px 8px rgba(0,0,0,0.2);
        }

        .pause-btn, .resume-btn {
            display: none;
        }

        /* Responsive adjustments */
        @media (max-width: 991px) {
            .sidebar {
                display: none;
            }

            .message {
                max-width: 90%;
            }

            .bot-message .message-avatar,
            .user-message .message-avatar {
                display: none;
            }
        }

        @media (max-width: 576px) {
            .chat-header-info p {
                display: none;
            }

            .message {
                max-width: 95%;
            }

            .chat-input {
                padding: 12px 15px;
                font-size: 0.9rem;
            }
        }

        /* Dark mode */
        @media (prefers-color-scheme: dark) {
            :root {
                --bg-color: #121212;
                --text-color: #e0e0e0;
                --light-text: #a0a0a0;
                --bot-message: #262940;
                --user-message: #1e3a34;
                --primary-light: #252440;
                --shadow: 0 4px 12px rgba(0,0,0,0.2);
            }

            body, .chat-messages {
                background-color: var(--bg-color);
            }

            .sidebar, .chat-container, .chat-input-container, .chat-header {
                background-color: #1e1e1e;
                border-color: #333;
            }

            .chat-input-wrapper {
                background-color: #2d2d2d;
            }

            .control-overlay, .message-actions button {
                background-color: #2d2d2d;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="sidebar">
            <div class="logo">
                <i class="fas fa-brain" style="font-size: 1.8rem; color: var(--primary-color);"></i>
                <h1>MindfulBot</h1>
            </div>
            <ul class="menu">
                <li><a href="#" class="active"><i class="fas fa-comment-dots"></i> Chat</a></li>
                <li><a href="#"><i class="fas fa-book"></i> Resources</a></li>
                <li><a href="#"><i class="fas fa-solid fa-lightbulb"></i> Techniques</a></li>
                <li><a href="#"><i class="fas fa-question-circle"></i> About</a></li>
            </ul>
            <div class="info-box">
                <h3>Need professional help?</h3>
                <p>If you're experiencing a mental health crisis, please reach out to a professional right away.</p>
                <a href="https://www.mentalhealthhotline.org/" target="_blank">Find Help</a>
            </div>
        </div>

        <div class="chat-container">
            <div class="chat-header">
                <div class="chat-header-title">
                    <div class="chat-header-avatar">
                        <i class="fas fa-robot"></i>
                    </div>
                    <div class="chat-header-info">
                        <h2>MindfulBot</h2>
                        <p>Your supportive mental health companion</p>
                    </div>
                </div>
                <div class="chat-header-actions">
                    <button title="Clear conversation"><i class="fas fa-trash"></i></button>
                    <button title="Settings"><i class="fas fa-cog"></i></button>
                </div>
            </div>

            <div class="chat-messages" id="chat-messages">
                <div class="message bot-message">
                    <div class="message-avatar">
                        <i class="fas fa-robot"></i>
                    </div>
                    <div class="message-content">
                        Hello! I'm here to listen and support you. How are you feeling today? You can type or click the microphone button to speak.
                    </div>
                    <div class="message-time">Now</div>
                    <div class="speech-controls">
                        <button class="speak-btn" onclick="speakText(this.parentNode.parentNode)" title="Listen">
                            <i class="fas fa-volume-up"></i>
                        </button>
                        <button class="pause-btn" onclick="pauseSpeech()" title="Pause">
                            <i class="fas fa-pause"></i>
                        </button>
                        <button class="resume-btn" onclick="resumeSpeech()" title="Resume">
                            <i class="fas fa-play"></i>
                        </button>
                    </div>
                </div>
            </div>

            <div class="chat-input-container">
                <div class="chat-input-wrapper">
                    <input type="text" id="user-input" class="chat-input" placeholder="Type your message here...">
                    <div class="chat-input-actions">
                        <button class="voice-btn" id="voice-btn" title="Voice input">
                            <i class="fas fa-microphone"></i>
                        </button>
                    </div>
                </div>
                <button class="send-btn" id="send-btn" title="Send message">
                    <i class="fas fa-paper-plane"></i>
                </button>
            </div>
        </div>
    </div>

    <script>
        // Global variables for speech synthesis
        let currentSpeech = null;
        let currentSpeakingBtn = null;
        let isSpeaking = false;
        let isPaused = false;
        
        document.addEventListener('DOMContentLoaded', function() {
            const chatMessages = document.getElementById('chat-messages');
            const userInput = document.getElementById('user-input');
            const sendBtn = document.getElementById('send-btn');
            const voiceBtn = document.getElementById('voice-btn');
            
            // Get current time
            function getCurrentTime() {
                const now = new Date();
                return now.getHours() + ':' + (now.getMinutes() < 10 ? '0' : '') + now.getMinutes();
            }

            // Add a message to the chat
            function addMessage(message, isUser) {
                // Stop any ongoing speech when a new message is added
                stopSpeech();
                
                const messageDiv = document.createElement('div');
                messageDiv.classList.add('message');
                messageDiv.classList.add(isUser ? 'user-message' : 'bot-message');
                
                // Create avatar
                const avatarDiv = document.createElement('div');
                avatarDiv.classList.add('message-avatar');
                avatarDiv.innerHTML = isUser ? 
                    '<i class="fas fa-user"></i>' : 
                    '<i class="fas fa-robot"></i>';
                messageDiv.appendChild(avatarDiv);
                
                // Create message content
                const contentDiv = document.createElement('div');
                contentDiv.classList.add('message-content');
                contentDiv.textContent = message;
                messageDiv.appendChild(contentDiv);
                
                // Add timestamp
                const timeDiv = document.createElement('div');
                timeDiv.classList.add('message-time');
                timeDiv.textContent = getCurrentTime();
                messageDiv.appendChild(timeDiv);
                
                // Add speech controls for bot messages
                if (!isUser) {
                    const speechControls = document.createElement('div');
                    speechControls.classList.add('speech-controls');
                    
                    const speakBtn = document.createElement('button');
                    speakBtn.classList.add('speak-btn');
                    speakBtn.innerHTML = '<i class="fas fa-volume-up"></i>';
                    speakBtn.onclick = function() {
                        speakText(messageDiv);
                    };
                    
                    const pauseBtn = document.createElement('button');
                    pauseBtn.classList.add('pause-btn');
                    pauseBtn.innerHTML = '<i class="fas fa-pause"></i>';
                    pauseBtn.onclick = function() {
                        pauseSpeech();
                    };
                    
                    const resumeBtn = document.createElement('button');
                    resumeBtn.classList.add('resume-btn');
                    resumeBtn.innerHTML = '<i class="fas fa-play"></i>';
                    resumeBtn.onclick = function() {
                        resumeSpeech();
                    };
                    
                    speechControls.appendChild(speakBtn);
                    speechControls.appendChild(pauseBtn);
                    speechControls.appendChild(resumeBtn);
                    messageDiv.appendChild(speechControls);
                }
                
                chatMessages.appendChild(messageDiv);
                chatMessages.scrollTop = chatMessages.scrollHeight;
                return messageDiv;
            }

            // Send message to the server
            function sendMessage(message, inputType = 'text') {
                if (message && message.trim()) {
                    // Add user message to chat
                    addMessage(message, true);
                    
                    // Create typing indicator
                    const typingDiv = document.createElement('div');
                    typingDiv.classList.add('message', 'bot-message');
                    
                    const typingContent = document.createElement('div');
                    typingContent.classList.add('message-content', 'typing-indicator');
                    
                    // Add the three dots
                    for (let i = 0; i < 3; i++) {
                        const dot = document.createElement('span');
                        typingContent.appendChild(dot);
                    }
                    
                    typingDiv.appendChild(typingContent);
                    typingDiv.id = 'typing-indicator';
                    chatMessages.appendChild(typingDiv);
                    chatMessages.scrollTop = chatMessages.scrollHeight;
                    
                    // Send the message to the server
                    fetch('/chat', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ 
                            message: message,
                            input_type: inputType
                        }),
                    })
                    .then(response => response.json())
                    .then(data => {
                        // Remove typing indicator
                        const typingIndicator = document.getElementById('typing-indicator');
                        if (typingIndicator) {
                            typingIndicator.remove();
                        }
                        
                        // Add bot response to chat
                        if (data.response) {
                            addMessage(data.response, false);
                        } else {
                            addMessage("I'm sorry, I couldn't process your request. Please try again.", false);
                        }
                    })
                    .catch(error => {
                        // Remove typing indicator
                        const typingIndicator = document.getElementById('typing-indicator');
                        if (typingIndicator) {
                            typingIndicator.remove();
                        }
                        
                        addMessage("I'm having trouble connecting. Please check your connection and try again.", false);
                        console.error('Error:', error);
                    });
                }
            }

            // Handle sending messages when Send button is clicked
            sendBtn.addEventListener('click', function() {
                const message = userInput.value.trim();
                if (message) {
                    sendMessage(message);
                    userInput.value = '';
                }
            });
            
            // Handle sending messages when Enter key is pressed
            userInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    const message = userInput.value.trim();
                    if (message) {
                        sendMessage(message);
                        userInput.value = '';
                    }
                }
            });
            
            // Voice input handling
            voiceBtn.addEventListener('click', function() {
                if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
                    // Stop current speech if any
                    stopSpeech();
                    
                    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                    const recognition = new SpeechRecognition();
                    
                    recognition.lang = 'en-US';
                    recognition.interimResults = false;
                    
                    // Change appearance when recording starts
                    voiceBtn.classList.add('listening');
                    voiceBtn.innerHTML = '<i class="fas fa-record-vinyl"></i>';
                    
                    recognition.onstart = function() {
                        // Create a listening indicator
                        const listeningDiv = document.createElement('div');
                        listeningDiv.classList.add('message', 'bot-message');
                        
                        const listeningContent = document.createElement('div');
                        listeningContent.classList.add('message-content');
                        listeningContent.innerHTML = '<i class="fas fa-ear"></i> Listening...';
                        listeningContent.id = 'listening-indicator';
                        
                        listeningDiv.appendChild(listeningContent);
                        chatMessages.appendChild(listeningDiv);
                        chatMessages.scrollTop = chatMessages.scrollHeight;
                    };
                    
                    recognition.onresult = function(event) {
                        const transcript = event.results[0][0].transcript;
                        userInput.value = transcript;
                        
                        // Remove the listening indicator
                        const listeningIndicator = document.getElementById('listening-indicator');
                        if (listeningIndicator) {
                            listeningIndicator.parentNode.remove();
                        }
                        
                        // Send the transcribed message
                        sendMessage(transcript, 'voice');
                        userInput.value = '';
                    };
                    
                    recognition.onerror = function(event) {
                        voiceBtn.classList.remove('listening');
                        voiceBtn.innerHTML = '<i class="fas fa-microphone"></i>';
                        
                        // Remove the listening indicator
                        const listeningIndicator = document.getElementById('listening-indicator');
                        if (listeningIndicator) {
                            listeningIndicator.parentNode.remove();
                        }
                        
                        addMessage("Sorry, I couldn't understand that. Please try again.", false);
                        console.error('Speech recognition error', event.error);
                    };
                    
                    recognition.onend = function() {
                        voiceBtn.classList.remove('listening');
                        voiceBtn.innerHTML = '<i class="fas fa-microphone"></i>';
                        
                        // Remove listening indicator if it still exists
                        const listeningIndicator = document.getElementById('listening-indicator');
                        if (listeningIndicator) {
                            listeningIndicator.parentNode.remove();
                        }
                    };
                    
                    recognition.start();
                    
                } else {
                    alert("Speech recognition is not supported in your browser. Try Chrome or Edge for best results.");
                }
            });
            
            // Initialize by focusing the input
            userInput.focus();
        });

        // Function to speak text
        function speakText(messageDiv) {
            // Stop any current speech
            stopSpeech();
            
            // Get the message text (from the message-content div)
            const textContent = messageDiv.querySelector('.message-content').textContent.trim();
            
            // Get the buttons
            const speakBtn = messageDiv.querySelector('.speak-btn');
            const pauseBtn = messageDiv.querySelector('.pause-btn');
            const resumeBtn = messageDiv.querySelector('.resume-btn');
            
            // Show the pause button, hide resume button
            if (pauseBtn) pauseBtn.style.display = 'flex';
            if (resumeBtn) resumeBtn.style.display = 'none';
            
            // Add speaking class to the speak button
            if (speakBtn) {
                speakBtn.classList.add('speaking');
                currentSpeakingBtn = speakBtn;
            }
            
            // Create speech synthesis utterance
            currentSpeech = new SpeechSynthesisUtterance();
            currentSpeech.text = textContent;
            currentSpeech.volume = 1;
            currentSpeech.rate = 1;
            currentSpeech.pitch = 1;
            
            // Get available voices and set a nice one
            let voices = window.speechSynthesis.getVoices();
            if (voices.length === 0) {
                // If voices aren't loaded yet, wait for them
                window.speechSynthesis.onvoiceschanged = function() {
                    voices = window.speechSynthesis.getVoices();
                    setVoice();
                };
            } else {
                setVoice();
            }
            
            function setVoice() {
                // Try to find a female voice first
                let voice = voices.find(v => 
                    (v.name.includes('female') || v.name.includes('Female')) && 
                    (v.lang.includes('en-US') || v.lang.includes('en-GB'))
                );
                
                // If no female voice, get any English voice
                if (!voice) {
                    voice = voices.find(v => v.lang.includes('en-US') || v.lang.includes('en-GB'));
                }
                
                // If still no voice, use the first available
                if (!voice && voices.length > 0) {
                    voice = voices[0];
                }
                
                if (voice) {
                    currentSpeech.voice = voice;
                    console.log("Using voice: " + voice.name);
                }
            }
            
            // When speech ends
            currentSpeech.onend = function() {
                resetSpeechUI();
            };
            
            // Start speaking
            window.speechSynthesis.speak(currentSpeech);
            isSpeaking = true;
            isPaused = false;
        }

        // Function to pause speech
        function pauseSpeech() {
            if (window.speechSynthesis && isSpeaking && !isPaused) {
                window.speechSynthesis.pause();
                isPaused = true;
                
                // Update UI: show resume button, hide pause button
                const activeBotMessage = document.querySelector('.bot-message .speak-btn.speaking')?.parentNode.parentNode;
                if (activeBotMessage) {
                    const pauseBtn = activeBotMessage.querySelector('.pause-btn');
                    const resumeBtn = activeBotMessage.querySelector('.resume-btn');
                    
                    if (pauseBtn) pauseBtn.style.display = 'none';
                    if (resumeBtn) resumeBtn.style.display = 'flex';
                }
            }
        }

        // Function to resume speech
        function resumeSpeech() {
            if (window.speechSynthesis && isPaused) {
                window.speechSynthesis.resume();
                isPaused = false;
                
                // Update UI: show pause button, hide resume button
                const activeBotMessage = document.querySelector('.bot-message .speak-btn.speaking')?.parentNode.parentNode;
                if (activeBotMessage) {
                    const pauseBtn = activeBotMessage.querySelector('.pause-btn');
                    const resumeBtn = activeBotMessage.querySelector('.resume-btn');
                    
                    if (pauseBtn) pauseBtn.style.display = 'flex';
                    if (resumeBtn) resumeBtn.style.display = 'none';
                }
            }
        }

        // Function to stop speech
        function stopSpeech() {
            if (window.speechSynthesis) {
                window.speechSynthesis.cancel();
                resetSpeechUI();
            }
        }

        // Reset all speech-related UI elements
        function resetSpeechUI() {
            isSpeaking = false;
            isPaused = false;
            
            // Reset all buttons to initial state
            if (currentSpeakingBtn) {
                currentSpeakingBtn.classList.remove('speaking');
                currentSpeakingBtn = null;
            }
            
            // Hide all pause/resume buttons, they should only be visible during speech
            document.querySelectorAll('.pause-btn, .resume-btn').forEach(btn => {
                btn.style.display = 'none';
            });
        }
    </script>
</body>
</html>
        """)
    
    # Add command-line interface option
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        print("=" * 50)
        print("Mental Health Chatbot with Voice Support (CLI Mode)")
        print("=" * 50)
        print("Type your message or enter 'voice' to use voice input.")
        print("Type 'exit' or 'quit' to end the conversation.")
        print("=" * 50)
        
        # Reset conversation history for CLI
        conversation_history = [{"role": "system", "content": SYSTEM_PROMPT}]
        
        print("Bot: Hello! I'm here to listen and support you. How are you feeling today?")
        
        while True:
            user_choice = input("\nYou: ")
            
            if user_choice.lower() == "voice":
                print("Activating voice input...")
                response = process_input(input_type="voice")
            elif user_choice.lower() in ["exit", "quit", "bye"]:
                print("Thank you for using the Mental Health Chatbot. Take care!")
                break
            else:
                response = process_input(input_type="text", text_input=user_choice)
            
            print(f"Bot: {response}")
    else:
        print("Starting the Mental Health Chatbot server...")
        app.run(debug=True)













































