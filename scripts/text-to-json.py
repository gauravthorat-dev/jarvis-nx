import json

# Open the JSONL file
data = []
with open(r"D:\jarvis_project\data\jarvis_emotion.jsonl", "r") as f:
    for line in f:
        if line.strip():  # skip empty lines
            data.append(json.loads(line.strip()))

# Convert to Jarvis-friendly format
emotion_dict = {}
for item in data:
    emotion = item['completion'].strip()
    prompt = item['prompt'].strip()
    if emotion not in emotion_dict:
        emotion_dict[emotion] = []
    emotion_dict[emotion].append(prompt)

# Save as new JSON
with open(r"D:\jarvis_project\emotion_responses.json", "w") as f:
    json.dump(emotion_dict, f, indent=4)

print("✅ Converted to Jarvis-friendly JSON!")
