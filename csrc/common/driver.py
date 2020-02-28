# -*- coding: utf-8 -*-
# email: zhoubingcheng@datagrand.com
# create  : 2020/2/28

import os
import sys

if not hasattr(sys.modules[__name__], '__file__'):
    __file__ = '/root/csrcspider/csrc/common/driver.py'

cur_path = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))