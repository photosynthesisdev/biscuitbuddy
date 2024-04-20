from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import JSONResponse, FileResponse
from pathlib import Path
from openai import OpenAI
import logging
import os

app = FastAPI()
client = OpenAI()

logging.basicConfig(level=logging.DEBUG)

def safe_filename(filename):
    """Generate a safe filename from the original by stripping directory paths."""
    return Path(filename).name

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from openai import OpenAI
import os

app = FastAPI()
client = OpenAI()

def safe_filename(filename):
    """Generate a safe filename from the original by stripping directory paths."""
    return filename.split('/')[-1].split('\\')[-1]

@app.post("/upload/")
async def upload(audio_file: UploadFile):
    if not audio_file.filename.lower().endswith(('.wav', '.mp3')):
        raise HTTPException(status_code=400, detail="Unsupported file type.")
    safe_name = safe_filename(audio_file.filename)
    file_location = f"./uploads/{safe_name}"
    os.makedirs(os.path.dirname(file_location), exist_ok=True)
    try:
        with open(file_location, "wb") as file_object:
            file_object.write(await audio_file.read())
        audio_file.file.close()

        # Here you call your function to process the audio file
        response = get_biscuit_response(file_location)

        return JSONResponse(status_code=200, content={"response": response})
    except Exception as e:
        os.remove(file_location)  # Cleanup if something goes wrong
        return JSONResponse(status_code=500, content={"message": str(e)})

def get_biscuit_response(audio_file_path):
    with open(audio_file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a friendly critter named Biscuit. You live in the wild and talk to those that wish to speak to you. Be friendly and cordial."},
                {"role": "user", "content": transcription.text},
            ]
        )
        return completion.choices[0].message.content
    

@app.get("/")
def read_root():
    return FileResponse('index.html')