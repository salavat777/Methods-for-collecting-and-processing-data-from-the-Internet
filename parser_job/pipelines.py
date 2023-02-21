# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo


class ParserJobPipeline:
    def __init__(self):
        client = pymongo.MongoClient('localhost:27017')
        self.mongo_db = client.parser_job

    def process_item(self, item, spider):
        print('\n************************\n%s\n%s\n**************************\n'
              % (item, spider))
        collections = self.mongo_db[spider.name]
        collections.insert_one(item)

        return item
