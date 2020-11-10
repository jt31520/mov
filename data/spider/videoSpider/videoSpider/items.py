# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class VideospiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    name = scrapy.Field()
    image = scrapy.Field()
    updateTo = scrapy.Field()
    score = scrapy.Field()
    alias = scrapy.Field()
    director = scrapy.Field()
    star = scrapy.Field()
    type = scrapy.Field()
    region = scrapy.Field()
    language = scrapy.Field()
    issueTime = scrapy.Field()
    filmLength = scrapy.Field()
    updateTime = scrapy.Field()
    details = scrapy.Field()
    episode = scrapy.Field()
    episodeUrl = scrapy.Field()
    source = scrapy.Field()
    totalPlay = scrapy.Field()
    todayPlay = scrapy.Field()
    totalScore = scrapy.Field()
    scoreTime = scrapy.Field()
    episodeInt = scrapy.Field()