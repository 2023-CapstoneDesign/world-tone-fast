from pydub import AudioSegment
import torch, torchaudio
import os

print(1)
# print(f"MPS 장치를 지원하도록 build가 되었는가? {torch.backends.mps.is_built()}")
# print(f"MPS 장치가 사용 가능한가? {torch.backends.mps.is_available()}") 
# if torch.backends.mps.is_available():
#     print("success gpu")
#     device = torch.device("mps")
# else:
#     print("fail")
#     device = torch.device("cpu")
if torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch.device("cpu")
print(1)


# Audio segment
def split_audio(input_path, output_folder, segment_length=30):
    audio = AudioSegment.from_file(input_path)

    # Cut by 30s
    segments = [audio[i:i+segment_length*1000] for i in range(0, len(audio), segment_length*1000)]

    # Save as segment file
    for i, segment in enumerate(segments):
        segment.export(f"{output_folder}ref_{i+1}.wav", format="wav")

    return segments

input_audio_path = "tmp/ref2.wav"
folder_path = "tmp/segments/"
os.makedirs(os.path.dirname(folder_path), exist_ok=True)  # 디렉토리 생성
segments = split_audio(input_audio_path, folder_path)
print(1)

# Append reference list
ref_list = []
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path):
        ref_list.append(file_path)
print(1)


# path to 16kHz, single-channel, source waveform
src_wav_path = 'tmp/src2.wav'
if not os.path.exists(src_wav_path):
    raise FileNotFoundError(f"Audio file not found: {src_wav_path}")
# list of paths to all reference waveforms (each must be 16kHz, single-channel) from the target speaker
ref_wav_paths = ref_list
print(1)

knn_vc = torch.hub.load('bshall/knn-vc', 'knn_vc', prematched=True, trust_repo=True, pretrained=True, device=device)

query_seq = knn_vc.get_features(src_wav_path).float()
print(1)
matching_set = knn_vc.get_matching_set(ref_wav_paths).float()
print(1)
out_wav = knn_vc.match(query_seq, matching_set, topk=4)
print(2)
torchaudio.save('tmp/out.wav', out_wav[None], 16000)