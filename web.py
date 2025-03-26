import os
import PIL
import json
from requests import get
from google import genai
from dotenv import load_dotenv
from Functions.Data import MK_File
from werkzeug.utils import secure_filename
from Functions.getResponse import process_prompt
from Functions.Files import read_file, upload_video
from flask import Flask, render_template, request, jsonify, url_for, send_from_directory


load_dotenv()
client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))
app = Flask(__name__)
log_file = MK_File()
# Raw URL of the README file
url = "https://raw.githubusercontent.com/siMobin/Gemini-Echo/a69734c328b3ae6c0df35b704fe62671fcde65e7/README.md"
pre = get(url)

# Set the upload folder for media files
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

with open("instructions/keywords.json") as f:
    keywords = json.load(f)

with open("instructions/commands.json") as f:
    commands = json.load(f)


# Check if the request was successful
if pre.status_code == 200:
    pre_1 = "\n".join(pre.text.split("\n")[8:19])
else:
    pass

greeting = commands["web_startup"]
response = process_prompt(greeting, log_file)


@app.route("/")
def index():
    greeting = commands["web_startup"]
    response, _ = process_prompt(greeting, log_file)  # Discard the image_path
    return render_template("index.html", greeting=response, pre_1=pre_1)


@app.route("/get-keywords")
def get_keywords():
    return send_from_directory("instructions", "keywords.json")


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.form.get("message")
    media_file = request.files.get("media")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Initialize media variables
    image = None
    media_audio = None
    media_video = None
    media_path = None

    # Check if the file is valid and allowed
    if media_file:
        filename = secure_filename(media_file.filename)
        file_extension = f".{filename.rsplit('.', 1)[1].lower()}"

        # Save the file to the server
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        media_file.save(file_path)
        media_path = url_for("static", filename=f"uploads/{filename}")  # Adjusted path

        # Check file type and set the appropriate file path variable
        if file_extension in keywords["images"]:
            image = PIL.Image.open(file_path)
        elif file_extension in keywords["audios"]:
            media_audio = client.files.upload(file=file_path)
        elif file_extension in keywords["videos"]:
            media_video = upload_video(file_path, client)
        elif file_extension in keywords["documents"]:
            info = read_file(file_path)
            user_message = info + "\n\n\n" + user_message
        else:
            return jsonify({"error": "Unsupported file type"}), 400

    response, image_path = process_prompt(
        user_message,
        log_file,
        image=image,
        media_audio=media_audio,
        media_video=media_video,
    )

    return jsonify(
        {"response": response, "media": media_path, "image_path": image_path}
    )


if __name__ == "__main__":
    app.run(host=os.getenv("host"), port=os.getenv("port"), debug=os.getenv("debug"))
