from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os, base64
from core import stt_from_file, translate_text, language_code_map

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
os.makedirs("uploads", exist_ok=True)

# --------------------------
#       PAGES
# --------------------------

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/live")
def live_page():
    return render_template("live.html")

@app.route("/file-upload")
def file_upload_page():
    return render_template("file_upload.html")

@app.route("/converse")
def converse_page():
    return render_template("converse.html")


# --------------------------
#   FILE UPLOAD STT + TRANSLATE
# --------------------------

@app.route("/translate", methods=["POST"])
def translate_audio():

    if "file" not in request.files:
        return jsonify({"error": "no file"}), 400

    f = request.files["file"]
    spoken_lang = request.form.get("spoken_language", "English")
    target_lang = request.form.get("target_language", "Hindi")

    filename = secure_filename(f.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    f.save(filepath)

    try:
        text = stt_from_file(filepath, spoken_lang)
        translated = translate_text(text, spoken_lang, target_lang)

        return jsonify({
            "transcription": text,
            "translated_text": translated
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --------------------------
#   CONVERSATION MODE: TEXT → TEXT
# --------------------------

@app.route("/converse", methods=["POST"])
def converse_api():

    input_text = request.form.get("text") or request.form.get("user1_text")
    src = request.form.get("sourceLang") or request.form.get("srcLang")
    tgt = request.form.get("targetLang") or request.form.get("tgtLang")

    if not input_text:
        return jsonify({"error": "No text"}), 400

    translated = translate_text(input_text, src, tgt)

    return jsonify({
        "original": input_text,
        "translated": translated
    })


# --------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
