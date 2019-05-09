#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .models.housesales import Sales
__author__ = 'David Qian'

"""
Created on 12/19/2016
@author: David Qian

"""


def get_sales_data():
    records = Sales.query.order_by(Sales.date)
    return [rec for rec in records]


if __name__ == '__main__':
    get_sales_data()
