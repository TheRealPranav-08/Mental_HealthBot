// This would go in your chat.js or similar file that handles message sending
function sendMessage(message) {
    // Your existing code to send the message to the server
    
    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            message: message,
            input_type: 'text'
        }),
    })
    .then(response => response.json())
    .then(data => {
        // Add the response to the UI
        addMessageToChat('assistant', data.response);
        
        // Check if auto-speak is enabled
        const autoSpeakEnabled = document.getElementById('autoSpeakResponse').checked;
        if (autoSpeakEnabled) {
            speakText(data.response);
        }
    });
}

// Function to speak text
function speakText(text) {
    fetch('/speak', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: text }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'speaking') {
            // Show speech controls
            document.getElementById('speechControls').style.display = 'block';
            
            // Start status checking
            checkSpeechStatus();
        }
    });
}