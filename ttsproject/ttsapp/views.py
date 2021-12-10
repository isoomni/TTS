from django.shortcuts import render, redirect
from google.cloud import texttospeech
import os
from django.http import HttpResponse

import cv2 
import numpy as np 
import pyautogui 

from moviepy.editor import *

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:\\Users\\jjm\\Desktop\\tts\\ttsproject\\ttsapp\\texttospeech-290400-bba9ca830f43.json"

def main(request) :
    # list_voices()
    return render(request, 'ttsapp/main.html')


def tts_converter(request) :
    body = request.POST['body']
    no_speak_body = body
    body = '<speak>' + body + '</speak>'
    
    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(ssml=body)

    voice = texttospeech.VoiceSelectionParams(
        # language_code="en-US", 
        language_code="ko-KR", 
        name='ko-KR-Standard-C',
        ssml_gender=texttospeech.SsmlVoiceGender.MALE
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )

    is_audio = False

    with open("ttsapp/static/ttsapp/output.mp3", "wb") as out:
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')
        is_audio = True

    content = {
        'body': no_speak_body,
        'audio' : is_audio
    }

    return render(request, 'ttsapp/main.html', content)

def recode(request) :
    if request.method == "POST" :
        screen_size = (1800, 800)
        # pyautogui.size () 
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        out=cv2.VideoWriter("ttsapp/static/ttsapp/recode.avi",fourcc, 13, (screen_size))

        cv2.namedWindow("Live", cv2.WINDOW_NORMAL) 
        cv2.resizeWindow("Live", 1, 1) 
        
        while True: 
            img = pyautogui.screenshot(region=(0, 200, 1800, 800))  
            frame = np.array(img) 
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
            out.write(frame) 
            cv2.imshow("Live", frame) 
            if cv2.waitKey(1) == 27: 
                break
        
        # Release the Video writer 
        out.release() 
        
        # Destroy all windows 
        cv2.destroyAllWindows()

    return render(request, 'ttsapp/main.html')

def merge(request) :
    if request.method == "POST" :
        videoclip = VideoFileClip("ttsapp/static/ttsapp/recode.avi")
        audioclip = AudioFileClip("ttsapp/static/ttsapp/output.mp3")
        new_audioclip = CompositeAudioClip([audioclip])
        videoclip.audio = new_audioclip
        videoclip.write_videofile("ttsapp/static/ttsapp/result.mp4")

    return render(request, 'ttsapp/main.html')


# def list_voices():
#     client = texttospeech.TextToSpeechClient()

#     # Performs the list voices request
#     voices = client.list_voices()

#     for voice in voices.voices:
#         # Display the voice's name. Example: tpc-vocoded
#         print(f"Name: {voice.name}")

#         # Display the supported language codes for this voice. Example: "en-US"
#         for language_code in voice.language_codes:
#             print(f"Supported language: {language_code}")

#         ssml_gender = texttospeech.SsmlVoiceGender(voice.ssml_gender)

#         # Display the SSML Voice Gender
#         print(f"SSML Voice Gender: {ssml_gender.name}")

#         # Display the natural sample rate hertz for this voice. Example: 24000
#         print(f"Natural Sample Rate Hertz: {voice.natural_sample_rate_hertz}\n")