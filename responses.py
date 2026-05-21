import random

responses = {
    "greeting":["Hello Sir!", "Hey Gaurav!", "Hi there, Sir!"],
    "goodbye":["Goodbye Sir!", "See you later!", "Take care, Gaurav!"],
    "thanks":["You're welcome!", "Glad to help!", "Anytime!"],
    "name":["I'm Jarvis, your assistant.", "Call me Jarvis."],
    "creator":["Created by Gaurav using Python."]
}

def get_response(tag:str) -> str: return random.choice(responses.get(tag, ["I don't understand that."]))
