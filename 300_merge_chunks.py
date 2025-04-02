import os
import json

TEMP_DIR = "temp"
OUTPUT_DIR = "transcripts"

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


def merge_full_transcript(original_name):
    """Merges all chunk text files into a single full transcript."""
    file_transcription_dir = os.path.join(TEMP_DIR, original_name, "transcriptions")
    full_transcript = []
    

    cumulative_end_time = 0.0  # Track the cumulative end time for timestamps
    
    # Iterate over all chunk text files and merge them
    for filename in sorted(os.listdir(file_transcription_dir)):
        if filename.endswith(".txt"):
            chunk_path = os.path.join(file_transcription_dir, filename)
            with open(chunk_path, 'r', encoding='utf-8') as f:
                for line in f:
                    # Extract the start and end timestamps from each segment
                    timestamp_part = line.split("]")[0][1:]  # Extract time range like [0.00 - 10.00]
                    start_time, end_time = map(float, timestamp_part.split(" - "))
                    
                    # Adjust the timestamps based on the cumulative end time
                    adjusted_start_time = start_time + cumulative_end_time
                    adjusted_end_time = end_time + cumulative_end_time
                    
                    # Update the line with adjusted timestamps
                    full_transcript.append(f"[{adjusted_start_time:.2f} - {adjusted_end_time:.2f}] {line.split(']')[1]}")
            
            # Update the cumulative end time based on the last segment's end time
            cumulative_end_time = adjusted_end_time  # Update with the latest chunk's end time


    # Save the merged transcript in the /transcripts folder
    output_file_path = os.path.join(OUTPUT_DIR, f"{original_name}_gpt.txt")
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.writelines(full_transcript)

    print(f"Saved full transcript for {original_name} at {output_file_path}")


if __name__ == "__main__":

    """Processes all chunks and merges transcriptions, using checkpoints."""
    grouped_chunks = group_chunks()
    for original_name, chunks in grouped_chunks.items():
        print(f"Processing chunks for {original_name}")

        merge_full_transcript(original_name)


    print("Merging completed. Files saved in /transcripts.")
