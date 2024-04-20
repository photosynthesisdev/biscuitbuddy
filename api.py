from fastapi import FastAPI, File, UploadFile, HTTPException, Request, Response, Cookie
from typing import Optional
from fastapi.responses import JSONResponse, FileResponse
from pathlib import Path
from openai import OpenAI
import logging
import os
import json
import time

app = FastAPI()
client = OpenAI(api_key='sk-proj-2JApfwSe6dwXMs43DwJTT3BlbkFJLxxgb9OaFFmQjCBXi0bW')

logging.basicConfig(level=logging.DEBUG)

@app.get("/whoami")
def whoami(request: Request, response: Response):
    conversation_id = int(time.time())
    response.set_cookie(key='conversation_id', value=str(conversation_id))
    file_path = f"conversations/{conversation_id}.json"
    with open(file_path, "w") as file:
        data = [
            {"role": "system", "content": "You are a friendly critter named Biscuit. You live in the wild and talk to those that wish to speak to you. Be friendly and cordial."}
        ]
        json.dump(data, file, indent=4)
    return {"conversation_id": conversation_id}

@app.post("/upload/")
async def upload(audio_file: UploadFile, conversation_id: Optional[str] = Cookie(default=None)):
    def get_biscuit_response(audio_file_path):
        nonlocal conversation_list
        with open(audio_file_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
            user_question = transcription.text
            conversation_list.append(
                {"role": "user", "content": user_question}
            )
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=conversation_list
            )
            biscuit_response = completion.choices[0].message.content
            conversation_list.append(
                {"role": "assistant", "content": biscuit_response}
            )
            return biscuit_response
    if conversation_id == None:
        return "No conversation started."
    file_path = f"conversations/{conversation_id}.json"
    with open(file_path, "r") as file:
        data = file.read()
        conversation_list = json.loads(data)
        logging.error(conversation_list)
    safe_name = audio_file.filename.split('/')[-1].split('\\')[-1]
    file_location = f"./uploads/{safe_name}"
    os.makedirs(os.path.dirname(file_location), exist_ok=True)
    try:
        with open(file_location, "wb") as file_object:
            file_object.write(await audio_file.read())
        audio_file.file.close()
        # Here you call your function to process the audio file
        response = get_biscuit_response(file_location)
        with open(file_path, "w") as file:
            json.dump(conversation_list, file, indent=4)
        return JSONResponse(status_code=200, content={"response": response})
    except Exception as e:
        os.remove(file_location)  # Cleanup if something goes wrong
        logging.error(e)
        return JSONResponse(status_code=500, content={"message": str(e)})


@app.get("/runner")
def runner():
    return FileResponse('index.html')