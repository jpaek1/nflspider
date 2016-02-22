# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NFLTeam(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    teamname = scrapy.Field()
    roster = scrapy.Field()
    passers = scrapy.Field()
    rushers = scrapy.Field()
    receivers = scrapy.Field()
    sackers = scrapy.Field()
    passing_yards_leaders = scrapy.Field()
    rushing_yards_leaders = scrapy.Field()
    receive_yards_leaders = scrapy.Field()
    total_sacks_leaders = scrapy.Field()

class Player(scrapy.Item):
    name = scrapy.Field()
    pass_yards = scrapy.Field()
    rush_yards = scrapy.Field()
    receive_yards = scrapy.Field()
    total_sacks = scrapy.Field()
