#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PIL import Image
from pytesseract import pytesseract

__author__ = 'David Qian'

"""
Created on 09/07/2016
@author: David Qian

"""


class DataImageOCRer(object):
    def __init__(self, img_path):
        self._img_path = img_path
        self._image = Image.open(self._img_path)

    def get_subscribe_num(self):
        subscribe_box = (71, 64, 116, 78)
        return self.recognize_region(subscribe_box)

    def get_deal_num(self):
        deal_box = (129, 62, 170, 78)
        return self.recognize_region(deal_box)

    def recognize_region(self, region_box):
        region = self._image.crop(region_box)
        return pytesseract.image_to_string(region)


if __name__ == '__main__':
    img_path = '../../../images/dist_day_new.jpg'
    ocr = DataImageOCRer(img_path)
    print ocr.get_subscribe_num()
    print ocr.get_deal_num()