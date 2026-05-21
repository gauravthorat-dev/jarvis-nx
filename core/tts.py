import pyttsx3
import textwrap


def speak(text: str):
    if not text or not text.strip():
        return

    print("Jarvis:", textwrap.fill(text, width=120))

    try:
        # 🔹 Create a fresh engine every time — fixes "speaks only once" bug on Windows
        engine = pyttsx3.init()

        voices = engine.getProperty('voices')
        # Pick David (male) if available
        for v in voices:
            if 'david' in v.name.lower():
                engine.setProperty('voice', v.id)
                break

        engine.setProperty('rate', 165)
        engine.setProperty('volume', 1.0)

        engine.say(text)
        engine.runAndWait()

        # 🔹 Explicitly stop the engine loop so next call starts clean
        engine.stop()

    except Exception as e:
        print(f"TTS error: {e}")