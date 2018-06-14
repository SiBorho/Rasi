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
    import pdb; pdb.set_trace()
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
            headline = message[head + 9 : len(message) -1]
        else:
            headline = 'No Headline'
        if com_new != -1:
            command = message[com_new : com_new + 8]
            postNote(headline, content)
        elif com_get != -1:
            command = message[com_get : com_get + 8]
            if headline == 'No Headline':
                getAllNote()
            else:
                getNote(headline)
        elif com_del != -1:
            command = message[com_del : com_del + 11]
            deleteNote(headline)


def postNote(headline, content):
    r = requests.post(url, data={'headline':headline, 'text':content})
    if r.status_code == 201:
        returnValue("Note created: " + headline + " / " + content)
    else:
        returnValue("Faild")

def getAllNote():
    r = requests.get(url)
    if r.status_code == 200:
        returnValue("All Notes: " + r.text)
    else:
        returnValue("Faild")

def getNote(headline):
    import pdb; pdb.set_trace()
    r = requests.get(url2, data={'headline':headline})
    import pdb; pdb.set_trace()
    if r.status_code == 200:
        returnValue("Note: " + r.text)
    else:
        returnValue("Faild")


def deleteNote(headline):
    r = requests.delete(url2, data={'headline':headline})
    import pdb; pdb.set_trace()
    if r.status_code == 204:
        returnValue("Note deleted: " + headline)
    else:
        returnValue("Faild")


def returnValue(text):
    main.output(text)
