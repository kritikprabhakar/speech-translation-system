# core.py
import speech_recognition as sr
from googletrans import Translator
import os

recognizer = sr.Recognizer()
translator = Translator()

# --------------------------
# List of all languages
# --------------------------

language_code_map = {
    "English": "en",
    "Assamese": "as",
    "Bangla": "bn",
    "Bodo": "brx",
    "Dogri": "doi",
    "Gujarati": "gu",
    "Hindi": "hi",
    "Kannada": "kn",
    "Kashmiri": "ks",
    "Konkani": "kok",
    "Maithili": "mai",
    "Malayalam": "ml",
    "Manipuri": "mni",
    "Marathi": "mr",
    "Nepali": "ne",
    "Oriya": "or",
    "Punjabi": "pa",
    "Tamil": "ta",
    "Telugu": "te",
    "Santali": "sat",
    "Sindhi": "sd",
    "Urdu": "ur",
}

# -----------------------------------
#   SPEECH RECOGNITION (FILE)
# -----------------------------------

def stt_from_file(filepath, spoken_language):
    lang_code = language_code_map[spoken_language]

    with sr.AudioFile(filepath) as source:
        audio = recognizer.record(source)
        text = recognizer.recognize_google(audio, language=lang_code)

    return text


# -----------------------------------
#   TRANSLATION
# -----------------------------------

def translate_text(input_text, source_lang, target_lang):
    src_code = language_code_map[source_lang]
    tgt_code = language_code_map[target_lang]

    translated_text = translator.translate(
        input_text,
        src=src_code,
        dest=tgt_code
    ).text

    return translated_text
