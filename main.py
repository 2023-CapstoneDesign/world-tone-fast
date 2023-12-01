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
import utils.audio as audio
import model.deepfilternet as df
import model.knnvc as vc
import utils.file as file

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
    ref_file_name = audio.combine_files("tmp/"+str(dto.group_key)+"/aws/"+str(dto.group_key), str(dto.group_key))
    ref_file_name = await df.enhance_ref_voice(ref_file_name, str(dto.group_key))

    ## Create TTS file from translated scripts
    src_file_name = tts.tts_create(dto.scripts, dto.gender, dto.target_language, str(dto.saved_key), str(dto.group_key))
    logger.info(src_file_name)

    ## TODO: Apply VC model to TTS file
    out_file_name = await vc.voice_conversion(ref_file_name, src_file_name, str(dto.saved_key), str(dto.group_key))

    logger.info(out_file_name)
    ## TODO: Upload TTS file to S3
    object_key = await s3.upload(out_file_name, str(dto.saved_key))

    ## Delete TTS file and target voice file from local
    file.delete_files_in_folder("tmp/"+str(dto.group_key))
    if os.path.exists("tmp/tts/" + str(dto.saved_key) + ".wav"):
        os.remove("tmp/tts/" + str(dto.saved_key) + ".wav")
    if os.path.exists("tmp/voice/" + str(dto.group_key) + ".wav"):
        os.remove("tmp/voice/" + str(dto.group_key) + ".wav")

    ## Return s3_saved_key
    return {"created": object_key}

if __name__ == '__main__':
    uvicorn.run(app="main:app", reload=True)
