# instantiate the pipeline
from pyannote.audio import Pipeline
from pyannote.audio.pipelines.utils.hook import ProgressHook
import os
import json
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN_WRITE")

#print("Current working directory:", os.getcwd())
def diarize(audio: str, output: str):
    if HF_TOKEN is None:
        raise ValueError("Hugging Face token not found. Please set HF_TOKEN in your .env file.")

    #Remove existing/past output
    if os.path.exists(output):
        os.remove(output)

    pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.0",
    use_auth_token=HF_TOKEN)

    # run the pipeline on an audio file
    diarization = pipeline(audio)

    #Format Json
    diarization_results = []
    for segment, _, speaker in diarization.itertracks(yield_label=True):
        diarization_results.append({
            "start": segment.start,
            "end": segment.end,
            "speaker": speaker
        })

    # dump the diarization output to disk using JSON format
    with open(output, "w") as json_file:
        json.dump(diarization_results, json_file, indent=4)

    with ProgressHook() as hook:
        diarization = pipeline(audio, hook=hook)

if __name__ == "__main__":
    audio_file = "./audioTest.mp3"
    if not os.path.exists(audio_file):
        raise FileNotFoundError(f"Audio file not found: {audio_file}")

    diarize(audio_file, "./diarization.json")