#decode_message.py

def splitt(message):

    if not message:
        print("leer ...")
    else:
        # New Note - head - content
        com_new = message.find('new note')

        # Add to Note - head - content
        com_add = message.find('add to note')

        # Delete Note - head
        com_del = message.find('delete note')

        # Headline
        head = message.find('headline')
        # Content
        cont = message.find('content')

        if com_new != -1:
            command = message[com_new : com_new + 8]
            print(command)
        elif com_add != -1:
            command = message[com_add : com_add + 11]
            print(command)
        elif com_del != -1:
            command = message[com_add : com_add + 11]
            print(command)
        if head != -1 and cont != -1:
            headline = message[head + 9 : cont - 1]
            print(headline)
        if cont != -1:
            content = message[cont + 8 : len(message)]
            print(content)
