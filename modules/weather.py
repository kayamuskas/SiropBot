#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Это парсер погоды с информера Гисметео по Днепропетровску
# Потом можно будет сделать по любому городу, передавая его id как аргумент

import feedparser
import logging
import time, func

def parse(arguments, message):

    response = {'chat_id': message['chat']['id']}

    try:

        # Локально парсим тестовый файл. Или потом превратим его в "cache"
        url = ("dp.xml")
        # rss информера по Днепропетровску
        #url = ('http://informer.gismeteo.ua/rss/34504.xml')
        feed = feedparser.parse(url)

        # Формируем результат
        result = ["\rЗначит так, прогноз такой:"]

        # Разгребаем фид
        for item in feed.entries:

           title = str(item.title)
           string = (title[16:] + "\n" + item.description + "\n")
           print(string)
           result.append(string)


    except Exception as e:
            logging.warning("Error:" + str(e))
            response['text'] = "Нешмогла :("


    func.send_action(response, "typing")
    time.sleep(1)

    return response
