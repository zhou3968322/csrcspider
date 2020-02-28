# -*- coding: utf-8 -*-
# email: zhoubingcheng@datagrand.com
# create  : 2020/2/28


import abc


class Parser(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def parse(self):
        pass
