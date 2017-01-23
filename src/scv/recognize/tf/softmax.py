#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tensorflow as tf

__author__ = 'David Qian'

"""
Created on 01/22/2017
@author: David Qian

"""

# http://www.shareditor.com/blogshow/?blogId=94


class SoftmaxTrainer(object):
    def __init__(self, feature_count, label_count, learning_rate, iterate_count):
        self.x = tf.placeholder(tf.float32, [None, feature_count])
        self.W = tf.Variable(tf.zeros([feature_count, label_count]))
        self.b = tf.Variable(tf.zeros([label_count]))
        self.y = tf.nn.softmax(tf.matmul(self.x, self.W) + self.b)
        self.y_ = tf.placeholder("float", [None, label_count])
        cross_entropy = -tf.reduce_sum(self.y_ * tf.log(self.y))
        self.train_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(cross_entropy)
        self.iterate_count = iterate_count
        self.session = tf.InteractiveSession()

    def train(self, training_pairs, verify_pairs):
        init = tf.initialize_all_variables()
        self.session.run(init)

        xs = [p[0] for p in training_pairs]
        ys = [p[1] for p in training_pairs]
        for i in range(self.iterate_count):
            self.session.run(self.train_step, feed_dict={self.x: xs, self.y_: ys})

            correct_prediction = tf.equal(tf.argmax(self.y, 1), tf.argmax(self.y_, 1))
            accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
            recognize_accuracy = accuracy.eval(feed_dict={
                                                    self.x:  [p[0] for p in verify_pairs],
                                                    self.y_: [p[1] for p in verify_pairs],
                                                })

            print 'Recognize accuracy is %f' % recognize_accuracy

    def predict(self, feature):
        return self.session.run(tf.argmax(self.y, 1), {self.x: [feature]})


#
# flags = tf.app.flags
# FLAGS = flags.FLAGS
# flags.DEFINE_string('data_dir', './', 'Directory for storing data')
#
# mnist = input_data.read_data_sets(FLAGS.data_dir, one_hot=True)
#
#
#
#
# x = tf.placeholder(tf.float32, [None, 160])
# W = tf.Variable(tf.zeros([160, 10]))
# b = tf.Variable(tf.zeros([10]))
# y = tf.nn.softmax(tf.matmul(x, W) + b)
# y_ = tf.placeholder("float", [None, 10])
# cross_entropy = -tf.reduce_sum(y_*tf.log(y))
# train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)
#
# init = tf.initialize_all_variables()
# sess = tf.InteractiveSession()
# sess.run(init)
# for i in range(1000):
#     batch_xs, batch_ys = mnist.train.next_batch(100)
#     sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})
#
# correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
# accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
# print(accuracy.eval({x: mnist.test.images, y_: mnist.test.labels}))


