# -*- coding: utf-8 -*-
# email: zhoubingcheng@datagrand.com
# create  : 2020/3/1
import re
from enum import Enum, unique

strip_pattern = re.compile(r"\s+")


@unique
class CsrcMetaParsedStatus(Enum):
    UnCrawled = 0
    UrlCrawled = 1
    FileCrawled = 2


@unique
class CsrcFileParsedStatus(Enum):
    UnCrawled = 0
    FileCrawled = 1



