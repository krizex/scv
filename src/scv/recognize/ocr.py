#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from PIL import Image
from pytesseract import pytesseract

__author__ = 'David Qian'

"""
Created on 09/07/2016
@author: David Qian

"""

VERTICAL = 'vertical'
HORIZON = 'horizon'


class DataImageOCRer(object):
    def __init__(self, img_path):
        self._img_path = img_path
        self._image = Image.open(self._img_path)

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
        number_regions = self.split_numbers(region)
        print number_regions
        self.__print_region(region)
        self.__print_regions(region, number_regions)

        # return pytesseract.image_to_string(region, config='outputbase digits')

    def split_numbers(self, crop_region):
        image = crop_region.convert('1')
        pixdata = image.load()

        vertical_boundaries = []

        left = -1
        for x in range(image.size[0]):
            if left == -1:
                if any([pixdata[x, y] == 0 for y in range(image.size[1])]):
                    left = x
            else:
                if all([pixdata[x, y] == 255 for y in range(image.size[1])]):
                    right = x - 1
                    vertical_boundaries.append((left, right))
                    left = -1

        number_regions = []
        # all vertical boundaries have found
        for left, right in vertical_boundaries:
            top = -1
            for y in range(image.size[1]):
                if top == -1:
                    if any([pixdata[x, y] == 0 for x in range(left, right + 1)]):
                        top = y
                else:
                    if all([pixdata[x, y] == 255 for x in range(left, right + 1)]):
                        bottom = y - 1
                        number_regions.append(((left, top), (right, bottom)))
                        break

        return number_regions

    def __print_regions(self, region, region_coords):
        for top_left, bottom_right in region_coords:
            self.__print_region(region, (top_left, bottom_right))
            print ''

    def __print_region(self, region, coord=None):
        image = region.convert('1')
        pixdata = image.load()
        if coord is None:
            coord = ((0, 0), (image.size[0]-1, image.size[1]-1))

        top_left, bottom_right = coord

        for i in range(top_left[1], bottom_right[1] + 1):
            for j in range(top_left[0], bottom_right[0] + 1):
                if pixdata[j, i] == 255:
                    sys.stdout.write(' ')
                else:
                    sys.stdout.write('1')

            print ''


if __name__ == '__main__':
    img_path = '../running/data/images/20160908.jpg'
    ocr = DataImageOCRer(img_path)
    print ocr.get_subscribe_num()
    print ocr.get_deal_num()
