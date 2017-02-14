# https://github.com/novel/py-urbandict
import urbandict
import json
from html.parser import HTMLParser

def get_word(arguments, message):

    response = ""

    chat_id = message['chat']['id']
    response = {'chat_id': message['chat']['id']}

    # Convert XML/HTML Entities into Unicode String    
    h = HTMLParser()

    try:

        try:
            li = urbandict.define((arguments[0]))
            print(li)

        except IndexError:
            li = urbandict.define(urbandict.TermTypeRandom())
            print(li)

        a = li[0]

        word = (h.unescape(a['word']))
        definition = (h.unescape(a['def']))
        example = (h.unescape(a['example']))


        result = ["Word: " + word]
        result.append("Definition:")
        result.append(definition)
       
        if example:
            result.append("Example:")
            result.append(example)

        response['text'] = "\n\t".join(result)

    except:
        response['text'] = ("Я хз что сказать...")

    return response
