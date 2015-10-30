import tornado
import tornado.web
import tornado.ioloop
import requests
import time
import logging
import func

# API
###
api = requests.Session()

# Заставка на главную
###
class RootHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("It works!")

# Логика бота
###
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("It's bot!")

    def post(self):
        try:
            logging.debug("Got request: %s" % self.request.body)
            update = tornado.escape.json_decode(self.request.body)
            message = update['message']
            text = message['text']
#	    text = message.get('text')
#	    chat_id = message['chat'].get('id')
            chat_id = message['chat']['id']
#           print(chat_id)

            if text:
                logging.info("MESSAGE\t%s\t%s" % (message['chat']['id'], text))

                if text[0] == '/':
                    command, *arguments = text.split(" ", 1)
                    response = func.CMD.get(command, func.not_found)(arguments, message)
                    print(command, arguments) # debug
#                   response = {'chat_id': chat_id}
#                   response["text"] = "Я пока не умею выполнять команды"
                    logging.info("REPLY\t%s\t%s" % (message['chat']['id'], response))
                    func.send_action(response, "typing")
                    #ime.sleep(1)
                    func.send_reply(response)

                else:
                    #response = {'chat_id': chat_id, 'text': text}
                    #response = func.CMD["<speech>"](message)
                    print(message)
                    response = func.human_response(message)
                    logging.info("REPLY\t%s\t%s" % (message['chat']['id'], response))
                    func.send_reply(response)

        except Exception as e:
            logging.warning("Error:" + str(e))
