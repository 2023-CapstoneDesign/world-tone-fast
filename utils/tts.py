from pydub import AudioSegment

from utils.googlecloud.googleTexttospeech import generate_tts
from utils.script import Script

## 싱크에 맞춘 TTS 생성
def tts_create(scripts: list(Script), lang: str, file_name: str):
    result_audio_seg = AudioSegment.empty()

    for i in range(len(scripts)):
        cs_audio_seg = generate_tts(scripts[i].text, lang)
        result = get_sync_speed(cs_audio_seg, scripts[i].duration_self())
        if result[0] == 1:
            cs_audio_seg = generate_tts(scripts[i].text, lang, result[1])
        else:
            cs_audio_seg = cs_audio_seg + AudioSegment.silent(duration=result[1])
        result_audio_seg = result_audio_seg + cs_audio_seg
        if scripts[i] != scripts[-1]:
            result_audio_seg = result_audio_seg + AudioSegment.silent(
                duration=scripts[i].duration_other(scripts[i+1]))
    result_audio_seg.export("/temp/tts/" + file_name + ".wav", format="wav")

## 싱크를 맞추기 위한 속도 계산
def get_sync_speed(audio_seg: AudioSegment, target_duration: int) -> list:
    current_duration = len(audio_seg)
    if current_duration > target_duration:
        return [1, current_duration / target_duration]
    else:
        return [0, target_duration - current_duration]
