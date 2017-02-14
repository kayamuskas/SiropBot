import urllib.request, json
import urllib
from html.parser import HTMLParser

def get_aphorism(arguments, message):

    chat_id = message['chat']['id']
    response = {'chat_id': message['chat']['id']}

    # Convert XML/HTML Entities into Unicode String    
    h = HTMLParser()

    try:

        url = 'http://api.forismatic.com/api/1.0/?method=getQuote&format=json'

        # Парсим json
        request = urllib.request.urlopen(url)
        content = request.read().decode('utf8')
        data = json.loads(content)


        if data['quoteText']:
            quote = h.unescape(data['quoteText'])

            if data['quoteAuthor']:
                author = data['quoteAuthor']
            else:
                author = 'кто-то'

            result = ["Однажды " + author + " сказал: " + "«" + quote + "»"]

            response['text'] = "\n\t".join(result)

        else:
            response['text'] = ("Я хз что сказать...")

    except:
        response['text'] = ("Я хз что сказать...")

    return response
