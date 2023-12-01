import torch, torchaudio
from pydub import AudioSegment
import os

# Audio segment
def split_audio(input_path, output_folder, segment_length=30):
    audio = AudioSegment.from_file(input_path)

    # Cut by 30s
    segments = [audio[i:i+segment_length*1000] for i in range(0, len(audio), segment_length*1000)]

    # Save as segment file
    for i, segment in enumerate(segments):
        segment.export(f"{output_folder}ref_{i+1}.wav", format="wav")

    return segments


async def voice_conversion(ref_file_name: str, source_file_name: str, save_file_name: str, group_key: str):

    if torch.cuda.is_available():
        device = torch.device("cuda")
    else:
        device = torch.device("cpu")
    knn_vc = torch.hub.load('bshall/knn-vc', 'knn_vc', prematched=True, trust_repo=True, pretrained=True, device=device)

    folder_path = "tmp/segments/"
    os.makedirs(os.path.dirname(folder_path), exist_ok=True)  # 디렉토리 생성
    segments = split_audio(ref_file_name, folder_path)

    # Append reference list
    ref_list = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            ref_list.append(file_path)
    # path to 16kHz, single-channel, source waveform
    src_wav_path = source_file_name
    if not os.path.exists(src_wav_path):
        raise FileNotFoundError(f"Audio file not found: {src_wav_path}")
    # list of paths to all reference waveforms (each must be 16kHz, single-channel) from the target speaker
    ref_wav_paths = ref_list

    query_seq = knn_vc.get_features(src_wav_path)
    matching_set = knn_vc.get_matching_set(ref_wav_paths)

    out_wav = knn_vc.match(query_seq, matching_set, topk=4)
    local_file_path = "tmp/"+group_key+"/out/out"
    os.makedirs(os.path.dirname(local_file_path), exist_ok=True)  # 디렉토리 생성
    torchaudio.save(local_file_path+".wav", out_wav[None], 16000)
    return local_file_path+".wav"