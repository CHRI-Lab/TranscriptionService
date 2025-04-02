import os
import subprocess

MAX_FILE_SIZE_MB = 25
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024  # Convert MB to bytes
TEMP_DIR = "temp"

def ensure_temp_folder():
    """Creates the /temp folder if it doesn't exist."""
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

def get_audio_duration(audio_file_path):
    """Returns the duration of the audio file using FFmpeg."""
    cmd = [
        "ffmpeg",
        "-i", audio_file_path,
        "-hide_banner",
        "-f", "null", "-"
    ]
    result = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)
    lines = result.stderr.split("\n")
    for line in lines:
        if "Duration" in line:
            time_str = line.split("Duration: ")[1].split(",")[0]
            h, m, s = map(float, time_str.replace(":", " ").split())
            return h * 3600 + m * 60 + s  # Convert to seconds
    return None

def estimate_max_duration(audio_file_path, total_duration):
    """Estimates max duration per chunk ensuring each chunk is ≤ 25MB."""
    file_size = os.path.getsize(audio_file_path)
    bytes_per_second = file_size / total_duration
    return MAX_FILE_SIZE_BYTES / bytes_per_second  # Calculate safe chunk duration

def split_audio_ffmpeg(audio_file_path, original_name):
    """Splits audio files into ≤ 25MB chunks using FFmpeg."""
    chunks = []
    total_duration = get_audio_duration(audio_file_path)
    if not total_duration:
        print(f"Skipping {audio_file_path}, unable to determine duration.")
        return []
    
    chunk_duration = estimate_max_duration(audio_file_path, total_duration)
    start_time = 0
    chunk_num = 1

    while start_time < total_duration:
        chunk_path = os.path.join(TEMP_DIR, f"{original_name}_chunk{chunk_num}.m4a")
        cmd = [
            "ffmpeg",
            "-i", audio_file_path,
            "-ss", str(start_time),
            "-t", str(chunk_duration),
            "-c", "copy",
            chunk_path
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        chunks.append(chunk_path)

        start_time += chunk_duration
        chunk_num += 1

    return chunks

def process_audio_files(input_directory):
    """Processes all .m4a files in the given directory."""
    ensure_temp_folder()

    for filename in os.listdir(input_directory):
        if filename.endswith(".m4a"):
            audio_file_path = os.path.join(input_directory, filename)
            original_name = os.path.splitext(filename)[0]
            print(f"Processing: {filename}")

            if os.path.getsize(audio_file_path) > MAX_FILE_SIZE_BYTES:
                split_audio_ffmpeg(audio_file_path, original_name)
            else:
                # Copy file to /temp as a single chunk
                temp_path = os.path.join(TEMP_DIR, f"{original_name}_chunk1.m4a")
                os.system(f"cp '{audio_file_path}' '{temp_path}'")  # Copy file
                print(f"Copied {filename} as single chunk.")

if __name__ == "__main__":
    input_directory = "Audio"  # Change this to your actual folder
    process_audio_files(input_directory)
    print("Audio splitting completed. Chunks saved in /temp.")
