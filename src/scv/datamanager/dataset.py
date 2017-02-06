#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import os
from collections import namedtuple

import pymongo

from scv.db.db import DBManager

__author__ = 'David Qian'

"""
Created on 01/23/2017
@author: David Qian

"""


class SalesData(object):
    def __init__(self, pic_name, subscribe_num, deal_num):
        self.pic_name = pic_name
        self.subscribe_num = subscribe_num
        self.deal_num = deal_num


class SalesFeatureLabel(object):
    FeatureLabel = namedtuple('FeatureLabel', ['feature', 'label'])

    def __init__(self, features, labels):
        self.data = []
        self.__init_data(features, labels)

    def __init_data(self, features, labels):
        for feature, label in zip(features, labels):
            label_list = [0.0] * 10
            label_list[label] = 1.0
            self.data.append(self.FeatureLabel(feature, label_list))


class DataSet(object):
    def __init__(self):
        self.__pic_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../running/data/images'))
        self.trainset_percent = 0.7
        self.__data = []
        self.init_dataset()

    @property
    def split_pos(self):
        return int(len(self.__data) * self.trainset_percent)

    def init_dataset(self):
        records = DBManager.fetch_record()
        records = records.sort([('date', pymongo.ASCENDING)])
        for rec in records:
            data_date = datetime.datetime.strptime(rec['date'], '%Y%m%d')
            pic_name = '%s.jpg' % (data_date + datetime.timedelta(days=1)).strftime('%Y%m%d')
            self.__data.append(SalesData(pic_name, rec['subscribe'], rec['deal_num']))

    def real_pic_path(self, pic_name):
        return os.path.join(self.__pic_dir, pic_name)

    def get_training_set(self):
        return self.__get_feature_label(self.__data[:self.split_pos])

    def get_verify_set(self):
        return self.__get_feature_label(self.__data[self.split_pos:])

    def __get_feature_label(self, dataset):
        sales_feature_label_list = []
        from scv.recognize.ocr import DataImageOCRer
        for rec in dataset:
            ocrer = DataImageOCRer(self.real_pic_path(rec.pic_name), None)
            features = ocrer.get_subscribe_number_feature() + ocrer.get_deal_number_feature()
            labels = [int(x) for x in (list(str(rec.subscribe_num)) + list(str(rec.deal_num)))]
            sales_feature_label_list.append(SalesFeatureLabel(features, labels))

        ret = []
        for x in sales_feature_label_list:
            for y in x.data:
                ret.append(y)

        return ret

    @staticmethod
    def print_feature_label(feature, label):
        feature_matrix = []
        for i, x in enumerate(feature):
            if x == 0:
                feature_matrix.append('1')
            else:
                feature_matrix.append(' ')

            if i % 10 == 9:
                feature_matrix.append('\n')

        print 'Digit:'
        print ''.join(feature_matrix)

        label = label.index(1)
        print 'Label: %d' % label





