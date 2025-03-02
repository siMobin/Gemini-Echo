import os
import PIL
import json
from google import genai
from Functions.Data import MK_File
from Functions.Files import upload_video
from werkzeug.utils import secure_filename
from Functions.Main_Response import process_prompt
from flask import Flask, render_template, request, jsonify

client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))
app = Flask(__name__)
log_file = MK_File()

# Set the upload folder for media files
UPLOAD_FOLDER = "data"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Load keywords.json to detect file types
with open("instructions/keywords.json") as f:
    keywords = json.load(f)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.form.get("message")
    media_file = request.files.get("media")

    # Debugging log to check if message and media file are received
    print(f"Received user message: {user_message}")
    print(f"Received media file: {media_file}")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Initialize media variables
    image = None
    media_audio = None
    media_video = None

    # Check if the file is valid and allowed
    if media_file:
        filename = secure_filename(media_file.filename)
        file_extension = f".{filename.rsplit('.', 1)[1].lower()}"

        # Debug
        print(f"File extension: {file_extension}")  # Debugging line
        # Save the file to the server
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        media_file.save(file_path)

        # Check file type and set the appropriate file path variable
        if file_extension in keywords["images"]:
            image = PIL.Image.open(file_path)
        elif file_extension in keywords["audios"]:
            media_audio = client.files.upload(file=file_path)
        elif file_extension in keywords["videos"]:
            media_video = upload_video(file_path, client)
        else:
            print(f"Unsupported file type: {file_extension}")  # Debugging line
            return jsonify({"error": "Unsupported file type"}), 400
    else:
        print("No media file uploaded or unsupported file type.")  # Debugging line

    response = process_prompt(
        user_message,
        log_file,
        image=image,
        media_audio=media_audio,
        media_video=media_video,
    )

    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
