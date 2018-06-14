#decode_message.py

import requests
import main

#GET - alle headlines
#POST - headline / text -> erstellt new Note
#DELETE - headline
url = 'http://127.0.0.1:8000/api/notes/'
#GET - headline -> bekomme Text von Headline
url2 = 'http://127.0.0.1:8000/api/notes/headline/'


def splitt(message):
    out = []
    if not message:
        returnValue("No message")
    else:
        # New Note - head - content
        com_new = message.find('new note')
        # Get to Note - head - content
        com_get = message.find('get note')
        # Delete Note - head
        com_del = message.find('delete note')
        # Headline
        head = message.find('headline')
        # Content
        cont = message.find('content')


        if cont != -1:
            content = message[cont + 8 : len(message)]
        if head != -1 and cont != -1:
            headline = message[head + 9 : cont - 1]
        elif head != -1:
            headline = message[head + 9 : len(message)]
        else:
            headline = 'No Headline'
        if com_new != -1:
            command = message[com_new : com_new + 8]
            postNote(headline, content)
        elif com_get != -1:
            command = message[com_add : com_add + 8]
            if not headline:
                getAllNote()
            else:
                getNote(headline)
        elif com_del != -1:
            command = message[com_add : com_add + 11]
            deleteNote(headline)


def postNote(headline, content):
    r = requests.post(url, data={'headline':headline, 'text':content})
    returnValue("Note Created: " + headline + " / " + content)

def getAllNote():
    r = requests.get(url)
    returnValue("Note Created: " + headline + " / " + content)

def getNote(headline):
    r = requests.get(url2, data={'headline':headline})
    returnValue("Note Created: " + headline + " / " + content)

def deleteNote(headline):
    r = requests.delete(url, data={'headline':headline})
    print(r.status_code, r.reason)
    returnValue("Note Created: " + headline + " / " + content)

def returnValue():
    main.output(text)
