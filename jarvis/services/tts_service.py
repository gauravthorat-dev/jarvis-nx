from __future__ import annotations

import logging
import textwrap
import threading

import pyttsx3

logger = logging.getLogger(__name__)


class TTSService:
    def __init__(self, rate: int = 170, volume: float = 1.0) -> None:
        self.rate = rate
        self.volume = volume
        self._lock = threading.Lock()

    def speak(self, text: str) -> None:
        if not text or not text.strip():
            return
        logger.info('Jarvis: %s', textwrap.shorten(text, width=160, placeholder='...'))
        with self._lock:
            try:
                # Create a fresh engine per call for Windows reliability.
                engine = pyttsx3.init()
                engine.setProperty('rate', self.rate)
                engine.setProperty('volume', self.volume)
                for v in engine.getProperty('voices'):
                    if 'david' in v.name.lower():
                        engine.setProperty('voice', v.id)
                        break
                engine.say(text)
                engine.runAndWait()
                engine.stop()
            except Exception as exc:
                logger.exception('TTS failed: %s', exc)

    def interrupt(self) -> None:
        with self._lock:
            return
