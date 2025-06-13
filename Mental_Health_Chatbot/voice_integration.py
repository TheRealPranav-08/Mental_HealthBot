from voice_input import get_voice_input
# Import your existing MentalBERT modules
from mental_bert_model import preprocess_text, classify_text, generate_response

def process_input(input_type="text", text_input=None):
    """Process either text or voice input through the MentalBERT pipeline"""
    
    # Get input text either from voice or direct text input
    if input_type == "voice":
        user_input = get_voice_input()
        print(f"Voice input received: {user_input}")
        
        # Check if there was an error with voice recognition
        if user_input.startswith(("Sorry", "No speech")):
            return user_input  # Return the error message
    else:
        user_input = text_input
    
    # Process through your existing MentalBERT pipeline
    preprocessed_text = preprocess_text(user_input)
    mental_health_category = classify_text(preprocessed_text)
    response = generate_response(mental_health_category, user_input)
    
    return response