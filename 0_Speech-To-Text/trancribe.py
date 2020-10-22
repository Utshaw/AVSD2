import io
import os

# Imports the Google Cloud client library
from google.cloud import speech




# Instantiates a client
client = speech.SpeechClient()

audio_folder="./audio"
audio_files=os.listdir(audio_folder)

text_dir = "./transcribed"

START_INDEX=0
END_INDEX=100

processed_audio_count=0
total_audio_count=len(audio_files)

config = speech.RecognitionConfig(
        # encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        encoding = speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
        sample_rate_hertz=16000,
        language_code="bn-BD",
    )

for audio in audio_files[START_INDEX:END_INDEX]:
    # The name of the audio file to transcribe
    
    fileBaseName = audio
    file_name = os.path.join(os.path.dirname(__file__), audio_folder,audio)
    utt_id=audio.split('.')[0]

    # Loads the audio into memory
    with io.open(file_name, "rb") as audio_file:
        content = audio_file.read()
        audio = speech.RecognitionAudio(content=content)

    # Detects speech in the audio file
    response = client.recognize(request={"config": config, "audio": audio})
    processed_audio_count+=1
    transcript="<sos> "

    for result in response.results:

        transcript+=result.alternatives[0].transcript+" $ "

    with open(os.path.join(text_dir, os.path.splitext(fileBaseName)[0] + ".txt"),'a') as file:
        file.write(utt_id+" "+transcript+"\n")

    print("Processed  {}/{} files\nTranscript: {}".format(processed_audio_count,total_audio_count,transcript))

    
