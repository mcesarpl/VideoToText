import os
import wave, math, contextlib
import speech_recognition as sr
from moviepy.editor import AudioFileClip

transcribed_audio_file_name = "transcribed_speech.wav";
video_file_name="test_5.mp4";
timeSubdivision = 60;

def mp4ToWavConvert(inputFilePath, outPutPath):
    if not os.path.exists(outPutPath):
        print('Starting Conversion...');
        audioclip = AudioFileClip(inputFilePath)
        audioclip.write_audiofile(outPutPath)

def calcDuration(wavFilePath, time):
    with contextlib.closing(wave.open(wavFilePath, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames/ float(rate)
        total_duration = math.ceil(duration / time)
    return total_duration

def format_text(text):
    newphrase = text
    linelength = 188
    if len(text) > linelength:
        vector = text.split()
        newphrase = ''
        newLine = ''
        for i in range(0, len(vector)):
            newLine += vector[i] + ' '
            if len(newLine) >= linelength:
                newphrase += '\n' + newLine[:-1]
                newLine = ''
        if len(newLine) > 0:
            newphrase += '\n' + newLine[:-1]
    return newphrase

mp4ToWavConvert(video_file_name, transcribed_audio_file_name)
total_duration = calcDuration(transcribed_audio_file_name, timeSubdivision)

print('total durantion:')
print(str(total_duration*timeSubdivision) + 's')
print('total Subdivisions:')
print(str(total_duration))

print('recognizing...')
r = sr.Recognizer()
f = open("transcription.txt", "a")
for i in range(0, total_duration):
        with sr.AudioFile(transcribed_audio_file_name) as source:
            audio = r.record(source, offset=i*timeSubdivision, duration=timeSubdivision)
            """ text = r.recognize_google(audio, language='pt-BR') """
            text = r.recognize_google(audio, language='en-US')
            formated = format_text(text)
            print(str(i + 1) + " frase - ")
            print(text)
            f.write(str(i*timeSubdivision) + ' - ' + str(i*timeSubdivision + timeSubdivision) + 's'+ '\n')
            f.write(formated)
            f.write("\n\n")
f.close()
print('Transcription done!')