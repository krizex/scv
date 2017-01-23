#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from scv.datamanager.dataset import DataSet
from scv.recognize.tf.softmax import SoftmaxTrainer

__author__ = 'David Qian'

"""
Created on 01/23/2017
@author: David Qian

"""


class TestSoftmax(unittest.TestCase):
    def test_train(self):
        dataset = DataSet()
        training_set = dataset.get_training_set()
        verify_set = dataset.get_verify_set()
        print 'training set size is %d' % len(training_set)

        for feature, label in training_set:
            DataSet.print_feature_label(feature, label)

        for feature, label in verify_set:
            DataSet.print_feature_label(feature, label)

        feature_count = len(training_set[0].feature)
        label_count = len(training_set[0].label)

        trainer = SoftmaxTrainer(feature_count, label_count, 0.1, 100)
        trainer.train(training_set, verify_set)

        # for feature, label in verify_set:
        #     DataSet.print_feature_label(feature, label)
        #     predict_label = trainer.predict(feature)
        #     print 'Predict label: %d' % predict_label

