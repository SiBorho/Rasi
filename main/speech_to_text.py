#speech_to_text.py
# JbhDgtydR4PVaNUCYT4M
# dJpP79BPgFsXU-rA32fb
"""
Created on 2018.05.12

@author: S.Borho
"""

import requests
import json
import os
import main


def sendIBM():
    audio = open('output.wav', 'rb')
    send(audio)

def debug():
    audio = open('shopping_list.wav', 'rb')
    send(audio)

def send(audio):
    # IBM bluemix API url
    url = 'https://stream.watsonplatform.net/speech-to-text/api/v1/recognize'
    username = '14e2ddc4-5384-4dc7-9ddc-c904964edc72'
    password = 'W6lSrjmxzt46'
    headers={'Content-Type': 'audio/wav'}

    print("Send audio ...")
    try:
        r = requests.post(url, data=audio, headers=headers, auth=(username, password))
    except requests.exceptions.RequestException as e:
        print("Faild: ")
        main.getText(e)

    if r.status_code == 200:
        data = json.loads(r.text)

        if not data['results']:
            result = "There is no Message."
        else:
            result = data['results'][0]['alternatives'][0]['transcript']
    elif r.status_code == 406:
        result = (str(r.status_code) + ' The request specified an Accept header'
            + 'with an incompatible content type.')
    elif r.status_code == 415:
        result = (str(r.status_code) + ' The request specified an unacceptable media type.')
    else:
        result = (str(r.status_code) + ' Unknown Error Code')

    #os.remove('output.wav')
    main.getText(result)
