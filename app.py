from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from utils.script import Script

import uuid


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

    print("scripts:")
    for script in dto.scripts:
        print("----")
        print(f"script: {script}")
        print(f"duration: {script.duration()}")

    ## TODO: Get source file from S3 by group_key

    ## TODO: Translate scripts

    ## TODO: Create TTS file from translated scripts

    ## TODO: Apply VC model to TTS file

    ## TODO: Upload TTS file to S3

    ## TODO: Return s3_saved_key
    s3_saved_key = uuid.uuid4()
    return {"s3_saved_key": s3_saved_key}
