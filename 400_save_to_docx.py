import os
import re
from docx import Document

TRANSCRIPT_DIR = "transcripts"
OUTPUT_DIR = "docs"

def ensure_output_folder():
    """Creates the /docs folder if it doesn't exist."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def clean_transcript(text):
    """Removes timestamps from transcript text."""
    return re.sub(r"\[\d+\.\d+ - \d+\.\d+\] ", "", text)

def convert_transcripts_to_docx():
    """Reads transcript files, removes timestamps, and saves as .docx."""
    ensure_output_folder()
    
    for filename in os.listdir(TRANSCRIPT_DIR):
        if filename.endswith("_gpt.txt"):  # Ensure we're only processing transcript files
            input_path = os.path.join(TRANSCRIPT_DIR, filename)
            output_path = os.path.join(OUTPUT_DIR, filename.replace("_gpt.txt", ".docx"))
            
            with open(input_path, "r", encoding="utf-8") as file:
                raw_text = file.read()
                cleaned_text = clean_transcript(raw_text)
            
            doc = Document()
            doc.add_paragraph(cleaned_text)
            doc.save(output_path)
            print(f"Processed: {filename} → {output_path}")

if __name__ == "__main__":
    convert_transcripts_to_docx()
    print("All transcripts have been converted to .docx!")
