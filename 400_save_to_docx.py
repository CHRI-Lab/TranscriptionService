import os
import re
from docx import Document

TRANSCRIPT_DIR = "transcripts/Backup2"
OUTPUT_DIR = "docs"

def ensure_output_folder():
    """Creates the /docs folder if it doesn't exist."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def clean_line(line):
    """Removes timestamp from a single line."""
    return re.sub(r"\[\d{1,2}:\d{2}:\d{2} - \d{2}:\d{2}:\d{2}\]\s*", "", line).strip()

def convert_transcripts_to_docx():
    """Reads transcript files, removes timestamps, and saves as .docx with preserved paragraph breaks."""
    ensure_output_folder()

    for filename in os.listdir(TRANSCRIPT_DIR):
        if filename.endswith("_gpt.txt"):
            input_path = os.path.join(TRANSCRIPT_DIR, filename)
            output_path = os.path.join(OUTPUT_DIR, filename.replace("_gpt.txt", ".docx"))

            with open(input_path, "r", encoding="utf-8") as file:
                raw_text = file.read()

            # Split the transcript into blocks of text separated by multiple newlines
            blocks = re.split(r"\n\s*\n", raw_text.strip())
            
            doc = Document()
            for block in blocks:
                # Process each line within the block to remove timestamps
                lines = block.strip().splitlines()
                cleaned_lines = [clean_line(line) for line in lines if clean_line(line)]
                if cleaned_lines:
                    paragraph_text = " ".join(cleaned_lines)
                    doc.add_paragraph(paragraph_text)

            doc.save(output_path)
            print(f"Processed: {filename} → {output_path}")

if __name__ == "__main__":
    convert_transcripts_to_docx()
    print("All transcripts have been converted to .docx!")
