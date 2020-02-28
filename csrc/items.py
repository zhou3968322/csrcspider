# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FileMetaItem(scrapy.Item):
    crawl_url = scrapy.Field()
    file_name = scrapy.Field()
    md5 = scrapy.Field()
    save_path = scrapy.Field()


class CsrcMetaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    index_num = scrapy.Field()
    classify_text = scrapy.Field()
    release_agency = scrapy.Field()
    release_date = scrapy.Field()
    title = scrapy.Field()
    article_id = scrapy.Field()
    subject = scrapy.Field()
    file_meta_list = scrapy.Field()





