import requests
import func, time
from xml.etree import ElementTree as ET


def prices(arguments, message):
    response = {'chat_id': message['chat']['id']}
    
    # Получаем цены от ПриватБанка по Авиасу в Днепропетровске
    xmlget = requests.get("https://privat24.privatbank.ua/p24/accountorder?oper=prp&avias=price&region=04&type=&PUREXML=")

    # Парсим XML
    root = ET.fromstring(xmlget.content)

#    tree = ET.parse('price.xml')

#    root = tree.getroot()

    # Дата "сегодня" из ответа
    for date in root.iter('date'):
        day = date.attrib
        today = day['traditional']
        print("Сегодня, %s:" % (today))
        result = ["\rСегодня, %s:" % (today)]

    # Цены
    for cost in root.iter('price'):
        avias = cost.attrib
        fuel = avias['type']
        price = avias['price']
        string = ("%s стоит %s" % (fuel, price))
        print(string)
        result.append(string)
        response['text'] = "\n\t".join(result)

    func.send_action(response, "typing")
    time.sleep(1)
    return response
