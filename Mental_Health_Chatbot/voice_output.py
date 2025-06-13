import pyttsx3

class VoiceOutput:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.setup_voice()
    
    def setup_voice(self):
        # Set properties for the voice
        self.engine.setProperty('rate', 150)    # Speed of speech
        self.engine.setProperty('volume', 0.9)  # Volume level
        
        # Set voice type (usually index 1 is female, 0 is male)
        voices = self.engine.getProperty('voices')
        if len(voices) > 1:
            self.engine.setProperty('voice', voices[1].id)  # Female voice
    
    def speak(self, text):
        """Convert text to speech and play it"""
        self.engine.say(text)
        self.engine.runAndWait()
    
    def adjust_rate(self, rate):
        """Adjust speaking rate (words per minute)"""
        self.engine.setProperty('rate', rate)
    
    def adjust_volume(self, volume):
        """Adjust volume (0.0 to 1.0)"""
        self.engine.setProperty('volume', volume)

# Example usage
if __name__ == "__main__":
    voice = VoiceOutput()
    voice.speak("Hello, I am your mental health companion. How are you feeling today?")