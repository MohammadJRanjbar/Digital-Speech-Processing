from hezar.models import Model
import pyaudio
import wave
from openai import OpenAI
import re
import os
import json
OPENAI_API_KEY="YOUR_OPENAI_KEY"


# Dictionary to store conversation history for each user
conversation_history = {}
def process_line(line):
    if re.match(r'^User:', line):
        return {"role": "user", "content": line.split(':')[1].strip()}
    elif re.match(r'^assistant:', line):
        return {"role": "assistant", "content": line.split(':')[1].strip()}

def read_file(filename):
    messages = []
    messages.append({"role": "system", "content": "You are a helpful assistant."})
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            message = process_line(line)
            if message:
                messages.append(message)
    return messages
def get_password(username):
    # Retrieve password from the user database
    return user_database.get(username)

def save_conversation_to_file(username, conversation):
    filename = f"{username}_conversation.txt"
    with open(filename, "a", encoding="utf-8") as file:
        for line in conversation:
            file.write(line + "\n")

def load_conversation_from_file(username):
    filename = f"{username}_conversation.txt"
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.readlines()
    except FileNotFoundError:
        return []

def authenticate_user():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    stored_password = get_password(username)
    if stored_password == password:
        print("Authentication successful!")
        return username,False
    else:
        print("Incorrect username or password.")
        return username,True

def transcriber(audio):
    audio_file= open(audio, "rb")
    client = OpenAI(api_key=OPENAI_API_KEY)
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file
    )
    print(transcription.text)
    return transcription.text

def response_generator(text,messages):
    client = OpenAI(api_key=OPENAI_API_KEY)
    messages.append({"role": "user", "content":text})

    response = client.chat.completions.create(
    model = "gpt-3.5-turbo-0125",
    temperature = 0.8,
    max_tokens = 3000,
    messages = messages
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



if os.path.exists('user_database.json'):
    # Read the existing JSON file
    with open('user_database.json', 'r') as file:
        user_database = json.load(file)
else:
    # If the file does not exist, create an empty dictionary
    user_database = {}

    # Save the empty dictionary as a JSON file
    with open('user_database.json', 'w') as file:
        json.dump(user_database, file)



def save_conversation(filename, conversation):
    with open(filename, 'a', encoding='utf-8') as file:
        for message in conversation:
            file.write(message + '\n')
while True:
    audio = input("Do you have an account:Y/N/Q ")
    if audio.lower() == "n":
        print("Make an account")
        username = input("Enter a username: ")
        while username in user_database:
            print("Username already exists. Please choose another one.")
            username = input("Enter a different username: ")
        password = input("Enter a password: ")
        user_database[username] = password
        with open('user_database.json', 'w') as file:
            json.dump(user_database, file)
        print("Account created successfully!")
        print("You can now log in.")
    elif audio.lower() == "y":
        check=True
        while(check):
            username,check=authenticate_user()
            if(check):
                print("If you do not have an account, you need to restart the program.")
            pass
        while True:
            audio = input("Press 'r' to record a new audio or 'q' to quit: ")
            if audio.lower() == "q":
                break
            elif audio.lower() == "r":
                audio_file = record_audio()
                if os.path.exists(f"{username}_conversation.txt"):
                    conversations=read_file(f"{username}_conversation.txt")
                else:    
                    messages = []
                    conversations=[{"role": "system", "content": "You are a helpful assistant."}]
                text = transcriber(audio_file)
                response = response_generator(text,conversations)
                conversations.append("User: " + text)
                conversations.append("assistant: " + response)
                save_conversation(f"{username}_conversation.txt", ["User: " + text, "assistant: " + response])
            else:
                print("Invalid input!")
    elif audio.lower() == "q":
        print("Bye!")
        break
    else:
        print("Invalid input!")



