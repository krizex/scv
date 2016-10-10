#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

        if self.vcount() == NumberModle(matrix, 'UNKNOWN').vcount():
            return True

        return False