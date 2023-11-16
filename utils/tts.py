from pydub import AudioSegment

from utils.googleTexttospeech import generate_tts
from utils.script import Script


def tts_create(scripts, lang):

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
            result_audio_seg = result_audio_seg + AudioSegment.silent(duration=scripts[i].duration_other(scripts[i+1]))

    result_audio_seg.export("스티브잡스연설.wav", format="wav")




def get_sync_speed(audio_seg, target_duration):
    current_duration = len(audio_seg)

    if current_duration > target_duration:
        return [1, current_duration / target_duration]
    else:
        return [0, target_duration - current_duration]

        ## Or return speed down ratio
        # return [0, target_duration / current_duration]


