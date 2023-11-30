from df.enhance import enhance, init_df, load_audio, save_audio
from df.utils import download_file
import uvicorn
import os
from fastapi import FastAPI

app = FastAPI()

if __name__ == '__main__':
    try:
        # Load default model
        model, df_state, _ = init_df()
        
        # Download and open some audio file. You use your audio files here
        audio_path = os.path.join("tmp", "content/ref.wav")
        
        # Check if the file exists
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        # Load audio
        audio, _ = load_audio(audio_path, sr=df_state.sr())
        
        # Denoise the audio
        enhanced = enhance(model, df_state, audio)
        
        # Save for listening
        save_audio("/tmp/content/ref_enhanced.wav", enhanced, df_state.sr())
        print("Enhancement complete. Output saved as ref_enhanced.wav")
        
        uvicorn.run(app='main:app', reload=True)
        
    except Exception as e:
        print(f"An error occurred: {e}")