#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import datetime
import requests
import time

from scv.exceptions.spider import ImageUnableGetException
from scv.log.logger import log

__author__ = 'David Qian'

"""
Created on 09/07/2016
@author: David Qian

"""


class ImageCollector(object):
    img_url = 'http://www.njhouse.com.cn/include/fdc_include/dataimg/dist_day_new.jpg'

    def __init__(self, store_folder=''):
        self.__store_folder = store_folder if store_folder else '.'

    @property
    def store_folder(self):
        return self.__store_folder

    def get_image(self):
        try:
            r = requests.get(self.img_url, stream=True)
            if r.status_code != 200:
                log.error("get image from '%s' failed" % self.img_url)
                raise ImageUnableGetException('Download image failed')
        except:
            raise ImageUnableGetException('Download image failed')

        f_path = self.__get_store_img_path()
        with open(f_path, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)

        return f_path, datetime.date.today() - datetime.timedelta(days=1)

    def __get_store_img_path(self):
        img_name = '%s.jpg' % time.strftime("%Y%m%d")
        return os.path.join(self.store_folder, img_name)


if __name__ == '__main__':
    collector = ImageCollector()
    img_path, data_time = collector.get_image()
    log.debug(img_path)
