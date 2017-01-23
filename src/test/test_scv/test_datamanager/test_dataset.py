#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from scv.datamanager.dataset import DataSet

__author__ = 'David Qian'

"""
Created on 01/23/2017
@author: David Qian

"""


class TestDataSet(unittest.TestCase):
    def test_get_training_set(self):
        dataset = DataSet()
        training_set = dataset.get_training_set()
        for rec in training_set:
            print rec.feature
            print rec.label
