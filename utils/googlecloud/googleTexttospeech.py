from google.cloud import texttospeech
from pydub import AudioSegment

import os
import io

# Google Cloud 서비스를 사용하기 위한 인증 정보
credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_PATH")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

## text와 language_code를 받아서 tts를 생성하고 AudioSegment를 반환
def generate_tts(text, language_code, speaking_rate=1.0) -> AudioSegment:
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16,
        speaking_rate=speaking_rate,
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config,
    )

    audio_stream = io.BytesIO(response.audio_content)
    return AudioSegment.from_file(audio_stream, format="wav")
