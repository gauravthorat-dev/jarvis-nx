from __future__ import annotations

import logging

import speech_recognition as sr

logger = logging.getLogger(__name__)


class SpeechService:
    def __init__(self, language: str = 'en-IN') -> None:
        self.language = language
        self.recognizer = sr.Recognizer()
        self.last_error: str = ''
        self.last_heard_text: str = ''

    def listen(self, phrase_time_limit: int = 15) -> str:
        self.last_error = ''
        self.last_heard_text = ''
        try:
            with sr.Microphone(sample_rate=16000) as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1.0)
                audio = self.recognizer.listen(source, timeout=None, phrase_time_limit=phrase_time_limit)
        except OSError as exc:
            self.last_error = f'Microphone unavailable: {exc}'
            logger.warning(self.last_error)
            return ''
        except Exception as exc:
            self.last_error = f'Microphone capture failed: {exc}'
            logger.warning(self.last_error)
            return ''
        try:
            text = self.recognizer.recognize_google(audio, language=self.language)
            self.last_heard_text = text.strip()
            return text.strip()
        except sr.UnknownValueError:
            self.last_error = 'Could not understand audio.'
            return ''
        except sr.RequestError as exc:
            self.last_error = f'Speech service unavailable: {exc}'
            logger.warning(self.last_error)
            return ''
