# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class ChainItem(Item):

    CN_Code = Field()

    CAS_Number = Field()

    CUS = Field()

    EC_Number = Field()

    UN_Number = Field()

    Nomen = Field()

    Name = Field()