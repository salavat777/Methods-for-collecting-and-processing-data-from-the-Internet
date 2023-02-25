# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import Compose, MapCompose, TakeFirst

# Функция очистки названия товара от пробелов с двух сторон и переносов строки
def clean_name(value):
    return " ".join(value.split())

# Функция преобразования цены в тип int
def str_to_int(value):
    return int(value.replace(" ", ""))

class CastoramaRuItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(input_processor=MapCompose(clean_name))
    url = scrapy.Field()
    price = scrapy.Field(input_processor=TakeFirst(), output_processor=MapCompose(str_to_int))
    image_urls = scrapy.Field()
    images = scrapy.Field()

