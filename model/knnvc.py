import torch, torchaudio

async def voice_conversion(ref_file_name: str, source_file_name: str, save_file_name: str):

    if torch.cuda.is_available():
        device = torch.device("cuda")
    else:
        device = torch.device("cpu")

    knn_vc = torch.hub.load('bshall/knn-vc', 'knn_vc', prematched=True, trust_repo=True, pretrained=True, device=device)

    # path to 16kHz, single-channel, source waveform
    src_wav_path = source_file_name
    # list of paths to all reference waveforms (each must be 16kHz, single-channel) from the target speaker
    ref_wav_paths = [ref_file_name, ]

    query_seq = knn_vc.get_features(src_wav_path)
    matching_set = knn_vc.get_matching_set(ref_wav_paths)

    out_wav = knn_vc.match(query_seq, matching_set, topk=4)

    torchaudio.save('/tmp/out/'+save_file_name+'.wav', out_wav[None], 16000)
    return '/tmp/out/'+save_file_name+'.wav'