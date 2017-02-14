import urllib.request, json

import modules.flags.flags

def get_ip(arguments, message):

    chat_id = message['chat']['id']
    response = {'chat_id': message['chat']['id']}

    try:

        try:
            ip = arguments[0]
            print(ip)

        except IndexError:
            response['text'] = ('Нужен ip-адрес в качестве аргумента')
            return response

        url = 'http://ip-api.com/json/%s' % (ip)

        # Парсим json
        request = urllib.request.urlopen(url)
        content = request.read().decode('utf8')
        data = json.loads(content)
        print(data)

        if data['status'] == 'fail':
            if data['message'] == 'invalid query':
                print(data['message'])
                response['text'] = 'Запрос неверный! Это по-твоему ip?!'

            elif data['message'] == 'reserved range':
                response['text'] = 'Запрос неверный! Этот адрес в диапазоне зарезервированных ip!'

            elif data['message'] == 'private range':
                response['text'] = 'Запрос неверный! Этот адрес в диапазоне частых ip!'

        elif data['status'] == 'success':
            result = ['Значит так, я поискал и узнал, что это:']
            flag = (modules.flags.flags.get_flag(data['countryCode']))
            result.append(flag + data['country'] + ' (' + data['countryCode'] + '), ' + data['regionName'])
            result.append('🏨' + 'Город: ' + data['city'])
            result.append('⏱' + 'Часовой пояс: ' + data['timezone'])
            result.append('📡' + 'Провайдер: ' + data['isp'] + ' / ' + data['as'])
            response['text'] = "\n\t".join(result)

        else:
            response['text'] = ("Я хз что сказать...")

    except:
        response['text'] = ("Что-то пошло не так...")

    return response


def grep_ip(ip, message):
    ''' Automatic grep IP from converation'''

    chat_id = message['chat']['id']
    response = {'chat_id': message['chat']['id']}
    response['reply_to_message_id'] = message['message_id']

    try:

        url = 'http://ip-api.com/json/%s' % (ip)

        # Парсим json
        request = urllib.request.urlopen(url)
        content = request.read().decode('utf8')
        data = json.loads(content)

        if data['status'] == 'success':
            if data['org'] == 'My Company':
                response['text'] = 'this is my company!'
            else:
                result = ['Кстати, если речь зашла об ip %s' % (ip) + ', то я тут поискал и нашел, что это:']
                flag = (modules.flags.flags.get_flag(data['countryCode']))
                result.append(flag + data['country'] + ' (' + data['countryCode'] + '), ' + data['regionName'])
                result.append('🏨' + 'Город: ' + data['city'])
                result.append('⏱' + 'Часовой пояс: ' + data['timezone'])
                result.append('📡' + 'Провайдер: ' + data['isp'] + ' / ' + data['as'])
                response['text'] = "\n\t".join(result)

        else:
            pass

    except:
        pass    

    return response
