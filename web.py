from flask import Flask, render_template, request, jsonify

from Functions.Data import MK_File
from Functions.Main_Response import process_prompt

app = Flask(__name__)
log_file = MK_File()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Call the process_prompt function directly
    response = process_prompt(user_message, log_file)

    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(host="localhost", port=80, debug=True)
