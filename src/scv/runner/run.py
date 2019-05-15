#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import gc
import sys
import datetime
import objgraph
from scv import config
from scv.db.db import DBManager
from scv.exceptions.spider import ImageUnableGetException
from scv.log.logger import log
from scv.recognize.ocr import DataImageOCRer, RecognizeException
from scv.recognize.tf.softmax import SoftmaxTrainer
from scv.spider.collect.image import ImageCollector
from scv.app import app
from scv.app import db
from scv.app.models.housesales import Sale
from scv.datamanager.dataset import DataSet

__author__ = 'David Qian'

"""
Created on 09/07/2016
@author: David Qian

"""

def is_time_to_run(prev, now, expt):
    return prev < expt <= now


class Runner(object):
    def __init__(self, train):
        self._collector = ImageCollector(config.file_store['path'])
        self._recognizer = SoftmaxTrainer(160, 10, 0.00005, 500)
        self.init(train)

    def init(self, train):
        if train:
            dataset = DataSet()
            training_set = dataset.get_training_set()
            verify_set = dataset.get_verify_set()
            self._recognizer.train(training_set, verify_set)
        else:
            self._recognizer.restore()

    def do_once(self):
        try:
            self.execute()
        except ImageUnableGetException:
            log.error('Get image failed.')
        except RecognizeException:
            log.error('Recognize image failed.')


    def run(self):
        prev_check = datetime.datetime.now()
        while True:
            gc.collect()
            expect = datetime.datetime(prev_check.year, prev_check.month, prev_check.day, hour=12, minute=30, second=0)
            now_check = datetime.datetime.now()
            if is_time_to_run(prev_check, now_check, expect):
                self.do_once()
            else:
                time.sleep(60)

            prev_check = now_check

    def execute(self):
        log.info('start to get image')
        img_path, data_time = self._download_image()
        log.info('start to recognize image')
        ocr = DataImageOCRer(img_path, self._recognizer)
        subscribe_num = ocr.recognize_subscribe_num()
        deal_num = ocr.recognize_deal_num()
        log.info("date=%s, subscribe=%s, deal=%s" % (data_time.strftime("%Y%m%d"), subscribe_num, deal_num))
        with app.app_context():
            if not Sale.query.filter(Sale.date == data_time).all():
                db.session.add(Sale(date=data_time, subscribe=subscribe_num, deal=deal_num))
                db.session.commit()

    def _download_image(self):
        retrys = 5
        for i in range(1, retrys + 1):
            try:
                return self._collector.get_image()
            except ImageUnableGetException:
                log.warn('(%d/%d) unable to download image' % (i, retrys))

        log.error('unable to download image with retry %d times' % retrys)
        raise ImageUnableGetException('Get image failed with retry %d times' % retrys)


if __name__ == '__main__':
    if sys.argv[1] == 'train':
        Runner(True)
    else:
        Runner(False).run()
