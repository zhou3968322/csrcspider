# -*- coding: utf-8 -*-
import scrapy
import logging, os, time
from scrapy_splash import SplashRequest
from scrapy.utils.log import configure_logging
from csrc.common.driver import PROJECT_ROOT_PATH

splash_args = {
    'wait': 0.5,
}

class CsrcSpider(scrapy.Spider):
    
    name = 'csrc_spider'
    start_urls = ["http://www.csrc.gov.cn/pub/zjhpublic/"]

    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename=os.path.join(PROJECT_ROOT_PATH, 'log/spider.log'),
        format='%(levelname)s: %(message)s',
        level=logging.INFO
    )

    def start_requests(self):
        splash_args = {
            'wait': 0.5,
        }
        for url in self.start_urls:
            yield SplashRequest(url, self.parse_result, endpoint='render.html',
                                args=splash_args)

    def parse(self, response):
        t0 = time.time()
        self.logger.info("start parse")
        data_list = response.xpath('//*[@id="DataList"]')
        self.logger.info("success parse html data,cost:{}".format(time.time() - t0))
