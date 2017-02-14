#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import feedparser
import logging
import time, func

def get_news(arguments, message):

    response = {'chat_id': message['chat']['id']}

    try:

        # rss последних новостей с правдакомуа
        url = ('http://www.pravda.com.ua/rss/view_mainnews/')
        feed = feedparser.parse(url)

        # Формируем результат
        result = ["\rПоследние новости:"]

        # Разгребаем фид
        for item in feed.entries:

            string = (item.title + "\n" + item.link + "\n")
            print(string)  # debug
            result.append(string)
            response['text'] = "\n\t".join(result)

    except Exception as e:
            logging.warning("Error:" + str(e))
            response['text'] = "Нешмогла :("


    func.send_action(response, "typing")
    time.sleep(1)

    return response
