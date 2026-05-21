import json
from datetime import datetime
import os

LOG_FILE = "interaction_log.json"

def log_interaction(user_input, jarvis_reply):
    """Save every user and Jarvis interaction in a JSON file"""
    data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user_input": user_input,
        "jarvis_reply": jarvis_reply
    }

    # If file doesn't exist, create it
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            json.dump([], f)

    # Read existing data
    with open(LOG_FILE, "r") as f:
        interactions = json.load(f)

    # Add new one
    interactions.append(data)

    # Write back to file
    with open(LOG_FILE, "w") as f:
        json.dump(interactions, f, indent=4)

    print("✅ Interaction saved.")
