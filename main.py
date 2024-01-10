from openai import OpenAI
import openai
import os

MAX_TRANSCRIPTION_FILESIZE = 26214400

def get_key():
    with open(".apikey") as f:
        return f.read()

def write_output(transcription, input_filename):
    output_filename = "transcribed_" + input_filename.replace(" ", "_")
    with open("./output/" + output_filename, "w") as f:
        f.write(transcription)

def transcribe_file(client, audio_filename):
    audio_file = open("data/" + audio_filename, "rb")
    transcript = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
    )
    return transcript.text


if __name__ == '__main__': 
    client = OpenAI(api_key=get_key())

    input_filenames = os.listdir("./data")
    for input_filename in input_filenames: 
        print("Working on file: " + input_filename)
        filesize = os.stat("./data/" + input_filename).st_size
        if filesize > MAX_TRANSCRIPTION_FILESIZE:
            continue
        
        try:
            transcription = transcribe_file(client, input_filename)
            write_output(transcription, input_filename)
        except openai.APIStatusError as e:
            print("Unable to transcribe file: " + input_filename)
            print(e)
            print("-" * 50)