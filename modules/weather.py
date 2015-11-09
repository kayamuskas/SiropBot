#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Это парсер погоды с информера Гисметео по Днепропетровску
# Потом можно будет сделать по любому городу, передавая его id как аргумент

import feedparser

def parse():
    
    url = ("dp.xml")
    #url = ('http://informer.gismeteo.ua/rss/34504.xml')
    feed = feedparser.parse(url)

    for item in feed.entries:
        title = str(item.title)
        print(title[16:] + "\n" + item.description + "\n")


if __name__ == '__main__':
    parse()
