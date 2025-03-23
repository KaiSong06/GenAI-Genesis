from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv
from bias_checker import reading_json, assessing_bias, return_json
from feedback import getFeedback
from returnArgs import returnArguments
from transcript import transcript
import json
import os
from werkzeug.utils import secure_filename
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openAiModel = init_chat_model("gpt-4o-mini", model_provider="openai", api_key=OPENAI_API_KEY)
CohereModel = init_chat_model("command-r-plus", model_provider="cohere", api_key=COHERE_API_KEY)

app = Flask(__name__)

CONVERSATION_FILE = "conversations.json"
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure conversations.json exists
if not os.path.exists(CONVERSATION_FILE):
    with open(CONVERSATION_FILE, "w") as file:
        file.write("[]")

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

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
                file.write('[]')
        
        # Read the feedback file
        with open("feedback.json", "r") as file:
            feedback_data = json.load(file)
        return jsonify(feedback_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/generate_feedback", methods=["POST"])
def generate_feedback():
    """Generate feedback using the getFeedback function."""
    try:
        feedback = getFeedback(CohereModel)
        return jsonify(feedback), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/generate_arguments", methods=["POST"])
def generate_arguments():
    """Generate arguments using the returnArguments function."""
    try:
        argument = request.json.get("argument")
        if not argument:
            return jsonify({"error": "Argument is required"}), 400
        result = returnArguments(argument, CohereModel)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/transcribe", methods=["POST"])
def transcribe():
    """Transcribe audio using the transcript function."""
    try:
        audio_file = request.files.get("audio")
        print("Transcribing audio")
        if not audio_file:
            return jsonify({"error": "Audio file is required"}), 400

        # Save the audio file
        print(f"Received audio file: {audio_file.filename}")
        audio_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_file.filename)
        audio_file.save(audio_path)
        print(f"Audio file saved to {audio_path}")

        # Transcribe the audio file
        transcription = transcript(audio_path)
        print("Transcription complete")
        return jsonify(transcription), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/assess_bias", methods=["POST"])
def assess_bias():
    """Assess bias using the assessing_bias function."""
    try:
        data = request.json.get("data")
        if not data:
            return jsonify({"error": "Data is required"}), 400
        bias_assessment = assessing_bias(data, openAiModel)
        return jsonify(bias_assessment), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/return_json", methods=["GET"])
def return_json_route():
    """Return JSON data using the return_json function."""
    try:
        data = return_json()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/process_conversation", methods=["POST"])
def process_conversation():
    """Process the conversation to generate feedback and analysis"""
    print("Processing conversation")
    try:
        # Read the latest conversation
        with open(CONVERSATION_FILE, "r") as file:
            conversations = json.load(file)
            
        if not conversations:
            return jsonify({"error": "No conversation to process"}), 400
            
        latest_conversation = conversations[-1]
        
        # Process the conversation through your various modules
        # 1. Check for bias
        bias_data = assessing_bias(reading_json(latest_conversation))
        with open("bias.json", "w") as file:
            json.dump(bias_data, file)
            
        # 2. Generate arguments
        arguments = returnArguments(latest_conversation)
        with open("arguments.json", "w") as file:
            json.dump({"arguments": arguments}, file)
            
        # 3. Process transcript
        transcript_data = transcript(latest_conversation)
        with open("transcript.json", "w") as file:
            json.dump({"transcript": transcript_data}, file)
            
        # 4. Generate feedback
        feedback_data = getFeedback(latest_conversation, bias_data, arguments)
        with open("feedback.json", "w") as file:
            json.dump({"feedback": feedback_data}, file)
            
        return jsonify({"message": "Processing complete"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)