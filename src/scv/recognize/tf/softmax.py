#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import tensorflow as tf
import objgraph
import gc

from scv.log.logger import log

__author__ = 'David Qian'

"""
Created on 01/22/2017
@author: David Qian

"""

# http://www.shareditor.com/blogshow/?blogId=94


class SoftmaxTrainer(object):
    def __init__(self, feature_count, label_count, learning_rate, iterate_count):
        self.x = tf.placeholder(tf.float32, [None, feature_count])
        self.W = tf.Variable(tf.zeros([feature_count, label_count]), name='W')
        self.b = tf.Variable(tf.zeros([label_count]), name='b')
        self.y = tf.nn.softmax(tf.matmul(self.x, self.W) + self.b)
        self.y_ = tf.placeholder(tf.float32, [None, label_count])
        # We should use `tf.reduce_mean` so learning rate could be independent with batch size
        self.cross_entropy = -tf.reduce_mean(self.y_ * tf.log(tf.clip_by_value(self.y, 1e-10, 1.0)))
        self.train_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(self.cross_entropy)
        self.iterate_count = iterate_count
        self.session = tf.InteractiveSession()
        self._persist_f = '/var/sf.dat'

    def train(self, training_pairs, verify_pairs):
        with self.session.as_default():
            self.session.run(tf.initialize_all_variables())

            xs = [p[0] for p in training_pairs]
            ys = [p[1] for p in training_pairs]

            for i in range(self.iterate_count):
                self.session.run(self.train_step, feed_dict={self.x: xs, self.y_: ys})
                # cost = self.session.run(self.cross_entropy, feed_dict={self.x: xs, self.y_: ys})
                # print 'Cost: %f' % cost

                correct_prediction = tf.equal(tf.argmax(self.y, 1), tf.argmax(self.y_, 1))
                accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
                recognize_accuracy = accuracy.eval(feed_dict={
                                                        self.x:  [p[0] for p in verify_pairs],
                                                        self.y_: [p[1] for p in verify_pairs],
                                                    })
                if i % 50 == 0:
                    log.debug('[%d] Recognize accuracy is %f' % (i, recognize_accuracy))

            self.save()

    def save(self):
        saver = tf.train.Saver()
        saver.save(self.session, self._persist_f)

    def restore(self):
        ckpt = tf.train.get_checkpoint_state(os.path.dirname(self._persist_f))
        saver = tf.train.Saver()
        saver.restore(self.session, ckpt.model_checkpoint_path)

    def recognize(self, feature):
        self.restore()
        with self.session.as_default():
            if not isinstance(feature[0], (list, tuple)):
                feature = [feature]

            return self.session.run(tf.argmax(self.y, 1), {self.x: feature})

