import pyautogui
from core.tts import speak

def pause_video(): speak("Pausing video."); pyautogui.hotkey('k')
def resume_video(): speak("Resuming playback."); pyautogui.hotkey('k')
def skip_ad():
    speak("Skipping ad."); pyautogui.press('l')
    try: pyautogui.click(x=1300,y=700)
    except: pass
def next_video(): speak("Next video."); pyautogui.hotkey('shift','n')
def toggle_mute(query:str): speak("Unmuting" if "unmute" in query else "Muting"); pyautogui.hotkey('m')
