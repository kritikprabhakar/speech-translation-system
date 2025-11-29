import tkinter as tk
from tkinter import ttk, filedialog, font
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os

recognizer = sr.Recognizer()
translator = Translator()

def start_recording():
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=10)
            spoken_language = spoken_language_dropdown.get()  # Get the selected spoken language
            text = recognizer.recognize_google(audio, language=language_code_map[spoken_language])
            transcription_box.insert(tk.END, text + "\n")
        except sr.WaitTimeoutError:
            print("Timeout occurred, please speak again.")
        except sr.UnknownValueError:
            print("Unable to recognize speech")
        except Exception as e:
            print(f"Error during recognition: {e}")

def upload_audio_file():
    file_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.wav;*.mp3")])
    if file_path:
        with sr.AudioFile(file_path) as source:
            audio = recognizer.record(source)
            spoken_language = spoken_language_dropdown.get()  # Get the selected spoken language
            try:
                text = recognizer.recognize_google(audio, language=language_code_map[spoken_language])
                transcription_box.insert(tk.END, text + "\n")
            except sr.UnknownValueError:
                print("Unable to recognize speech")
            except Exception as e:
                print(f"Error during recognition from file: {e}")

def translate_text():
    input_text = transcription_box.get("1.0", tk.END).strip()
    if not input_text:
        print("No text to translate")
        return
    input_language = spoken_language_dropdown.get()
    result_language = language_dropdown.get()
    try:
        translated_text = translator.translate(
            input_text,
            src=language_code_map[input_language],
            dest=language_code_map[result_language]
        ).text
        translation_box.delete("1.0", tk.END)
        translation_box.insert(tk.END, translated_text)

        history_entry = (
            f"Input Language: {input_language}\n"
            f"Result Language: {result_language}\n"
            f"User Input:\n{input_text}\n\n"
            f"Translated Text:\n{translated_text}\n"
            + "-"*50 + "\n"
        )
        history_listbox.insert(tk.END, history_entry)

        history_listbox.itemconfig(tk.END, font=('Arial', 12))

    except Exception as e:
        print(f"Translation Error: {e}")

def clear_text():
    transcription_box.delete("1.0", tk.END)
    translation_box.delete("1.0", tk.END)

window = tk.Tk()
window.title("Speech-to-Text Translation System")

tab_style = ttk.Style()
tab_style.configure("TNotebook.Tab", font=("Arial", 12))

notebook = ttk.Notebook(window)
notebook.pack(padx=10, pady=10, fill='both', expand=True)

tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="Translation")

spoken_language_label = tk.Label(tab1, text="Select Spoken Language:")
spoken_language_label.pack()

spoken_languages = [
    "English", "Assamese", "Bangla", "Bodo", "Dogri", "Gujarati", "Hindi", 
    "Kannada", "Kashmiri", "Konkani", "Maithili", "Malayalam", "Manipuri", 
    "Marathi", "Nepali", "Oriya", "Punjabi", "Tamil", "Telugu", "Santali", "Sindhi", "Urdu"
]

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

spoken_language_dropdown = ttk.Combobox(tab1, values=spoken_languages)
spoken_language_dropdown.current(0)  # Set default
spoken_language_dropdown.pack()

start_button = tk.Button(tab1, text="Start Recording", command=start_recording)
start_button.pack(pady=10)

upload_button = tk.Button(tab1, text="Upload Audio File", command=upload_audio_file)
upload_button.pack(pady=10)

transcription_box = tk.Text(tab1, height=10, width=50)
transcription_box.pack(pady=10)

language_label = tk.Label(tab1, text="Select Target Language:")
language_label.pack()

languages = spoken_languages 
language_dropdown = ttk.Combobox(tab1, values=languages)
language_dropdown.current(0)
language_dropdown.pack()

translate_button = tk.Button(tab1, text="Translate", command=translate_text)
translate_button.pack(pady=10)

translation_label = tk.Label(tab1, text="Translated Text:")
translation_label.pack()

translation_box = tk.Text(tab1, height=10, width=50)
translation_box.pack(pady=10)

tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="History")

history_font = font.Font(size=12)
history_listbox = tk.Listbox(tab2, height=20, width=80, font=history_font)
history_listbox.pack(padx=10, pady=10, fill='both', expand=True)


clear_button = tk.Button(tab1, text="Clear Text", command=clear_text)
clear_button.pack(pady=10)

window.mainloop()
