import pywhatkit, webbrowser, time, os, sys
from core.tts import speak

def play_youtube(search_query: str):
    speak(f"Playing {search_query} on YouTube, Sir.")
    try:
        pywhatkit.playonyt(search_query)
        time.sleep(6)
    except Exception as e:
        speak("Couldn't open YouTube.")

def open_youtube():
    speak("Opening YouTube for you, Sir.")
    url = "https://www.youtube.com"
    try:
        # Try standard library first
        opened = webbrowser.open_new_tab(url)
        if not opened and sys.platform.startswith('win'):
            # Fallback for some Windows environments
            try:
                os.startfile(url)
                return
            except Exception:
                pass
        return
    except Exception as e:
        # Last resort for Windows
        if sys.platform.startswith('win'):
            try:
                os.startfile(url)
                return
            except Exception:
                pass
    speak("Couldn't open the web browser on this machine.")
