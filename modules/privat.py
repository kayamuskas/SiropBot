import requests, json
import urllib.request
import logging
import func, time

from urllib import request
from xml.etree import ElementTree as ET


class PrivatBankAPI:

    def currency(arguments, message):
        response = {'chat_id': message['chat']['id']}

        try:

            # Нал
            reqnal = urllib.request.urlopen("https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5")
            # Безнал
            reqbez = urllib.request.urlopen("https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11")
            
            # Парсим нал
            content = reqnal.read().decode('utf8')
            datanal = json.loads(content)


            #print(reqnal.headers['content-type']) <- для дебага, смотреть заголовки
            print("Рубль покупаем по %s, а продаем по %s") % (datanal[0]['buy'], datanal[0]['sell'])


            # Парсим безнал


        except Exception as e:
           logging.warning("Error:" + str(e))
           response['text'] = "Нешмогла :("

        func.send_action(response, "typing")
        time.sleep(1)
        return response

    def avias_prices(arguments, message):
        response = {'chat_id': message['chat']['id']}

        try:

            # Получаем цены от ПриватБанка по Авиасу в Днепропетровске
            xmlget = requests.get("https://privat24.privatbank.ua/p24/accountorder?oper=prp&avias=price&region=04&type=&PUREXML=")

            # Парсим XML
            root = ET.fromstring(xmlget.content)

            # Тесты: парсим файл
            #tree = ET.parse('price.xml')
            #root = tree.getroot()

            # Дата "сегодня" из ответа api
            for date in root.iter('date'):
                day = date.attrib
                today = day['traditional']
                print("Сегодня, %s:" % (today))
                result = ["\rСегодня, %s:" % (today)]

            # Выбираем цены
            for cost in root.iter('price'):
                avias = cost.attrib
                fuel = avias['type']
                price = avias['price']
                string = ("%s стоит %s" % (fuel, price))
                print(string)
                result.append(string)
                response['text'] = "\n\t".join(result)

        except Exception as e:
           logging.warning("Error:" + str(e))
           response['text'] = "Нешмогла :("

        func.send_action(response, "typing")
        time.sleep(1)
        return response
