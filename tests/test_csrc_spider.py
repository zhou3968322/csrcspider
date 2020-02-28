# -*- coding: utf-8 -*-
# email: zhoubingcheng@datagrand.com
# create  : 2020/2/28

import sys, os

PROJECT_ROOT_PATH = os.path.abspath(os.path.join(os.path.abspath(__file__), "../../"))

print(PROJECT_ROOT_PATH)
sys.path.append(PROJECT_ROOT_PATH)

from csrc.common.utils import fake_response_from_file
from csrc.spiders.csrc_spider import CsrcSpider
import unittest


class TestScrcSpider(unittest.TestCase):
    
    def setUp(self):
        self.spider = CsrcSpider()
    
    def test_crawl_list(self):
        file_path = os.path.join(PROJECT_ROOT_PATH, "tests/samples/list.html")
        result = self.spider.parse(fake_response_from_file(file_path))
        
        
if __name__ == '__main__':
    unittest.main()