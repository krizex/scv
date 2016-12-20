#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import numpy as np
from PIL import Image

from scv.log.logger import log
from scv.recognize.model import NumberModle

__author__ = 'David Qian'

"""
Created on 09/07/2016
@author: David Qian

"""

VERTICAL = 'vertical'
HORIZON = 'horizon'


class RecognizeException(Exception):
    pass


class DataImageOCRer(object):
    def __init__(self, img_path):
        self._img_path = img_path
        self._image = Image.open(self._img_path)
        self._training_set = []
        self.__load_training_set()
        self.__print_training_set()

    def __load_training_set(self):
        dirname = os.path.dirname(__file__)

        for idx in range(10):
            mx = np.load(os.path.join(dirname, 'training_set', '%d.npy' % idx))
            self._training_set.append(NumberModle(mx, str(idx)))

    def __print_training_set(self):
        for idx, s in enumerate(self._training_set):
            matrix = s.get_array()
            self.__log_out_matrix(matrix, str(idx) + ':')

    @property
    def imagefile(self):
        return self._image

    def clip_image(self, region_box):
        return self._image.crop(region_box)

    def get_subscribe_num(self):
        subscribe_box = (71, 64, 116, 78)
        return self.recognize_region(subscribe_box)

    def get_deal_num(self):
        deal_box = (129, 62, 170, 78)
        return self.recognize_region(deal_box)

    def recognize_region(self, region_box):
        region = self.clip_image(region_box)
        self.__print_region(region)
        result = self.__recognize_region(region)
        log.info('Recognize result: %d' % result)
        return result

    def __recognize_region(self, crop_region):
        image = crop_region.convert('1')
        pixdata = image.load()

        mx = None
        nums = []

        for col in range(image.size[0]):
            data = [1 if pixdata[col, row] == 0 else 0 for row in range(image.size[1])]
            if any(data):
                if mx is not None:
                    mx = np.hstack((mx, np.matrix(data).T))
                else:
                    mx = np.matrix(data).T

                num = self.__match_num(mx)
                if num is not None:
                    nums.append(num)
                    mx = None
            else:
                if mx is not None:
                    raise RecognizeException('recognize failed')

                mx = None

        return int(''.join(nums))

    def __match_num(self, mx):
        for model in self._training_set:
            if model.match(mx):
                return model.label

        return None

    def __print_region(self, region, coord=None):
        image = region.convert('1')
        pixdata = image.load()
        if coord is None:
            coord = ((0, 0), (image.size[0]-1, image.size[1]-1))

        top_left, bottom_right = coord
        out_matrix = []
        for i in range(top_left[1], bottom_right[1] + 1):
            line = []
            for j in range(top_left[0], bottom_right[0] + 1):
                if pixdata[j, i] == 0:
                    line.append('1')
                else:
                    line.append(' ')

            out_matrix.append(line)

        self.__log_out_matrix(out_matrix, 'Origin matrix:')

    def __log_out_matrix(self, out_matrix, prefix_info=''):
        join_lines = []
        for line in out_matrix:
            join_lines.append(''.join(line))

        log.info('\n'.join([prefix_info] + join_lines))

    def __parse_region(self, region, coord):
        image = region.convert('1')
        pixdata = image.load()

        top_left, bottom_right = coord

        left = -1

        ret_matrix = None

        for col in range(top_left[0], bottom_right[0] + 1):
            data = [1 if pixdata[col, row] == 0 else 0 for row in range(top_left[1], bottom_right[1] + 1)]

            if left == -1:
                if any(data):
                    if ret_matrix:
                        ret_matrix = np.hstack((ret_matrix, np.matrix(data).T))
                    else:
                        ret_matrix = np.matrix(data).T

                    left = col
            else:
                if all([x == 0 for x in data]):
                    break
                else:
                    ret_matrix = np.hstack((ret_matrix, np.matrix(data).T))

        return ret_matrix


if __name__ == '__main__':
    img_path = '../running/data/images/20160908.jpg'
    ocr = DataImageOCRer(img_path)
    print ocr.get_subscribe_num()
    print ocr.get_deal_num()
