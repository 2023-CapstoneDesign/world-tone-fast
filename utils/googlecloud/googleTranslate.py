from google.cloud import translate

import os


# Google Cloud 서비스를 사용하기 위한 인증 정보
credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_PATH")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

# Google Cloud 서비스를 사용하기 위한 프로젝트 ID
project_id = os.environ.get("GOOGLE_APPLICATION_PROJECT_ID")

## texts와 language_code를 받아서 번역된 texts를 반환
def google_translate(texts, target_language) -> list(str):
    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": texts,
            "mime_type": "text/plain",
            "target_language_code": target_language,
        }
    )

    return [translation.translated_text for translation in response.translations]
