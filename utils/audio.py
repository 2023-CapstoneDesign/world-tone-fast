from pydub import AudioSegment
import os

def convert_webm_to_wav(input_folder: str, output_folder: str):
    # Make sure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.endswith(".webm"):
            # Load the WebM file
            webm_file = os.path.join(input_folder, filename)
            audio = AudioSegment.from_file(webm_file, format="webm")

            # Convert to WAV
            wav_filename = os.path.splitext(filename)[0] + ".wav"
            wav_file = os.path.join(output_folder, wav_filename)
            audio.export(wav_file, format="wav")

def concatenate_wav_files(input_folder: str, output_file: str):
    # Make sure the input folder exists
    os.makedirs(input_folder, exist_ok=True)

    # List all WAV files in the input folder
    wav_files = [f for f in os.listdir(input_folder) if f.endswith(".wav")]

    # Concatenate WAV files
    combined_audio = AudioSegment.silent()
    for wav_file in wav_files:
        file_path = os.path.join(input_folder, wav_file)
        segment = AudioSegment.from_file(file_path, format="wav")
        combined_audio += segment

    # Export the combined audio to a single WAV file
    combined_audio.export(output_file, format="wav")
    return output_file

def combine_files(input_folder: str, output_folder: str, output_file: str):
    # Convert WebM to WAV
    convert_webm_to_wav(input_folder, output_folder)

    # Concatenate WAV files
    return concatenate_wav_files(output_folder, output_file)