#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import unittest

from scv.datamanager.dataset import DataSet
from scv.recognize.tf.model import MODEL_DIR
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
        print('training set size is %d' % len(training_set))

        feature_count = len(training_set[0].feature)
        label_count = len(training_set[0].label)

        trainer = SoftmaxTrainer(feature_count, label_count, 0.00005, 500)
        trainer.train(training_set, verify_set)

        for feature, label in verify_set:
            DataSet.print_feature_label(feature, label)
            predict_label = trainer.recognize(feature)[0]
            print('Predict label %d' % predict_label)
            self.assertEqual(label.index(1), predict_label)

        if not os.path.exists(os.path.join(MODEL_DIR, 'model.ckpt')):
            trainer.save(os.path.join(MODEL_DIR, 'model.ckpt'))


