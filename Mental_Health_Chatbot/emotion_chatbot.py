from transformers import pipeline

# Load the emotion detection pipeline
classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=1)

# Map detected emotion to chatbot reply
emotion_responses = {
    "anger": "I sense you're upset. Do you want to talk about what's making you angry?",
    "joy": "That's great to hear! What made you feel so happy?",
    "sadness": "I'm really sorry you're feeling down. I'm here for you.",
    "fear": "It sounds like something is worrying you. Want to talk about it?",
    "disgust": "That seems to have really bothered you. I'm listening.",
    "surprise": "Whoa! That must’ve been unexpected. Want to share more?",
    "neutral": "Tell me more about what's on your mind."
}

print("Welcome to the Emotion Support Chatbot!")
print("Type 'exit' to end the chat.")

while True:
    user_input = input("You: ")
    
    if user_input.lower() == "exit":
        print("Bot: Take care! I'm always here if you need someone to talk to. 😊")
        break
    
    # Detect emotion
    result = classifier(user_input)
    detected_emotion = result[0][0]['label'].lower()

    # Choose response
    response = emotion_responses.get(detected_emotion, "I'm here to talk whenever you're ready.")
    
    print(f"Bot: {response}")
