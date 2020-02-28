# -*- coding: utf-8 -*-
# email: zhoubingcheng@datagrand.com
# create  : 2020/2/28
import hashlib, os, codecs
from scrapy.http import Request, HtmlResponse


def get_binary_md5(file_path):
    with open(file_path, "rb") as fr:
        file_binary = fr.read()
    return get_md5(file_binary)


def get_md5(file_binary):
    hash_md5 = hashlib.md5()
    hash_md5.update(file_binary)
    md5_code = hash_md5.hexdigest()
    return md5_code


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

    response = HtmlResponse(url=url, request=request, body=file_content, encoding = 'utf-8')
    return response


