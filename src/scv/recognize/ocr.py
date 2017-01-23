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


class FindMode(object):
    FIND_BEGIN = 0
    FIND_END = 1


class DataImageOCRer(object):
    def __init__(self, img_path):
        self._img_path = img_path
        self._image = Image.open(self._img_path)
        # self._training_set = []
        # self.__load_training_set()
        # self.__print_training_set()

    # def __load_training_set(self):
    #     dirname = os.path.dirname(__file__)
    #
    #     for idx in range(10):
    #         mx = np.load(os.path.join(dirname, 'training_set', '%d.npy' % idx))
    #         self._training_set.append(NumberModle(mx, str(idx)))

    # def __print_training_set(self):
    #     for idx, s in enumerate(self._training_set):
    #         matrix = s.get_array()
    #         self.__log_out_matrix(matrix, str(idx) + ':')

    @property
    def imagefile(self):
        return self._image

    def clip_image(self, region_box):
        return self._image.crop(region_box)

    def recognize_subscribe_num(self):
        subscribe_box = (71, 64, 116, 78)
        return self.recognize_region(subscribe_box)

    def recognize_deal_num(self):
        deal_box = (129, 62, 170, 78)
        return self.recognize_region(deal_box)

    def get_subscribe_number_feature(self):
        subscribe_box = (71, 64, 116, 78)
        return self.__get_split_feature(subscribe_box)

    def get_deal_number_feature(self):
        deal_box = (129, 62, 170, 78)
        return self.__get_split_feature(deal_box)

    def __get_split_feature(self, region_box):
        region = self.clip_image(region_box)
        self.__print_region(region)
        split_result = self.__split_region(region)
        ret = []
        left, upper, right, lower = region_box

        for b, e in split_result:
            box = (left + b, upper, left + e, lower)
            digit_region = self.clip_image(box)
            digit_region = digit_region.resize((10, 16))
            ret.append(self.__get_region_feature(digit_region))
            self.__print_region(digit_region)

        return ret

    def recognize_region(self, region_box):
        region = self.clip_image(region_box)
        self.__print_region(region)
        result = self.__recognize_region(region)
        log.info('Recognize result: %d' % result)
        return result

    def __recognize_region(self, crop_region):
        pass

    def __split_region(self, region):
        image = region.convert('1')
        pixdata = image.load()

        mode = FindMode.FIND_BEGIN
        begin = []
        end = []
        for i in range(image.size[0]):
            col = [pixdata[i, j] for j in range(image.size[1])]
            has_data_pix = any([x == 0 for x in col])
            if mode == FindMode.FIND_BEGIN and has_data_pix:
                begin.append(i)
                mode = FindMode.FIND_END
            elif mode == FindMode.FIND_END and not has_data_pix:
                end.append(i)
                mode = FindMode.FIND_BEGIN

        if len(begin) != len(end):
            end.append(image.size[0])

        return self.__fix_split_region(zip(begin, end), pixdata, image.size[1])

    def __fix_split_region(self, region_pair, pixdata, pic_height):
        THRESHOLD = 5
        ret = []
        for b, e in region_pair:
            if e - b < 2 * THRESHOLD:
                ret.append((b, e))
            else:
                while e - b >= 2 * THRESHOLD:
                    best_split_pos = self.__get_best_split_pos(pixdata, pic_height, [b + THRESHOLD, b + THRESHOLD + 1])
                    ret.append((b, best_split_pos))
                    b = best_split_pos

                ret.append((b, e))

        return ret

    def __get_best_split_pos(self, pixdata, pic_height, candidate_poses):
        best_pos = (-1, pic_height)
        for pos in candidate_poses:
            pix_num = sum([int(pixdata[pos, i] == 0) for i in range(pic_height)])
            if pix_num <= best_pos[1]:
                best_pos = (pos, pix_num)

        return best_pos[0]

    def __get_region_feature(self, region):
        image = region.convert('1')
        pixdata = image.load()

        feature = []
        for j in range(image.size[1]):
            for i in range(image.size[0]):
                feature.append(pixdata[i, j])

        return feature

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

    # def __parse_region(self, region, coord):
    #     image = region.convert('1')
    #     pixdata = image.load()
    #
    #     top_left, bottom_right = coord
    #
    #     left = -1
    #
    #     ret_matrix = None
    #
    #     for col in range(top_left[0], bottom_right[0] + 1):
    #         data = [1 if pixdata[col, row] == 0 else 0 for row in range(top_left[1], bottom_right[1] + 1)]
    #
    #         if left == -1:
    #             if any(data):
    #                 if ret_matrix:
    #                     ret_matrix = np.hstack((ret_matrix, np.matrix(data).T))
    #                 else:
    #                     ret_matrix = np.matrix(data).T
    #
    #                 left = col
    #         else:
    #             if all([x == 0 for x in data]):
    #                 break
    #             else:
    #                 ret_matrix = np.hstack((ret_matrix, np.matrix(data).T))
    #
    #     return ret_matrix


if __name__ == '__main__':
    img_path = '../running/data/images/20160908.jpg'
    ocr = DataImageOCRer(img_path)
    print ocr.recognize_subscribe_num()
    print ocr.recognize_deal_num()
