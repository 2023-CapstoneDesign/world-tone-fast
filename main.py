from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from utils.script import Script
import uvicorn
import os
import uuid
import utils.tts as tts
import utils.googlecloud.googleTranslate as gt
import utils.aws.s3 as s3
import logging

app = FastAPI()

logger = logging.getLogger("uvicorn")

class ReqDto(BaseModel):
    group_key: uuid.UUID
    gender: str
    saved_key: uuid.UUID
    target_language: str
    scripts: List[Script]

@app.post("/endpoint")
async def endpoint(dto: ReqDto):

    ## Translate scripts
    translated_texts = gt.google_translate(
        list(map(lambda script: script.text, dto.scripts)),
        dto.target_language)
    for script, translated_text in zip(dto.scripts, translated_texts):
        script.text = translated_text

    ## Get source file from S3 by group_key
    logger.info(str(dto.group_key))
    await s3.download(str(dto.group_key))

    ## Enhance ref audio file

    ## Create TTS file from translated scripts
    src_file = tts.tts_create(dto.scripts, dto.gender, dto.target_language, str(dto.saved_key))
    logger.info(src_file)

    ## TODO: Apply VC model to TTS file

    ## TODO: Upload TTS file to S3
    object_key = await s3.upload(src_file, str(dto.saved_key))

    ## Delete TTS file and target voice file from local
    if os.path.exists("/tmp/tts/" + str(dto.saved_key) + ".wav"):
        os.remove("/tmp/tts/" + str(dto.saved_key) + ".wav")
    if os.path.exists("/tmp/voice/" + str(dto.group_key) + ".wav"):
        os.remove("/tmp/voice/" + str(dto.group_key) + ".wav")

    ## Return s3_saved_key
    return {"created": object_key}

if __name__ == '__main__':
    uvicorn.run(app="main:app", reload=True)
