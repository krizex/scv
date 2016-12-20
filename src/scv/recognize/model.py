#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np

from scv.log.logger import log

__author__ = 'David Qian'

"""
Created on 10/10/2016
@author: David Qian

"""


class NumberModle(object):
    def __init__(self, matrix, label):
        self.matrix = matrix
        self.label = label
        self._vcount = []

    def __reshape_matrix(self, matrix):
        m = np.array(matrix)
        while all([x == 0 for x in m[0]]):
            m = np.delete(m, (0), axis=0)

        while all([x == 0 for x in m[-1]]):
            m = np.delete(m, (-1), axis=0)

        return m

    @property
    def shape(self):
        return self.matrix.shape

    def vcount(self):
        if self._vcount:
            return self._vcount

        for col in range(self.matrix.shape[1]):
            self._vcount.append(sum([self.matrix[i, col] for i in range(self.matrix.shape[0])]))

        return self._vcount

    def match(self, matrix):
        if self.shape[1] != matrix.shape[1]:
            return False

        matrix = self.__reshape_matrix(matrix)

        if self.shape[0] != matrix.shape[0]:
            return False

        diff_mat = self.matrix ^ matrix
        total = self.matrix.size
        diff = diff_mat.sum()
        diff_rate = 1.0 * diff / total

        log.debug('label %s, diff rate %f' % (self.label, diff_rate))

        if diff_rate >= 0.1:
            return False

        log.debug('match %s' % self.label)
        return True

    def get_array(self):
        ret = []
        for i in range(self.matrix.shape[0]):
            t = [str(elem) for elem in self.matrix[i]]
            rt = []
            for elem in t:
                if elem == '1':
                    rt.append('1')
                else:
                    rt.append(' ')
            ret.append(rt)

        return ret

