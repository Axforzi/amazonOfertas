# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonItem(scrapy.Item):
    name = scrapy.Field()
    discount = scrapy.Field()
    img = scrapy.Field()
    link = scrapy.Field()
