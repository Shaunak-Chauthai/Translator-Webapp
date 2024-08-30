from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .services import SpeechRecognitionService, TranslationService, TextToSpeechService
import os

@csrf_exempt
def process_customer_audio(request):
    if request.method == 'POST':
        audio_file = request.FILES['audio']
        file_path = save_uploaded_file(audio_file, 'customer_audio.wav')
        
        recognizer = SpeechRecognitionService(language='es')
        spanish_text = recognizer.transcribe_audio(file_path)
        
        translator = TranslationService()
        english_text = translator.translate_text(spanish_text, 'es', 'en')
        
        tts_service = TextToSpeechService(language='en')
        english_audio_path = tts_service.text_to_speech(english_text, 'customer_output.mp3')
        
        # Clean up
        os.remove(file_path)
        
        return JsonResponse({
            'spanish_text': spanish_text,
            'english_text': english_text,
            'english_audio_url': english_audio_path
        })

@csrf_exempt
def process_agent_audio(request):
    if request.method == 'POST':
        audio_file = request.FILES['audio']
        file_path = save_uploaded_file(audio_file, 'agent_audio.wav')
        
        recognizer = SpeechRecognitionService(language='en')
        english_text = recognizer.transcribe_audio(file_path)
        
        translator = TranslationService()
        spanish_text = translator.translate_text(english_text, 'en', 'es')
        
        tts_service = TextToSpeechService(language='es')
        spanish_audio_path = tts_service.text_to_speech(spanish_text, 'agent_output.mp3')
        
        # Clean up
        os.remove(file_path)
        
        return JsonResponse({
            'english_text': english_text,
            'spanish_text': spanish_text,
            'spanish_audio_url': spanish_audio_path
        })

@csrf_exempt
def save_uploaded_file(f, filename):
    with open(filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return filename

