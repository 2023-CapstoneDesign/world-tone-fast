from pydub import AudioSegment

def sync(file_name, target_duration):
    # 원래 음성
    audio = AudioSegment.from_wav(file_name + ".wav")
    current_duration = len(audio)
    
    if current_duration > target_duration:
        # 현재 길이가 목표 길이보다 길 경우 속도 up
        speeded_audio = audio.speedup(
            playback_speed=current_duration / target_duration
        )
        # final_audio = speeded_audio[:target_duration]
        final_audio = speeded_audio

    else:
        # 현재 길이가 목표 길이보다 짧을 경우 target_duration만큼 공백음 생성
        final_audio = audio + AudioSegment.silent(
            duration=target_duration - current_duration
        )

    # 결과를 파일로 저장
    final_audio.export("final_audio.wav", format="wav")
    return len(final_audio)

if __name__ == "__main__":
    file_name = "original"  # 원본 오디오 파일 경로
    target_duration = 60000  # 목표 길이(밀리초 단위)

    result = sync(file_name, target_duration)
    print(f"Final audio duration: {result} milliseconds")