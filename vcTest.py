import torch, torchaudio
import os

print(1)
print(f"MPS 장치를 지원하도록 build가 되었는가? {torch.backends.mps.is_built()}")
print(f"MPS 장치가 사용 가능한가? {torch.backends.mps.is_available()}") 
if torch.backends.mps.is_available():
    print("success gpu")
    device = torch.device("mps")
else:
    print("fail")
    device = torch.device("cpu")
print(1)

# path to 16kHz, single-channel, source waveform
src_wav_path = 'tmp/src.wav'
if not os.path.exists(src_wav_path):
    raise FileNotFoundError(f"Audio file not found: {src_wav_path}")
# list of paths to all reference waveforms (each must be 16kHz, single-channel) from the target speaker
ref_wav_paths = ['tmp/ref.wav', ]
print(1)

knn_vc = torch.hub.load('bshall/knn-vc', 'knn_vc', prematched=True, trust_repo=True, pretrained=True, device=device)

query_seq = knn_vc.get_features(src_wav_path).float()
print(1)
matching_set = knn_vc.get_matching_set(ref_wav_paths).float()
print(1)
out_wav = knn_vc.match(query_seq, matching_set, topk=4)
print(1)
torchaudio.save('tmp/out.wav', out_wav[None], 16000)