from df.enhance import enhance, init_df, load_audio, save_audio
from df.utils import download_file
import os
import torch, torchaudio

# Load default model
model, df_state, _ = init_df()
        
# Download and open some audio file. You use your audio files here
audio_path = "tmp/content/ref.wav"
print("1")
# Check if the file exists
if not os.path.exists(audio_path):
    raise FileNotFoundError(f"Audio file not found: {audio_path}")
info = torchaudio.info(audio_path)
print(info.sample_rate)
print("2")
# Load audio
audio, _ = load_audio(audio_path, sr=df_state.sr())
print(df_state.sr())
print("3")
# Check if the audio needs resampling
# if audio.shape[1] != df_state.sr():
#     resample = torchaudio.transforms.Resample(audio.shape[1], df_state.sr(), resampling_method='sinc_interp_hann')
#     audio = resample(audio)
print("4")

# Denoise the audio
enhanced = enhance(model, df_state, audio)
print("5")

output_path = "tmp/content/ref_enhanced.wav"
print("6")

# Ensure the directory exists
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Save for listening
save_audio(output_path, enhanced, df_state.sr())
print("Enhancement complete. Output saved as ref_enhanced.wav")