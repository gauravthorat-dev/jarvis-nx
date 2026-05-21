from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

# Raw string with backslashes
model_path = "D:\jarvis_project\models\jarvis_emotion"

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)

# Create pipeline
emotion_classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)

# Test
texts = [
    "I feel so happy today!",
    "I'm really angry about what happened!",
    "I'm feeling lonely and sad.",
    "That was a wonderful surprise!",
]

for text in texts:
    result = emotion_classifier(text)
    print(f"Text: {text}")
    print(f"Predicted Emotion: {result[0]['label']}\n")
