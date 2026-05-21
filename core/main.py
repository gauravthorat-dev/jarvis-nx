import datetime, random, wikipedia, pickle
from core.listen import listen
from core.tts import speak
from core.llama_helper import ask_llama
from core.news import get_latest_info
from core.youtube_helper import play_youtube, open_youtube
from core.youtube_controls import pause_video, resume_video, skip_ad, next_video, toggle_mute
from responses import get_response

# Load intent model
model, vectorizer = None, None
try:
    with open("data/jarvis_model.pkl","rb") as f: model = pickle.load(f)
    with open("data/jarvis_vectorizer.pkl","rb") as f: vectorizer = pickle.load(f)
    print("✅ Intent model loaded")
except: print("⚠️ Model not found. Skipping intent recognition.")

def main():
    speak("System online. Jarvis standing by.")
    while True:
        query = listen().strip()
        if not query: continue
        q_lower = query.lower()

        # Exit
        if any(w in q_lower for w in ["exit","bye","quit","shutdown"]):
            speak(get_response("goodbye")); break

        # Time & Date
        if "time" in q_lower: speak(datetime.datetime.now().strftime("The time is %I:%M %p, Sir.")); continue
        if "date" in q_lower: speak(datetime.datetime.now().strftime("Today is %A, %d %B %Y.")); continue

        # News
        if any(w in q_lower for w in ["today","latest","news","update","trending","current"]):
            speak("Fetching latest headlines, Sir.")
            info = get_latest_info(query)
            if info and "Sorry" not in info:
                for line in info.splitlines()[1:]: speak(line)
            else: speak(info)
            continue

        # Wikipedia / LLaMA
        if any(kw in q_lower for kw in ["what is","who is","tell me about","where is"]):
            try: speak(wikipedia.summary(query,sentences=2))
            except wikipedia.DisambiguationError as e:
                opt = e.options[0] if e.options else None
                if opt: speak(wikipedia.summary(opt,sentences=2))
                else: speak("Multiple entries, be specific, Sir.")
            except: speak(ask_llama(f"Explain briefly: {query}"))
            continue

        # YouTube
        if "open youtube" in q_lower:
            open_youtube()
            speak("What would you like to play?"); song = listen().strip()
            if song: play_youtube(song)
            continue
        if q_lower.startswith("play "): play_youtube(q_lower.replace("play","").strip()); continue

        # YouTube Controls
        if "pause" in q_lower: pause_video(); continue
        if "resume" in q_lower or "play video" in q_lower: resume_video(); continue
        if "skip ad" in q_lower or "skip add" in q_lower: skip_ad(); continue
        if "next" in q_lower: next_video(); continue
        if "mute" in q_lower or "unmute" in q_lower: toggle_mute(q_lower); continue

        # Intent model
        predicted_tag = None
        if model and vectorizer:
            try:
                X = vectorizer.transform([query])
                predicted_tag = model.predict(X)[0]
            except: predicted_tag=None
        if predicted_tag: speak(get_response(predicted_tag)); continue

        # LLaMA fallback
        speak("Let me think about that, Sir...")
        answer = ask_llama(f"You are Jarvis. User: {query}\nJarvis:")
        speak(answer if answer else "Couldn't get answer.")
