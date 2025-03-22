from pydub import AudioSegment
import os

def split_audio(audio):
    chunk_length_ms = 10000  # pydub calculates in millisec
    chunks = []

    # Ensure the chunks directory exists
    if not os.path.exists("./app/chunks"):
        os.makedirs("./app/chunks")
    else:
        # Clear the directory if it already exists
        for file in os.listdir("./app/chunks"):
            os.remove(f"./app/chunks/{file}")

    for i in range(0, len(audio), chunk_length_ms):
        chunk = audio[i:i + chunk_length_ms]
        chunks.append(chunk)
        chunk.export(f"./app/chunks/chunk{i // chunk_length_ms}.mp3", format="mp3")
    return chunks

print("Current working directory:", os.getcwd())

if __name__ == "__main__":
    audio_file = "./app/audioTest.mp3"
    if not os.path.exists(audio_file):
        raise FileNotFoundError(f"Audio file not found: {audio_file}")

    print(split_audio(AudioSegment.from_file(audio_file)))