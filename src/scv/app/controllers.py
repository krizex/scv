#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymongo

from scv.db.db import DBManager

__author__ = 'David Qian'

"""
Created on 12/19/2016
@author: David Qian

"""


def get_sales_data():
    records = DBManager.fetch_record()
    records = records.sort([('date', pymongo.ASCENDING)])
    return [rec for rec in records]


if __name__ == '__main__':
    get_sales_data()