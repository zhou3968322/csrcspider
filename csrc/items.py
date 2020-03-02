# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from csrc.common.constants import CsrcMetaParsedStatus, CsrcFileParsedStatus
from csrc.common.utils import normalize_date, convert_to_date, strip_date_day
from csrc.common.utils import get_month_md5_list as gmml
from csrc.settings import RELEASE_MIN_DATE, RELEASE_MAX_DATE, CRAWL_MD5_SUFFIX, FILE_MD5_SUFFIX


class UrlItem(scrapy.Item):
    
    url = scrapy.Field()


class FileMetaItem(scrapy.Item):
    url_md5 = scrapy.Field()
    file_url = scrapy.Field()
    pmd5 = scrapy.Field()
    file_name = scrapy.Field()
    release_date = scrapy.Field()
    crawl_status = scrapy.Field()
    file_md5 = scrapy.Field()
    save_path = scrapy.Field()
    
    def set_crawled_status(self):
        assert "file_md5" in self.keys() and "save_path" in self.keys()
        # 爬取后的文件item必须有这两个值
        super(FileMetaItem, self).__setitem__("crawl_status", CsrcFileParsedStatus.FileCrawled.value)
    
    def init_status(self):
        assert "release_date" in self.keys() and "url_md5" in self.keys()
        month_str = strip_date_day(self.get("release_date"))
        if self.get("url_md5") in gmml(month_str, FILE_MD5_SUFFIX):
            super(FileMetaItem, self).__setitem__("crawl_status", CsrcFileParsedStatus.FileCrawled.value)
        else:
            super(FileMetaItem, self).__setitem__("crawl_status", CsrcFileParsedStatus.UnCrawled.value)
    
    def __setitem__(self, key, value):
        if key in self.fields:
            if key == "release_date":
                self._values[key] = normalize_date(value)
            else:
                self._values[key] = value
        else:
            raise KeyError("%s does not support field: %s" %
                           (self.__class__.__name__, key))


class CsrcMetaItem(scrapy.Item):
    # define the fields for your item here like:
    
    url_md5 = scrapy.Field()
    crawl_url = scrapy.Field()
    index_num = scrapy.Field()
    classify_text = scrapy.Field()
    release_agency = scrapy.Field()
    release_date = scrapy.Field()
    title = scrapy.Field()
    article_id = scrapy.Field()
    subject = scrapy.Field()
    crawl_status = scrapy.Field()
    file_meta_list = scrapy.Field()
    
    @property
    def is_retired(self):
        assert "release_date" in self.keys()
        date_time = convert_to_date(self.get("release_date"))
        return not (convert_to_date(RELEASE_MIN_DATE) < date_time <= convert_to_date(RELEASE_MAX_DATE))
    
    @staticmethod
    def get_html_keys():
        return ["index_num", "classify_text", "release_agency",
                "release_date", "article_id", "subject"]
    
    def init_status(self):
        assert "url_md5" in self.keys() and "release_date" in self.keys()
        month_str = strip_date_day(self.get("release_date"))
        url_crawl_status = self.get("url_md5") in gmml(month_str, CRAWL_MD5_SUFFIX)
        if not url_crawl_status:
            super(CsrcMetaItem, self).__setitem__("crawl_status", CsrcMetaParsedStatus.UnCrawled.value)
            return
        assert "file_meta_list" in self.keys() and isinstance(self.get("file_meta_list"), list)
        for file_meta in self.get("file_meta_list"):
            assert isinstance(file_meta, FileMetaItem)
            if file_meta["crawl_status"] == CsrcFileParsedStatus.UnCrawled.value:
                super(CsrcMetaItem, self).__setitem__("crawl_status", CsrcMetaParsedStatus.UrlCrawled.value)
                return
        super(CsrcMetaItem, self).__setitem__("crawl_status", CsrcMetaParsedStatus.FileCrawled.value)
    
    def __setitem__(self, key, value):
        if key in self.fields:
            if key == "release_date":
                self._values[key] = normalize_date(value)
            else:
                self._values[key] = value
        else:
            raise KeyError("%s does not support field: %s" %
                           (self.__class__.__name__, key))
