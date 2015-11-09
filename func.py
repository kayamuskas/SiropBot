import zbot, config
import time, os, random, base64
import fuzzywuzzy
from fuzzywuzzy import process
from datetime import timedelta


from modules.privat import PrivatBankAPI as privat
import modules.weather

# Основные функции бота
###

# Функция отправки ответа
###
def send_reply(response):
    if 'text' in response:
        zbot.api.post(config.URL + "sendMessage", data=response)


# Функция сообщения действия
###
def send_action(response, action):
     if 'text' in response:
        zbot.api.post(config.URL + "sendChatAction?action=" + action, data=response)


# Базовые команды /start и /help
###
def help_message(arguments, message):
    response = {'chat_id': message['chat']['id']}

    result = ["Привет, %s!" % message["from"].get("first_name"),
              "\rЯ умею вот эти команды:"]

    for command in HELPLIST:
        string = ("%s — %s") % (command, HELPLIST[command])
        result.append(string)
        response['text'] = "\n\t".join(result)
    return response


def ping_command(arguments, message):
    response = {'chat_id': message['chat']['id']}

    response['text'] = ["pong"]
    return response


def not_found(arguments, message):
    response = {'chat_id': message['chat']['id']}

    response['text'] = ["Я не знаю такой команды..."]
    return response


# Тестовая команда /base64
###
def base64_decode(arguments, message):
    response = {'chat_id': message['chat']['id']}

    if not arguments:
        response['text'] = "Надо писать, типа: /base64 SGVsbG8h"
    else:
        try:
            response['text'] = base64.b64decode(" ".join(arguments).encode("utf8"))
        except:
            response['text'] = "Немогу расшифровать"
    return response


def base64_decode2(arguments, message):
    response = {'chat_id': message['chat']['id']}

    p = base64.b64decode("".join('SGVsbG8h').encode("utf8"))
    print(p)
    return response


# Псевдо-речь
###
def human_response(message):
    response = {'chat_id': message['chat']['id']}

    ratio = fuzzywuzzy.process.extract(message.get("text", ""), RESPONSES.keys(), limit=1)[0]

    if ratio[1] < 75:
        response['text'] = "Моя твоя не понимать"
    else:
        response['text'] = random.choice(RESPONSES.get(ratio[0])).format_map(
            {'name': message["from"].get("first_name", "")}
        )
    return response 


# Системное время
###
def system_uptime(arguments, message):
    response = {'chat_id': message['chat']['id']}

    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
        uptime_string = str(timedelta(seconds = uptime_seconds))
        response['text']=(uptime_string)
        send_action(response, "typing")
        time.sleep(1)
    return response


# System's load average
###
def system_la(arguments, message):
    response = {'chat_id': message['chat']['id']}

    LA = str(os.getloadavg())
    response['text'] = ("%s") % LA
    send_action(response, "typing")
#    time.sleep(1)
    return response

############################################################################


# Словарь команд для help
###
HELPLIST = {
    "/help": "Вот эта вот помощь",
    "/base64": "Могу перекодировать из base64",
    "/avias": "Сказать цены на заправках Авиас в Днепре",
    "/ping": "pong",
    "/privat": "Показать курсы валют Приватбанка",
    "/weather": "Показать прогноз погоды"
}

# Словарь приветствий
##
RESPONSES = {
    "Hello": ["Hi there!", "Hi!", "Welcome!", "Hello, {name}!"],
    "Hi there": ["Hello!", "Hello, {name}!", "Hi!", "Welcome!"],
    "Hi!": ["Hi there!", "Hello, {name}!", "Welcome!", "Hello!"],
    "Welcome": ["Hi there!", "Hi!", "Hello!", "Hello, {name}!"],
    "Привет": ["Привет!", "Хай!", "Здарова!", "Привет, {name}!"],
    "Хай": ["Привет!", "Хай!", "Здарова!", "Приветик, {name}!"],
    "Здарова": ["Привет!", "Хай!", "Куку!", "Привет, {name}!"],
    "Куку": ["Привет!", "Хай!", "Здарова!", "Приветули, {name}!"],
 }

# Словарь команд
###
CMD = {
    "/start": help_message,
    "/help": help_message,
    "/base64": base64_decode,
    "/uptime": system_uptime,
    "/la": system_la,
    "/ping": ping_command,
    "/avias": privat.avias_prices,
    "/privat": privat.currency,
    "/weather": modules.weather.getweather
}
