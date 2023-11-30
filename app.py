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
import model.deepfilternet as df
import model.knnvc as vc
import utils.audio as audio

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

    ## Get source file from S3 by group_key
    s3.download(dto.group_key)

    ## Enhance ref audio file
    ref_file = audio.combine_files(dto.group_key, "/tmp/ref", "/tmp/content/ref_audio")
    ref_enhanced_file = df.enhance_ref_voice(ref_file)

    ## Create TTS file from translated scripts
    src_file = tts.tts_create(dto.scripts, dto.target_language, dto.saved_key)

    ## TODO: Apply VC model to TTS file
    result = vc.voice_conversion(ref_enhanced_file, src_file, dto.saved_key)

    ## TODO: Upload TTS file to S3
    object_key = s3.upload(result, dto.saved_key)

    ## Delete TTS file and target voice file from local
    if os.path.exists("/tmp/tts/" + dto.saved_key + ".wav"):
        os.remove("/tmp/tts/" + dto.saved_key + ".wav")
    if os.path.exists("/tmp/voice/" + dto.group_key + ".wav"):
        os.remove("/tmp/voice/" + dto.group_key + ".wav")

    ## Return s3_saved_key
    return {"created": object_key}

if __name__ == '__main__':
    uvicorn.run(app="main:app", reload=True)