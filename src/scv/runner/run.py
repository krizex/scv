#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import gc
import sys
import datetime
import objgraph
import requests
from scv import config
from scv.db.db import DBManager
from scv.exceptions.spider import ImageUnableGetException
from scv.log.logger import log
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
    def do_once(self):
        for _ in range(10):
            try:
                self.execute()
                return
            except:
                log.error('execute failed, try again')
                time.sleep(10)

    def run(self):
        prev_check = datetime.datetime.now()
        while True:
            gc.collect()
            expect = datetime.datetime(prev_check.year, prev_check.month, prev_check.day, hour=23, minute=0, second=0)
            now_check = datetime.datetime.now()
            if is_time_to_run(prev_check, now_check, expect):
                self.do_once()
            else:
                time.sleep(60)

            prev_check = now_check

    def execute(self):
        log.info('start to get data')
        url = 'http://www.njhouse.com.cn/2019/spf/getdata'
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        subscribe_num, deal_num = r.content.decode().split('-')
        data_time = datetime.date.today()
        log.info("date=%s, subscribe=%s, deal=%s" % (data_time.strftime("%Y%m%d"), subscribe_num, deal_num))
        with app.app_context():
            if not Sale.query.filter(Sale.date == data_time).all():
                db.session.add(Sale(date=data_time, subscribe=subscribe_num, deal=deal_num))
                db.session.commit()


if __name__ == '__main__':
    Runner().run()
