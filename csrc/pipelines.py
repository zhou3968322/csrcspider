# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os, json
from scrapy.pipelines.files import FilesPipeline
from scrapy.exceptions import DropItem
from scrapy import Spider, Request
from csrc.settings import FILES_STORE, CRAWL_MD5_SUFFIX, CRAWL_META_SUFFIX, \
    FILE_MD5_SUFFIX, FILE_META_SUFFIX
from csrc.common.utils import strip_date_day
from csrc.common.base import MonthMetaItemWriterPipeline


class TestUrlPipeLine(object):
    
    def process_item(self, item, spider):
        spider.logger.info("current item url:{}".format(item["url"]))


class CrawlItemFilterPipeline(object):
    
    def process_item(self, item, spider):
        if item.is_retired:
            # 发现开始爬取到指定日期之前的文档
            spider.logger.info("crawl meta item has retired,url:{}".format(item["crawl_url"]))
            Spider.close(spider, "item retired")
            raise DropItem()
        elif item['crawl_status'] == 2:
            spider.logger.info("url all item has crawled,url:{}".format(item["crawl_url"]))
            raise DropItem()
        elif item["crawl_status"] == 1:
            spider.logger.info("url meta item has crawled,url:{}".format(item["crawl_url"]))
            return item
        else:
            spider.logger.info("url meta item hasn't crawled,url:{}".format(item["crawl_url"]))
            return item


class FileItemFilterPipeline(object):

    def process_item(self, item, spider):
        new_file_items = []
        for file_item in item["file_meta_list"]:
            if file_item['crawl_status'] == 1:
                spider.logger.info("file item has crawled,url:{}".format(file_item["file_url"]))
            else:
                new_file_items.append(file_item)
        item["file_meta_list"] = new_file_items
        return item
        

class CsrcFilesPipeline(FilesPipeline):
    
    def get_media_requests(self, item, info):
        return [Request(x["file_url"], cb_kwargs={"release_date": item["release_date"],
                                                  "file_name": x["file_name"]}) for x in item["file_meta_list"]]

    def item_completed(self, results, item, info):
        for i in range(len(results)):
            status, media_res = results[i]
            if status:
                item['file_meta_list'][i]["save_path"] = os.path.join(FILES_STORE, media_res['path'])
                item['file_meta_list'][i]["file_md5"] = media_res["checksum"]
        return item

    def file_path(self, request, response=None, info=None):
        release_month = strip_date_day(request.cb_kwargs["release_date"])
        return '{}/{}'.format(release_month, request.cb_kwargs["file_name"])


class FileMetaItemWriterPipeline(MonthMetaItemWriterPipeline):
    def __init__(self):
        super(FileMetaItemWriterPipeline, self).__init__()
        self._dump_fields = ["url_md5", "file_url", "pmd5", "file_name",
                             "release_date", "file_md5", "save_path"]
        self._md5_suffix = FILE_MD5_SUFFIX
        self._meta_suffix = FILE_META_SUFFIX
        
    def process_item(self, item, spider):
        for file_meta in item["file_meta_list"]:
            month_str = strip_date_day(file_meta["release_date"])
            self._update_md5(month_str, file_meta["url_md5"])
            fo = self._get_fo(month_str)
            fo.write(self._dump(file_meta))
            fo.write("\n")
            file_meta["crawl_status"] = 1
        return item
    

class CrawlMetaItemWriterPipeline(MonthMetaItemWriterPipeline):
    def __init__(self):
        super(CrawlMetaItemWriterPipeline, self).__init__()
        self._dump_fields = ["url_md5", "crawl_url", "index_num", "classify_text",
                             "release_agency", "release_date", "title", "article_id",
                             "subject"]
        self._md5_suffix = CRAWL_META_SUFFIX
        self._meta_suffix = CRAWL_MD5_SUFFIX
        
    def process_item(self, item, spider):
        month_str = strip_date_day(item["release_date"])
        self._update_md5(month_str, item["url_md5"])
        fo = self._get_fo(month_str)
        fo.write(self._dump(item))
        fo.write("\n")
        item["crawl_status"] = 2
        return item
