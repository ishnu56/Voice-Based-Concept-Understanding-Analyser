import whisper
import os

model = whisper.load_model("base")

def transcribe_audio(audio_input):

    print("audio_input =", audio_input)
    print("type =", type(audio_input))

    if isinstance(audio_input, str):
        result = model.transcribe(audio_input)
        return result["text"]

    import tempfile

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(audio_input.read())
        temp_audio_path = temp_audio.name

    result = model.transcribe(temp_audio_path)
    os.remove(temp_audio_path)

    return result["text"]