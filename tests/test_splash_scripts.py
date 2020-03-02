# -*- coding: utf-8 -*-
# email: zhoubingcheng@datagrand.com
# create  : 2020/2/29

import sys, os

PROJECT_ROOT_PATH = os.path.abspath(os.path.join(os.path.abspath(__file__), "../../"))

print(PROJECT_ROOT_PATH)
sys.path.append(PROJECT_ROOT_PATH)

import requests
import unittest
import base64
from csrc.common.lua_scripts import get_redirect_url_script
    

class TestSplashScripts(unittest.TestCase):
    
    def test_get_main_html(self):
        debug_path = os.path.join(PROJECT_ROOT_PATH, "tests/samples/parse_main.html")
     
        resp = requests.post('http://localhost:8050/execute', json={
            'lua_source': get_redirect_url_script,
            'url': 'http://www.csrc.gov.cn/pub/newsite/xxpl/yxpl/'
        })
        with open(debug_path, 'wb') as fw:
            fw.write(resp.content)


if __name__ == '__main__':
    unittest.main()
