from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F

# Load model and tokenizer
model_name = "SamLowe/roberta-base-go_emotions"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Load emotion labels from model config
labels = [
    "admiration", "amusement", "anger", "annoyance", "approval", "caring", "confusion", "curiosity", "desire", "disappointment",
    "disapproval", "disgust", "embarrassment", "excitement", "fear", "gratitude", "grief", "joy", "love", "nervousness",
    "optimism", "pride", "realization", "relief", "remorse", "sadness", "surprise"
]

def classify_emotion(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = F.softmax(logits, dim=1).squeeze()

    top_idx = torch.argmax(probs).item()
    top_emotion = labels[top_idx]
    top_prob = probs[top_idx].item()

    return top_emotion, top_prob, probs

# Test with example input
example = "I feel like no one cares about me anymore. I'm just tired of everything."
emotion, confidence, all_probs = classify_emotion(example)

print(f"\nDetected Emotion: {emotion}")
print(f"Confidence: {confidence:.2f}")
