from pathlib import Path
from openai import OpenAI
client = OpenAI(api_key="")

speech_file_path = Path(__file__).parent / "alarmvoice.mp3"
response = client.audio.speech.create(
  model="tts-1",
  voice="echo",
  input="Help is on the way. Please hang on tight!"
)

response.stream_to_file(speech_file_path)