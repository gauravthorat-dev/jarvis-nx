import speech_recognition as sr

recognizer = sr.Recognizer()

def listen():
    with sr.Microphone(sample_rate=16000) as source:  # higher quality
        print("🎧 Listening clearly... Speak now!")
        recognizer.adjust_for_ambient_noise(source, duration=1.5)  # handle background noise
        audio = recognizer.listen(source, timeout=None, phrase_time_limit=20)  # listen longer
    
    try:
        print("Recognizing your voice...")
        text = recognizer.recognize_google(audio, language="en-IN")  # better for Indian English
        print(f"You said: {text}")
        return text.lower()
    except sr.UnknownValueError:
        print("Sorry, I couldn’t understand clearly.")
        return ""
    except sr.RequestError:
        print("⚠️ Network error: Speech service unavailable.")
        return ""


# import whisper
# import sounddevice as sd
# import numpy as np

# model = whisper.load_model("base")  # or "small" / "medium" for more accuracy

# def listen():
#     print("🎧 Listening (Whisper)... Speak now!")
#     fs = 16000  # sampling rate
#     duration = 8  # seconds to record
#     recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
#     sd.wait()
    
#     audio = np.squeeze(recording)
#     print("Recognizing your voice...")
    
#     result = model.transcribe(audio, fp16=False, language="en")
#     text = result["text"].strip()
#     print(f"You said: {text}")
#     return text.lower()

# import speech_recognition as sr

# recognizer = sr.Recognizer()

# def listen():
#     with sr.Microphone(sample_rate=16000) as source:
#         print("🎧 Listening clearly... Speak now!")
#         recognizer.adjust_for_ambient_noise(source, duration=1.5)  # handle background noise
#         audio = recognizer.listen(source, timeout=None, phrase_time_limit=15)
    
#     try:
#         print("Recognizing your voice...")
#         # Google API for better casual command recognition
#         text = recognizer.recognize_google(audio, language="en-IN")
#         print(f"You said: {text}")
#         return text.lower()
#     except sr.UnknownValueError:
#         print("Sorry, I couldn’t understand clearly.")
#         return ""
#     except sr.RequestError:
#         print("⚠️ Network error: Speech service unavailable.")
#         return ""
