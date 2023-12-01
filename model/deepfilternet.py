from df.enhance import enhance, init_df, load_audio, save_audio
from df.utils import download_file
import os

async def enhance_ref_voice(file_name: str, group_key: str):
    # Load default model
    model, df_state, _ = init_df()
    # Download and open some audio file. You use your audio files here
    audio_path = file_name # ref audio file
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
    audio, _ = load_audio(audio_path, sr=df_state.sr())
    # Denoise the audio
    enhanced = enhance(model, df_state, audio)

    output_path = "tmp/"+group_key+"/content/ref_enhanced.wav"
    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Save for listening
    save_audio(output_path, enhanced, df_state.sr())
    print("Enhancement complete. Output saved as ref_enhanced.wav")

    return output_path