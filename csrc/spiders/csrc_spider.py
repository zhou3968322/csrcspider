# -*- coding: utf-8 -*-
import scrapy
import logging, os, random
from scrapy_splash import SplashRequest
from scrapy.utils.log import configure_logging
from csrc.settings import PROJECT_ROOT_PATH
from csrc.common.lua_scripts import get_redirect_url_script, get_next_url_script
from csrc.settings import USER_AGENT, user_agent_list
from csrc.common.utils import normalize, get_str_md5
from csrc.items import CsrcMetaItem, FileMetaItem, UrlItem
from bs4 import BeautifulSoup as Bs
from urllib.parse import urljoin

splash_args = {
    'wait': 0.5,
}


class CsrcSpider(scrapy.Spider):
    name = 'csrc_spider'
    start_urls = ["http://www.csrc.gov.cn/pub/newsite/xxpl/"]
    
    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename=os.path.join(PROJECT_ROOT_PATH, 'log/spider.log'),
        format='%(levelname)s: %(message)s',
        level=logging.INFO
    )
    
    def start_requests(self):
        headers = {"USER-AGENT": random.choice(user_agent_list)}
        for url in self.start_urls:
            yield SplashRequest(url, self.parse_get_parse_url,
                                endpoint='execute',
                                args={'lua_source': get_redirect_url_script},
                                splash_headers=headers,
                                headers=headers)
    
    def parse_get_parse_url(self, response):
        headers = {"USER-AGENT": random.choice(user_agent_list)}
        assert hasattr(response, "data") and isinstance(response.data, dict)
        parse_url = response.data.get("parse_url", "")
        next_url = response.data.get("next_url", "")
        if parse_url:
            yield scrapy.Request(url=parse_url, callback=self.parse_get_child_url, headers=headers)
        if next_url:
            yield SplashRequest(next_url, self.parse_get_parse_url,
                                endpoint='execute',
                                args={'lua_source': get_next_url_script},
                                splash_headers=headers,
                                headers=headers)

    def parse_get_child_url(self, response):
        headers = {"USER-AGENT": random.choice(user_agent_list)}
        child_selectors = response.selector.xpath("//*[@id='myul']//a")
        for child_selector in child_selectors:
            child_url = urljoin(response.url, child_selector.attrib["href"])
            self.logger.info("start to parse child_url:{}".format(child_url))
            yield scrapy.Request(url=child_url, callback=self.parse, headers=headers)
    
    def parse(self, response):
        try:
            meta_item = self._parse_child_meta(response)
            self.logger.info("finish parse child url:{}".format(response.url))
            yield meta_item
        except Exception as e:
            self.logger.exception("failed parse child url:{}".format(response.url))

    """
    #一些测试代码
    def parse_url(self, response):
        url_item = UrlItem()
        url_item["url"] = response.url
        yield url_item
    """


    @staticmethod
    def _parse_child_meta(response):
        csrc_meta_item = CsrcMetaItem()
        csrc_meta_item["crawl_url"] = response.url
        md5 = get_str_md5(response.url)
        csrc_meta_item["url_md5"] = md5
        title_str = response.selector.xpath("//*[@id =\"lTitle\"]").get()
        title_soup = Bs(title_str, 'html.parser')
        csrc_meta_item["title"] = normalize(title_soup.get_text())
        other_str_list = response.selector.xpath("//*[@id=\"headContainer\"]/tbody/tr/td//td").getall()
        for i in range(len(other_str_list)):
            str_soup = Bs(other_str_list[i], 'html.parser')
            soup_texts = normalize(str_soup.get_text()).split(":")
            if len(soup_texts) == 2:
                csrc_meta_item[csrc_meta_item.get_html_keys()[i]] = soup_texts[1]
            else:
                csrc_meta_item[csrc_meta_item.get_html_keys()[i]] = ''.join(soup_texts)
        a_selector_list = response.selector.xpath("//*[@class=\"mainContainer\"]//*[@class=\"content\"]//a")
        file_meta_list = []
        for a_selector in a_selector_list:
            file_meta_item = FileMetaItem()
            file_url = urljoin(response.url, a_selector.attrib["href"])
            file_meta_item["file_url"] = file_url
            file_meta_item["url_md5"] = get_str_md5(file_url)
            file_meta_item["pmd5"] = md5
            file_meta_item["file_name"] = os.path.basename(file_url)
            file_meta_item["release_date"] = csrc_meta_item.get("release_date")
            file_meta_item.init_status()
            file_meta_list.append(file_meta_item)
        csrc_meta_item["file_meta_list"] = file_meta_list
        csrc_meta_item.init_status()
        return csrc_meta_item
