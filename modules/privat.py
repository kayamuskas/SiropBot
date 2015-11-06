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
            req_nal = urllib.request.urlopen("https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5")
            # Безнал
            req_bez = urllib.request.urlopen("https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11")
            
            # Парсим нал
            content_nal = req_nal.read().decode('utf8')
            data_nal = json.loads(content_nal)

            # Dollar
            usdbuy = round(float(data_nal[2]['buy']), 2)
            usdsale = round(float(data_nal[2]['sale']), 2)

            # Euro
            eurbuy = round(float(data_nal[1]['buy']), 2)
            eursale = round(float(data_nal[1]['sale']), 2)

            # Rubl
            rubbuy = round(float(data_nal[0]['buy']), 2)
            rubsale = round(float(data_nal[0]['sale']), 2)


            #print(reqnal.headers['content-type']) <- для дебага, смотреть заголовки
            str_a = ("$ покупает по %s, а продает по %s" % (usdbuy, usdsale))
            str_b = ("€ покупает по %s, а продает по %s" % (eurbuy, eursale))
            str_c = ("₽ покупает по %s, а продает по %s" % (rubbuy, rubsale))

            result = ["\rЗначит так, ПриватБанк сегодня, наличный курс:"]
            
            result.append(str_a)
            result.append(str_b)
            result.append(str_c)

            #response['text'] = "\n\t".join(result)


            # Парсим безнал
            content_bez = req_bez.read().decode('utf8')
            data_bez = json.loads(content_bez)

            # Dollar
            usdbuy = round(float(data_bez[2]['buy']), 2)
            usdsale = round(float(data_bez[2]['sale']), 2)

            # Euro
            eurbuy = round(float(data_bez[1]['buy']), 2)
            eursale = round(float(data_bez[1]['sale']), 2)

            # Rubl
            rubbuy = round(float(data_bez[0]['buy']), 2)
            rubsale = round(float(data_bez[0]['sale']), 2)

            str_a = ("$ покупает по %s, а продает по %s" % (usdbuy, usdsale))
            str_b = ("€ покупает по %s, а продает по %s" % (eurbuy, eursale))
            str_c = ("₽ покупает по %s, а продает по %s" % (rubbuy, rubsale))

            result.append("\rа безналичный курс:")

            result.append(str_a)
            result.append(str_b)
            result.append(str_c)

            response['text'] = "\n\t".join(result)


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
