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
#	        text = message.get('text')
            chat_id = message['chat']['id']
            chat_type = message['chat']['type']

            if text:
                logging.info("MESSAGE\t%s\t%s" % (message['chat']['id'], text))

                if text[0] == '/':
                    command, *arguments = text.split(" ", 1)
                    response = func.CMD.get(command, func.not_found)(arguments, message)
                    print(command, arguments) # debug
                    logging.info("REPLY\t%s\t%s" % (message['chat']['id'], response))
                    func.send_action(response, "typing")
                    #time.sleep(1)
                    func.send_reply(response)

                elif chat_type == 'private' :
                    print(message) # debug
                    print(chat_type) # debug
                    response = func.human_response(message)
                    logging.info("REPLY\t%s\t%s" % (message['chat']['id'], response))
                    func.send_reply(response)

                    if chat_id == '234270':
                        print("kayama")

                else:
                    print(message) # debug
                    response = {'chat_id': message['chat']['id'], 'text': text}
                    func.send_action(response, "typing")

        except Exception as e:
            logging.warning("Error:" + str(e))
