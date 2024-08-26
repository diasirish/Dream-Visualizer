from pydub import AudioSegment

# Load the .ogg file
audio = AudioSegment.from_ogg("user_voice.ogg")

# Export the file as .m4a (mp4 audio)
audio.export("output_file.m4a", format="mp4")

print("Conversion completed: 'input_file.ogg' to 'output_file.m4a'")