#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

from pymongo.errors import DuplicateKeyError

from scv import config
from scv.db.db import DBManager
from scv.exceptions.spider import ImageUnableGetException
from scv.log.logger import log
from scv.recognize.ocr import DataImageOCRer, RecognizeException
from scv.recognize.tf.softmax import SoftmaxTrainer, init_recognizer
from scv.spider.collect.image import ImageCollector

__author__ = 'David Qian'

"""
Created on 09/07/2016
@author: David Qian

"""


class Runner(object):
    def __init__(self):
        self._collector = ImageCollector(config.file_store['path'])
        self._recognizer = SoftmaxTrainer(160, 10, 0.00003, 100)
        init_recognizer(self._recognizer)

    @property
    def recognizer(self):
        return self._recognizer

    def run(self):
        while True:
            start_time = time.time()
            try:
                self.execute()
            except ImageUnableGetException:
                log.error('Get image failed.')
            except RecognizeException:
                log.error('Recognize image failed.')

            log.info('Sleep...')
            self.suspend(time.time() - start_time)

    def execute(self):
        log.info('start to get image')
        img_path, data_time = self._download_image()
        log.info('start to recognize image')
        ocr = DataImageOCRer(img_path, self._recognizer)
        subscribe_num = ocr.recognize_subscribe_num()
        deal_num = ocr.recognize_deal_num()
        log.info("date=%s, subscribe=%s, deal=%s" % (data_time.strftime("%Y%m%d"), subscribe_num, deal_num))
        try:
            DBManager.delete_record({'date': data_time.strftime("%Y%m%d")})
            DBManager.insert_record({
                'date': data_time.strftime("%Y%m%d"),
                'subscribe': subscribe_num,
                'deal_num': deal_num
            })
        except DuplicateKeyError:
            log.warn('duplicate record')

    def _download_image(self):
        retrys = 5
        for i in range(1, retrys + 1):
            try:
                return self._collector.get_image()
            except ImageUnableGetException:
                log.warn('(%d/%d) unable to download image' % (i, retrys))

        log.error('unable to download image with retry %d times' % retrys)
        raise ImageUnableGetException('Get image failed with retry %d times' % retrys)

    def suspend(self, elaps_time=0):
        interval = config.scanner['interval']
        log.debug('suspend %d seconds...' % interval)
        time.sleep(interval - elaps_time)


if __name__ == '__main__':
    Runner().run()
