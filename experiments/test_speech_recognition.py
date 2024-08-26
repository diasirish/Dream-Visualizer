import whisper

model = whisper.load_model("medium")
# result = model.transcribe("audio_files/test_3.m4a", task='translate')
result = model.transcribe("user_voice.ogg", task='translate')
print(result["text"])