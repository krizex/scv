#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time

from scv import config
from scv.exceptions.spider import ImageUnableGetException
from scv.log.logger import log
from scv.recognize.ocr import DataImageOCRer
from scv.spider.collect.image import ImageCollector

__author__ = 'David Qian'

"""
Created on 09/07/2016
@author: David Qian

"""


class Runner(object):
    def __init__(self):
        self._collector = ImageCollector(config.file_store['path'])

    def run(self):
        while True:
            try:
                self.execute()
            except ImageUnableGetException:
                log.error('Get image failed.')

            self.suspend()

    def execute(self):
        img_path, data_time = self._download_image()
        ocr = DataImageOCRer(img_path)
        subscribe_num = ocr.get_subscribe_num()
        deal_num = ocr.get_deal_num()
        # TODO: store the data

    def _download_image(self):
        retrys = 5
        for i in range(1, retrys + 1):
            try:
                return self._collector.get_image()
            except ImageUnableGetException:
                log.warn('(%d/%d) unable to download image' % (i, retrys))

        log.error('unable to download image with retry %d times' % retrys)
        raise ImageUnableGetException('Get image failed with retry %d times' % retrys)

    def suspend(self):
        interval = config.scanner['interval']
        log.debug('suspend %d seconds...' % interval)
        time.sleep(interval)


if __name__ == '__main__':
    Runner().run()