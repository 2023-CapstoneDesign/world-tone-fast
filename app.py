from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from utils.script import Script

import uuid
import utils.googleTranslate as gt

app = FastAPI()

class ReqDto(BaseModel):
    group_key: uuid.UUID
    original_language: str
    target_language: str
    scripts: List[Script]

@app.post("/endpoint")
def endpoint(dto: ReqDto):
    print(f"s3 source voice group key: {dto.group_key}")
    print(f"original language: {dto.original_language}")
    print(f"target language: {dto.target_language}")

    print("\n==================\nscripts:")
    for script in dto.scripts:
        print("----")
        print(f"script: {script}")
        print(f"duration: {script.duration()}")

    ## Translate scripts
    # translated_texts = gt.google_translate( \
    #     texts= \
    #     list(map(lambda script: script.text, dto.scripts)), \
    #     source_language=dto.original_language, \
    #     target_language=dto.target_language)

    # for script, translated_text in zip(dto.scripts, translated_texts):
    #     script.text = translated_text

    ## 번역은 성공했으니, 우선 주석처리하고 시간에 맞춘 TTS 파일 생성부터 해보자

    print("\n==================\ntranslated scripts:")
    for script in dto.scripts:
        print("----")
        print(f"script: {script}")
        print(f"duration: {script.duration()}")

    ## TODO: Get source file from S3 by group_key

    ## TODO: Create TTS file from translated scripts

    ## TODO: Apply VC model to TTS file

    ## TODO: Upload TTS file to S3

    ## TODO: Return s3_saved_key
    s3_saved_key = uuid.uuid4()
    return {"s3_saved_key": s3_saved_key}
