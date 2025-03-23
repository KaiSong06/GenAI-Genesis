from flask import Flask, render_template, jsonify, request
from bias_checker import reading_json, assessing_bias, return_json
from feedback import getFeedback
from returnArgs import returnArguments
from transcript import transcript
import json
import os

app = Flask(__name__)

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

@app.route("/get_feedback")
def get_feedback():
    """Fetch feedback from feedback.json file."""
    try:
        # Create the file if it doesn't exist
        if not os.path.exists("feedback.json"):
            with open("feedback.json", "w") as file:
                file.write('{"feedback": "No feedback available yet."}')
        
        # Read the feedback file
        with open("feedback.json", "r") as file:
            feedback_data = json.load(file)
        return jsonify(feedback_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500