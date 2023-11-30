from df.enhance import enhance, init_df, load_audio, save_audio
from df.utils import download_file

async def enhance_ref_voice(file_name: str):
    # Load default model
    model, df_state, _ = init_df()
    # Download and open some audio file. You use your audio files here
    audio_path = file_name # ref audio file
    audio, _ = load_audio(audio_path, sr=df_state.sr())
    # Denoise the audio
    enhanced = enhance(model, df_state, audio)
    # Save for listening
    save_audio("/tmp/content/ref_enhanced.wav", enhanced, df_state.sr())
    return "/tmp/content/ref_enhanced.wav"