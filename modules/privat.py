import requests
import logging

class PrivatBankAPI:

    def currency(arguments, message):
        response = {'chat_id': message['chat']['id']}

        try:

            # Нал
            #"https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5"
            # Безнал
            #"https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11"

            if arguments:
                print("Hello Currency!")

        except Exception as e:
           logging.warning("Error:" + str(e))
           response['text'] = "Нешмогла :("

        return response
