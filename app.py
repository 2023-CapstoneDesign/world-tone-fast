from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from utils.script import Script

import os

import uuid
import utils.tts as tts
import utils.googlecloud.googleTranslate as gt

app = FastAPI()

class ReqDto(BaseModel):
    group_key: uuid.UUID
    saved_key: uuid.UUID
    target_language: str
    scripts: List[Script]

@app.post("/endpoint")
def endpoint(dto: ReqDto):

    ## Translate scripts
    translated_texts = gt.google_translate(
        list(map(lambda script: script.text, dto.scripts)),
        dto.target_language)
    for script, translated_text in zip(dto.scripts, translated_texts):
        script.text = translated_text

    ## TODO: Get source file from S3 by group_key

    ## Create TTS file from translated scripts
    tts.tts_create(dto.scripts, dto.target_language, dto.saved_key)

    ## TODO: Apply VC model to TTS file

    ## TODO: Upload TTS file to S3

    ## Delete TTS file and target voice file from local
    if os.path.exists("/temp/tts/" + dto.saved_key + ".wav"):
        os.remove("/temp/tts/" + dto.saved_key + ".wav")
    if os.path.exists("/temp/voice/" + dto.group_key + ".wav"):
        os.remove("/temp/voice/" + dto.group_key + ".wav")

    ## Return s3_saved_key
    return {"created": dto.saved_key}
