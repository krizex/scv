#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymongo

__author__ = 'David Qian'

"""
Created on 09/07/2016
@author: David Qian

"""


class _DBManager(object):
    def __init__(self):
        self.client = pymongo.MongoClient("localhost", 27017)
        self.table = self.client.scv.sales

    def insert_record(self, rec):
        return self.table.insert_one(rec).inserted_id

    def delete_record(self, filter):
        return self.table.delete_one(filter).deleted_count

    def fetch_record(self):
        return self.table.find()


DBManager = _DBManager()