# **Background**  

So, you finally decided to do an interview, record some audio, and now you're stuck waiting for transcription. Yeah, that sucks—I know it is a pain in the a**. But fear not! Yan (:insert_warrior_cat_imoji_here) created this transcriber tool to save you from hours of suffering. 

The basic idea? Just throw Whisper at it and let it do the work.  

---

## **Set Up This Mess**  

To keep things clean (and prevent your existing Python setup from turning into a dumpster fire), we’re using a **virtual environment**.  

If it’s your first time here, set up the virtual environment and install the dependencies:  

```bash
python3 -m venv transcriber
```  

### **Activate the Virtual Environment**  

Windows:  
```bash
transcriber\Scripts\activate
```  

MacOS/Linux:  
```bash
source transcriber/bin/activate
```  

### **Install the Required Packages**  
```bash
pip3 install -r requirements.txt
```  

Boom! You’re good to go.  

---

## **Project Folder Structure (a.k.a. How This Works)**  

Here’s the master plan:  
- If your audio file is **larger than 25MB**, we **chop it into chunks** (because Whisper doesn’t do big bites).  
- The **100_split_audio.py** script slices it up and saves the pieces in a `/temp` folder.  
- Then, **200_transcription_audio.py** picks up the chunks, transcribes them **one by one**, 
- Then, **300_merge_chunks.py** merges everything into a clean transcript.

### **How the Folder Should Look:**  
```
/your-project-folder
  ├── .env  
  ├── 100_split_audio.py            # Step 1: Slicing up the audio
  ├── 200_transcription_audio.py    # Step 2: Transcribing 
  ├── 300_merge_chunks.py           # Step 3: Merging
  ├── temp/                  # Temporary folder for audio chunks
  │    ├── audio1_chunk1.m4a
  │    ├── audio1_chunk2.m4a
  │    ├── audio2_chunk1.m4a
  │    ├── ...
  ├── transcripts/           # Final transcriptions
  │    ├── audio1_gpt.txt
  │    ├── audio2_gpt.txt
  │    ├── ...
  ├── Audio/           # Dump your audio files here
  │    ├── interview1.m4a
  │    ├── interview2.m4a
  │    ├── ...
```  


**Step 0:** Create a .env file and save the API key here in following format. Never upload the .env file to github
```
OPENAI_API_KEY= <KEY_HERE>
```

replace any content in checkpoint.json to 
```
{"processed_files": [], "last_file": "", "last_chunk": 0}
```
in the very first run


**Step 1:** Run `100_split_audio.py` to **cut** audio files into ≤25MB chunks.  

```
python3 100_split_audio.py
```

**Step 2:** Run `200_transcription_audio.py` to **transcribe** the each chunk and save to /temp folder.  
```
python3 200_transcription_audio.py
```

If the code encounters an exception, don't worry—temp files will be created as a backup, and the last checkpoint will be saved. This means you won't need to transcribe the entire audio file again. The script keeps track of the last successfully processed chunk and will restart from there.

Simply rerun the `transcribe_audio.py` script in case of a failure. Make sure that you do not delete the `checkpoint.json` file.


**Step 3:** Run `300_merge_chunks.py` to **merge** the chunks into a single transcript and fix timestamps.  
```
python3 300_merge_chunks.py
```

**Step 4:** Run `400_save_to_docx.py` to **export** the manually checked (double checked) transcript file to docx. So you can use it for thematic analysis (Sorry!! No scripts to this shitty step!!! Do it yourself)

```
python3 400_save_to_docx.py
```

**Step 5:** Send some cat gifs to Yan as a token of appreciation.