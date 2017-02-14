import requests, json
import urllib.request
import logging
import func, time
import datetime

from urllib import request
from xml.etree import ElementTree as ET

from modules.rulezdev import RulezDevAPI as rulez

class PrivatBankAPI:

    def currency(arguments, message):
        response = {'chat_id': message['chat']['id']}
        response['parse_mode'] = 'markdown'

        now = datetime.datetime.now()

        try:

            # Нал
            req_nal = urllib.request.urlopen("https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5")
            # Безнал
            req_bez = urllib.request.urlopen("https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11")

            # Парсим нал
            content_nal = req_nal.read().decode('utf8')
            data_nal = json.loads(content_nal)

            for x in range(3):
                ccy = (data_nal[x]['ccy'])

                if ccy == 'USD':
                    # Dollar
                    usdbuy = round(float(data_nal[x]['buy']), 2)
                    usdsale = round(float(data_nal[x]['sale']), 2)
                    print('Yes, USD')

                elif ccy == 'EUR':
                    # Euro
                    eurbuy = round(float(data_nal[x]['buy']), 2)
                    eursale = round(float(data_nal[x]['sale']), 2)
                    print('Yes, EUR')

                elif ccy == 'RUR':
                    # Rubl
                    rubbuy = round(float(data_nal[x]['buy']), 2)
                    rubsale = round(float(data_nal[x]['sale']), 2)
                    print('Yes, RUR')

#                elif ccy == 'BTC':
#                    # BitCoin
#                    btcbuy = round(float(data_nal[x]['buy']), 2)
#                    btcsale = round(float(data_nal[x]['sale']), 2)
#                    print('Yes, BTC')

                else:
                    print('Not found')


            #print(reqnal.headers['content-type']) <- для дебага, смотреть заголовки
            str_a = ("*$* покупает по ```%s```, а продает по `%s`" % (usdbuy, usdsale))
            str_b = ("*€* покупает по ```%s```, а продает по `%s`" % (eurbuy, eursale))
            str_c = ("*₽* покупает по ```%s```, а продает по `%s`" % (rubbuy, rubsale))
#            str_d = ("*Ƀ* покупает по ```$%s```, а продает по `$%s`" % (btcbuy, btcsale))

            today = now.strftime("%Y-%m-%d %H:%M")
            result = ["\rЗначит так, _ПриватБанк_ сегодня (%s), *наличный курс*:" % today] 

            result.append(str_a)
            result.append(str_b)
            result.append(str_c)
#            result.append(str_d)
            #response['text'] = "\n\t".join(result)


            # Парсим безнал
            content_bez = req_bez.read().decode('utf8')
            data_bez = json.loads(content_bez)

            for x in range(3):
                ccy = (data_bez[x]['ccy'])

                if ccy == 'USD':
                    # Dollar
                    usdbuy = round(float(data_bez[x]['buy']), 2)
                    usdsale = round(float(data_bez[x]['sale']), 2)
                    print('Yes, USD')

                elif ccy == 'EUR':
                    # Euro
                    eurbuy = round(float(data_bez[x]['buy']), 2)
                    eursale = round(float(data_bez[x]['sale']), 2)
                    print('Yes, EUR')

                elif ccy == 'RUR':
                    # Rubl
                    rubbuy = round(float(data_bez[x]['buy']), 2)
                    rubsale = round(float(data_bez[x]['sale']), 2)
                    print('Yes, RUR')

#                elif ccy == 'BTC':
#                    # BitCoin
#                    btcbuy = round(float(data_bez[x]['buy']), 2)
#                    btcsale = round(float(data_bez[x]['sale']), 2)
#                    print('Yes, BTC')

                else:
                    print('Not found')


            str_a = ("*$* покупает по ```%s```, а продает по `%s`" % (usdbuy, usdsale))
            str_b = ("*€* покупает по ```%s```, а продает по `%s`" % (eurbuy, eursale))
            str_c = ("*₽* покупает по ```%s```, а продает по `%s`" % (rubbuy, rubsale))
#            str_d = ("*Ƀ* покупает по ```$%s```, а продает по `$%s`" % (btcbuy, btcsale))

            result.append("\n*безналичный курс*:")

            result.append(str_a)
            result.append(str_b)
            result.append(str_c)
#            result.append(str_d)

            # Добавляем инфу от Карла
            market = rulez.currency()
            #result.append("\nа вот на [черном рынке](http://minfin.com.ua/currency/auction/usd/buy/dnepropetrovsk/?presort=&sort=time&order=desc) %s" % market)
            result.append("\nа вот на *черном рынке* %s" % market)
            response['reply_markup'] = json.dumps({'inline_keyboard': [[{'text': '💵 Минфин 💶', 'url': 'http://minfin.com.ua/currency/auction/usd/buy/dnepropetrovsk/?presort=&sort=time&order=desc'}]]})
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
