from hezar.models import Model
import pyaudio
import wave
from openai import OpenAI
OPENAI_API_KEY="YOUR_OPENAI_KEY"
def transcriber(audio):
    audio_file= open(audio, "rb")
    client = OpenAI(api_key=OPENAI_API_KEY)
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file
    )
    print(transcription.text)
    return transcription.text


def response_generator(text):
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
    model = "gpt-3.5-turbo-0125",
    temperature = 0.8,
    max_tokens = 3000,
    messages = [
        {"role": "system", "content": "You are a helpfull assistant"},
        {"role": "user", "content": text}
    ]
    )
    print(response.choices[0].message.content)
    return response.choices[0].message.content





def record_audio(filename="output.wav", seconds=3, fs=44100, chunk=1024, channels=2, sample_format=pyaudio.paInt16):
    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print('Recording')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames

    # Store data in chunks for specified duration
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream 
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    print('Finished recording')

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()
    return filename

conversation = []
while True:
    audio = input("Press 'r' to record a new audio or 'q' to quit: ")
    if audio.lower() == "q":
        break
    elif audio.lower() == "r":
        audio_file = record_audio(filename="output.wav", seconds=3, fs=44100, chunk=128, channels=2, sample_format=pyaudio.paInt16)
        text = transcriber(audio_file)
        response = response_generator(text)
        conversation.append("User: " + text)
        conversation.append("ChatBot: " + response)
    else:
        print("Invalid input!")

def save_conversation(filename, conversation):
    with open(filename, "w", encoding="utf-8") as file:
        for line in conversation:
            file.write(line + "\n")

save_conversation("conversation.txt", conversation)