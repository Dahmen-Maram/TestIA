from fastapi import FastAPI, UploadFile, File
import whisper
from pydub import AudioSegment
import os
import uuid

app = FastAPI()
model = whisper.load_model("medium")


def convert_to_wav(file_path):
    if file_path.endswith(".m4a"):
        audio = AudioSegment.from_file(file_path, format="m4a")
        wav_path = file_path.replace(".m4a", ".wav")
        audio.export(wav_path, format="wav")
        return wav_path
    return file_path

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    file_ext = file.filename.split(".")[-1]
    temp_filename = f"temp_{uuid.uuid4()}.{file_ext}"

    with open(temp_filename, "wb") as f:
        f.write(await file.read())

    wav_file = convert_to_wav(temp_filename)
    result = model.transcribe(wav_file, language="fr", fp16=False)
    os.remove(temp_filename)
    if wav_file != temp_filename and os.path.exists(wav_file):
        os.remove(wav_file)

    return {"transcription": result["text"]}
