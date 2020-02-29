# -*- coding: utf-8 -*-
import scrapy
import logging, os, time
from scrapy_splash import SplashRequest
from scrapy.utils.log import configure_logging
from csrc.common.driver import PROJECT_ROOT_PATH
from csrc.common.splash_scripts import click_bt1_bt2_bt3_script
from csrc.settings import USER_AGENT

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
        headers = {"USER-AGENT": USER_AGENT}
        for url in self.start_urls:
            yield SplashRequest('https://www.ubereats.com/new_york/', self.parse, endpoint='execute', args={
                'lua_source': click_bt1_bt2_bt3_script,
                'wait': 5
            }, splash_headers=headers, headers=headers)

    def parse(self, response):
        t0 = time.time()
        self.logger.info("start parse")
        data_list = response.xpath('//*[@id="DataList"]')
        self.logger.info("success parse html data,cost:{}".format(time.time() - t0))
