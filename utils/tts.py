from gtts import gTTS

def get(self):
    text = "좀 더 크게 말해줘"

    tts = gTTS(text=text, lang="ko")
    tts.save("helloKO.mp3")
    return "SUCCESS"
