from flask import Flask, render_template, jsonify, request
import json
import os

app = Flask(__name__, template_folder='../templates', static_folder='../static')

CONVERSATION_FILE = "conversations.json"

# Ensure conversations.json exists
if not os.path.exists(CONVERSATION_FILE):
    with open(CONVERSATION_FILE, "w") as file:
        file.write("[]")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_conversation")
def get_conversation():
    """Fetch stored conversation history from JSON file."""
    try:
        with open(CONVERSATION_FILE, "r") as file:
            conversations = json.load(file)
        return jsonify(conversations), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/clear_conversation", methods=["POST"])
def clear_conversation():
    """Clear the conversations.json file."""
    try:
        with open(CONVERSATION_FILE, "w") as file:
            file.write("[]")
        return jsonify({"message": "Chat history cleared"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
