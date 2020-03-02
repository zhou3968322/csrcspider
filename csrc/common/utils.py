# -*- coding: utf-8 -*-
# email: zhoubingcheng@datagrand.com
# create  : 2020/2/28
import hashlib, os, codecs, datetime, codecs
from scrapy.http import Request, HtmlResponse
from csrc.common.constants import strip_pattern
from functools import lru_cache
from csrc.settings import META_DIR


def get_file_md5(file_path):
    with open(file_path, "rb") as fr:
        file_binary = fr.read()
    return get_binary_md5(file_binary)


def get_binary_md5(file_binary):
    hash_md5 = hashlib.md5()
    hash_md5.update(file_binary)
    md5_code = hash_md5.hexdigest()
    return md5_code


def get_str_md5(content):
    return get_binary_md5(content.encode(errors='ignore'))


def fake_response_from_file(file_name, url=None):
    """
    Create a Scrapy fake HTTP response from a HTML file
    @param file_name: The relative filename from the responses directory,
                      but absolute paths are also accepted.
    @param url: The URL of the response.
    returns: A scrapy HTTP response which can be used for unittesting.
    """
    if not url:
        url = 'http://www.example.com'

    request = Request(url=url)
    if not file_name[0] == '/':
        responses_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(responses_dir, file_name)
    else:
        file_path = file_name

    with codecs.open(file_path, "r", "utf-8") as fr:
        file_content = fr.read()

    response = HtmlResponse(url=url, request=request, body=file_content, encoding='utf-8')
    return response
    

def normalize(text):
    return strip_pattern.sub("", text).replace("：", ":")


def normalize_date(text):
    try:
        return datetime.datetime.strptime(text, "%Y年%m月%d日").strftime("%Y-%m-%d")
    except ValueError:
        pass
    return datetime.datetime.strptime(text, "%Y-%m-%d").strftime("%Y-%m-%d")


def convert_to_date(text):
    try:
        return datetime.datetime.strptime(text, "%Y年%m月%d日")
    except ValueError:
        pass
    try:
        return datetime.datetime.strptime(text, "%Y-%m-%d")
    except ValueError:
        pass
    return datetime.datetime.strptime(text, "%Y-%m-%d %H:%M:%S")


def strip_date_day(date_str):
    return convert_to_date(date_str).strftime("%Y-%m")


@lru_cache(maxsize=180)
def get_month_md5_list(month_str, md5_suffix):
    meta_month_dir = os.path.join(META_DIR, month_str)
    if not os.path.isdir(meta_month_dir):
        return set()
    md5_path = os.path.join(meta_month_dir, '{}{}'.format(month_str, md5_suffix))
    if not os.path.isfile(md5_path):
        return set()
    with codecs.open(md5_path, 'r', 'utf-8') as fr:
        md5_list = fr.read().splitlines()
    return set(md5_list)


