from google.cloud import texttospeech
from pydub import AudioSegment

import os
import io

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/dongbin/Documents/Google_Cloud/cellular-ring-399104-5f689ce94d19.json"

def generate_tts(text, language_code='en-US', speaking_rate=1.0, pitch=0.0):

    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16,
        speaking_rate=speaking_rate,
        pitch=pitch
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    audio_stream = io.BytesIO(response.audio_content)
    return AudioSegment.from_file(audio_stream, format="wav")


def generate_tts_file(text, output_filename, language_code='en-US', speaking_rate=1.0, pitch=0.0):

    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=speaking_rate,
        pitch=pitch
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    # 응답된 오디오를 파일로 저장합니다.
    with open(output_filename, 'wb') as out:
        out.write(response.audio_content)
