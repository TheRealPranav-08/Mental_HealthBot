import speech_recognition as sr

def get_voice_input():
    """Capture and transcribe voice input from microphone"""
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Listening... Speak now.")
        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source)
        
        try:
            print("Capturing audio...")
            audio = recognizer.listen(source, timeout=5)
            
            print("Processing speech...")
            text = recognizer.recognize_google(audio)
            print(f"Recognized: {text}")
            return text
            
        except sr.WaitTimeoutError:
            return "No speech detected. Please try again."
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand what you said."
        except sr.RequestError:
            return "Sorry, speech recognition service is currently unavailable."

# Test function - run this file directly to test voice input
if __name__ == "__main__":
    print("Testing voice recognition...")
    result = get_voice_input()
    print(f"Final result: {result}")