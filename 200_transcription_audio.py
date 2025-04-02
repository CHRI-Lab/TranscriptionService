import os
import json
from openai import OpenAI
import traceback

client = OpenAI()  # Ensure OpenAI API is correctly set up

TEMP_DIR = "temp"
OUTPUT_DIR = "transcripts"
CHECKPOINT_FILE = "checkpoint.json"

def ensure_output_folder():
    """Creates the /transcripts folder if it doesn't exist."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def group_chunks():
    """Groups chunks based on their original filename."""
    audio_groups = {}
    for filename in sorted(os.listdir(TEMP_DIR)):  # Sort ensures order
        if filename.endswith(".m4a"):
            original_name = "_".join(filename.split("_")[:-1])  # Remove _chunkX
            if original_name not in audio_groups:
                audio_groups[original_name] = []
            audio_groups[original_name].append(os.path.join(TEMP_DIR, filename))
    return audio_groups

def transcribe_audio(file_path):
    """Transcribes an individual audio chunk."""
    with open(file_path, 'rb') as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="verbose_json",
            language="en",
            timestamp_granularities=["segment"]
        )
    return transcript

def save_transcription(transcript, output_path):
    """Saves the individual chunk transcription into a file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        for segment in transcript.segments:
            f.write(f"[{segment.start:.2f} - {segment.end:.2f}] {segment.text}\n")

def load_checkpoint():
    """Loads the last processed file from the checkpoint."""
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"processed_files": []}

def save_checkpoint(processed_files):
    """Saves the checkpoint, including the last processed file and chunk."""
    checkpoint_data = {
        "processed_files": processed_files
    }
    with open(CHECKPOINT_FILE, 'w', encoding='utf-8') as f:
        json.dump(checkpoint_data, f)


def process_chunks():
    """Processes all chunks from /temp and merges transcriptions, using checkpoints."""
    ensure_output_folder()
    grouped_chunks = group_chunks()
    checkpoint = load_checkpoint()
    processed_files = checkpoint["processed_files"]

    for original_name, chunks in grouped_chunks.items():
        print(f"All the audio files in {original_name} group is {chunks}")

        # Skip already processed files
        chunks = [chunk for chunk in chunks if chunk not in processed_files]
        print(f"To be processed audio files in {original_name} group is {chunks}")
    
        file_transcription_dir = os.path.join(TEMP_DIR, original_name, "transcriptions")
        if not os.path.exists(file_transcription_dir):
            os.makedirs(file_transcription_dir)

        # Continue from the last processed chunk for this file
        print(f"Transcribing: {original_name}")
        for i, chunk in enumerate(chunks):
            print(f"  → Processing chunk : {chunk}")
            try:
                transcript = transcribe_audio(chunk)
                chunk_transcript_path = os.path.join(file_transcription_dir, f"chunk_{i}.txt")
                save_transcription(transcript, chunk_transcript_path)
                print(f"  → Saved transcription for chunk {i}")

                # Save progress after processing each chunk
                processed_files.append(f"{chunk}")
                save_checkpoint(processed_files)

            except Exception:
                print(traceback.format_exc())
                # Save progress and exit on error
                save_checkpoint(processed_files)
                print("Progress saved. Please restart the process to continue.")
                return  # Exit after error

        # Once all chunks are processed, merge them into a full transcript
        save_checkpoint(processed_files)
        

if __name__ == "__main__":
    process_chunks()
    print("Transcription completed. Transcriptions saved as chunks in /temp.")
