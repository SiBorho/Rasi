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


def getText(text):
    print(text)
    out = dm.splitt(text)


def output(text):
    print(text)


def main():
    """Run TJ"""
    #sr.simple_recognition()

    """New Command"""
    #sr.recordCommands()

    """debug"""
    rec.start()
    #stt.debug_shoppinglist()
    #stt.debug_delete_note()
    #stt.debug_get_note()
    #stt.debug_get_note_shopping_list()


if __name__ == '__main__':
    main()
