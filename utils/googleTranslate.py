from google.cloud import translate

import os


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/dongbin/Documents/Google_Cloud/cellular-ring-399104-5f689ce94d19.json"

def google_translate(\
        texts=["Hello, world!"], \
        project_id="cellular-ring-399104", \
        source_language="ko-KR", \
        target_language="en-US"):

    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": texts,
            "mime_type": "text/plain",
            "source_language_code": source_language,
            "target_language_code": target_language,
        }
    )

    return [translation.translated_text for translation in response.translations]



print(google_translate(\
    texts=[\
        "안녕하세요. 여러분.",\
        "오늘은 파이썬을 배워봅시다.",\
        "파이썬은 재미있어요."],\
    source_language="ko-KR",\
    target_language="en-US"))

