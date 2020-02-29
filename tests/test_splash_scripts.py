# -*- coding: utf-8 -*-
# email: zhoubingcheng@datagrand.com
# create  : 2020/2/29

import sys, os

PROJECT_ROOT_PATH = os.path.abspath(os.path.join(os.path.abspath(__file__), "../../"))

print(PROJECT_ROOT_PATH)
sys.path.append(PROJECT_ROOT_PATH)

import requests
import unittest
from csrc.common.splash_scripts import show_origin_html_script, click_bt1_script, \
    click_bt1_bt2_script, click_bt1_bt2_bt3_script, get_page_html_script, get_page_redirect_script, \
    test_script
    

class TestSplashScripts(unittest.TestCase):
    
    def test_show_origin_html(self):
        screen_debug_path = os.path.join(PROJECT_ROOT_PATH, "tests/samples/origin_html.jpeg")
     
        resp = requests.post('http://localhost:8050/execute', json={
            'lua_source': show_origin_html_script,
            'url': 'http://www.csrc.gov.cn/pub/zjhpublic/'
        })
        with open(screen_debug_path, 'wb') as fw:
            fw.write(resp.content)
            
    def test_click_bt1(self):
        screen_debug_path = os.path.join(PROJECT_ROOT_PATH, "tests/samples/click_bt1_html.jpeg")
    
        resp = requests.post('http://localhost:8050/execute', json={
            'lua_source': click_bt1_script,
            'url': 'http://www.csrc.gov.cn/pub/zjhpublic/'
        })
        with open(screen_debug_path, 'wb') as fw:
            fw.write(resp.content)

    def test_click_bt1_bt2(self):
        screen_debug_path = os.path.join(PROJECT_ROOT_PATH, "tests/samples/click_bt1_bt2_html.jpeg")
    
        resp = requests.post('http://localhost:8050/execute', json={
            'lua_source': click_bt1_bt2_script,
            'url': 'http://www.csrc.gov.cn/pub/zjhpublic/'
        })
        with open(screen_debug_path, 'wb') as fw:
            fw.write(resp.content)

    def test_click_bt1_bt2_bt3(self):
        screen_debug_path = os.path.join(PROJECT_ROOT_PATH, "tests/samples/click_bt1_bt2_bt3_html.jpeg")
    
        resp = requests.post('http://localhost:8050/execute', json={
            'lua_source': click_bt1_bt2_bt3_script,
            'url': 'http://www.csrc.gov.cn/pub/zjhpublic/'
        })
        with open(screen_debug_path, 'wb') as fw:
            fw.write(resp.content)

    def test_get_page_html(self):
        debug_path = os.path.join(PROJECT_ROOT_PATH, "tests/samples/page_debug..html")
        resp = requests.post('http://localhost:8050/execute', json={
            'lua_source': get_page_html_script,
            'url': 'http://www.csrc.gov.cn/pub/zjhpublic/'
        })
        with open(debug_path, 'wb') as fw:
            fw.write(resp.content)
    
    def test_get_redirect_url(self):
        debug_path = os.path.join(PROJECT_ROOT_PATH, "tests/samples/page_redirect..html")
        resp = requests.post('http://localhost:8050/execute', json={
            'lua_source': test_script,
            'url': '/Users/zhoubingcheng/Desktop/study/project/csrcspider/tests/samples/page_debug.html'
        })
        # with open(debug_path, 'wb') as fw:
        #     fw.write(resp.content)
        print("success")


if __name__ == '__main__':
    unittest.main()
