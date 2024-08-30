import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os

class SpeechRecognitionService:
    def __init__(self, language):
        self.language = language
        self.recognizer = sr.Recognizer()

    def transcribe_audio(self, file_path):
        with sr.AudioFile(file_path) as source:
            audio = self.recognizer.record(source)
        try:
            text = self.recognizer.recognize_google(audio, language=self.language)
        except sr.UnknownValueError:
            text = "Could not understand audio"
        except sr.RequestError as e:
            text = f"Request error from Google Speech Recognition service; {e}"
        return text

class TranslationService:
    def __init__(self):
        self.translator = Translator()

    def translate_text(self, text, src_lang, dest_lang):
        translated = self.translator.translate(text, src=src_lang, dest=dest_lang)
        return translated.text

class TextToSpeechService:
    def __init__(self, language):
        self.language = language

    def text_to_speech(self, text, output_file):
        tts = gTTS(text=text, lang=self.language)
        tts.save(output_file)
        return output_file