#!/usr/bin/env python3

# It is start of J-Robot.
# J-Robot uses aiy.assistant.grpc and answers your questions.
# Also, J-robot can do works that you defines.

import threading
import logging
import aiy.assistant.grpc
import aiy.audio
import aiy.voicehat
import subprocess

import vision.camera as cam
from serial_comm import SerialComm as serial_comm
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
)

'''
You can set local_commands
input - text
output - isAnswer, answer
'''
def local_commands(text):
    isAnswer = True
    answer = ''
    if text:
        if text =='사진 찍어 줘':
            answer = '알겠습니다. 하나 둘 셋'
            textToSpeech(answer)
            image = cam.capture()
            cam.save_image(image,'/home/pi/image.jpg')
            textToSpeech('찍었습니다.')
        elif text =='불 켜 줘':
            answer = '알겠습니다.'
            textToSpeech(answer)
        elif text =='불 꺼 줘':
            answer = '알겠습니다.'
            textToSpeech(answer)
        elif 'IP' in text or 'ip' in text :
            answer = 'IP는 '
            answer += str(subprocess.check_output("hostname -I", shell=True))
            answer = answer.replace('n','')
            answer = answer.replace('b','')
            textToSpeech(answer)
            # print(answer)
        else:
            isAnswer = False
    else:
        isAnswer = False
    return isAnswer, answer




'''
this function is text to speech
lang is language
sox_effects is options.
'''
from google_speech import Speech
def textToSpeech(text):
    lang = "ko_KR"
    speech = Speech(text, lang)
    sox_effects = ("speed", "1.0")
    sox_effects = ("vol", "0.05")
    speech.play(sox_effects)
    



def main():
    
    sc1 = serial_comm()
    def serial_read():
        while True:
            sc1.read()
            if sc1.distance < 10:
                pass
                # textToSpeech('반갑다!')

    serial_reader = threading.Thread(target = serial_read)
    serial_reader.start()
    
    textToSpeech('J-Robot 시작합니다.')
    status_ui = aiy.voicehat.get_status_ui()
    status_ui.status('starting')
    assistant = aiy.assistant.grpc.get_assistant()
    button = aiy.voicehat.get_button()
    with aiy.audio.get_recorder():
        while True:
            status_ui.status('ready')
            print('Press the button and speak')
            button.wait_for_press()
            status_ui.status('listening')
            # text is what I said (speech to text)
            # audio is answer of assistant
            text, audio = assistant.recognize()
            local, answer = local_commands(text)
            if local is False:
                aiy.audio.play_audio(audio, assistant.get_volume())
            sc1.action()
            


if __name__ == '__main__':
    main()



