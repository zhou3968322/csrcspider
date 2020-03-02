# -*- coding: utf-8 -*-
# email: zhoubingcheng@datagrand.com
# create  : 2020/3/1

import sys, os

PROJECT_ROOT_PATH = os.path.abspath(os.path.join(os.path.abspath(__file__), "../../"))

print(PROJECT_ROOT_PATH)
sys.path.append(PROJECT_ROOT_PATH)
import unittest
from csrc.common.utils import get_str_md5, normalize_date


class TestUtils(unittest.TestCase):
    
    def test_get_md5(self):
        url = "http://www.csrc.gov.cn/pub/zjhpublic/G00306202/202002/t20200207_370603.htm"
        assert(get_str_md5(url) == "90ec9f2bbe192ac8241c75a177b0b71f")

    def test_normalize_date(self):
        date_str = "2020年01月16日"
        assert(normalize_date(date_str) == "2020-01-16")
    
    
if __name__ == '__main__':
    unittest.main()
