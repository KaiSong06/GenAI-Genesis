import whisper
import json
from flask import Flask
from flask_socketio import SocketIO, send

app1 = Flask(__name__)
socketio = SocketIO(app1)

# Create the secret key
app1.config['SECRET_KEY'] = 'secret'

# Decorate the message function to handle incoming WebSocket messages
@socketio.on('message')
def message(msg):
    """
    Send a message to the client.
    """
    print('Message: ' + msg)
    send(msg, broadcast=True)

# Show client connected or disconnected
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

# Load the Whisper model (locally)
model = whisper.load_model("base")  # You can choose "base", "small", "medium", or "large"

def transcript(audio_path: str) -> dict: # Transcript
    """
    Transcribe audio to text using the Whisper model (locally).
    """
    # Transcribe the audio using the Whisper model
    result = model.transcribe(audio_path)
    print(result)
    # Create a JSON-like dictionary with transcription details
    transcription_json = {
        "text": result["text"],  # The transcribed text
     }
    
    # Return the transcription details
    return transcription_json

## Test Case

# result = transcript(r".\app\speech1.mp3")
# print(json.dumps(result, indent=4)) 
