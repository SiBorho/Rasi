#main.py
"""
Created on 2018.05.25

@author: S.Borho
"""


""" HELLO TJ """
""" TJ END """


import simple_recognition as sr
import decode_message as dm
import recording as rec
import speech_to_text as stt
import requests

url = 'http://127.0.0.1:8000/'

def getText(text):
    print(text)
    out = dm.splitt(text)
    send(out)


def send(out):
    r = requests.post("127.0.0.1:8000/", data={'headline' : 'shopping list',
    'content' : 'milk'})
    print(r.status_code, r.reason)


def main():

    """Run TJ"""
    #sr.simple_recognition()

    """New Command"""
    #sr.recordCommands()

    """debug"""
    #rec.start()
    stt.debug()


if __name__ == '__main__':
    main()
