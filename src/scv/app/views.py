#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template

from scv.app.controllers import get_sales_data

__author__ = 'David Qian'

"""
Created on 12/19/2016
@author: David Qian

"""


def display_sales_data():
    records = get_sales_data()

    records_date = [str(rec['date']) for rec in records]

    records_date = {
        'categories': records_date
    }
    subscribe = [rec['subscribe'] for rec in records]
    deal_num = [rec['deal_num'] for rec in records]
    sales_data = [
        {
            'name': 'subscribe',
            'data': subscribe,
        },
        {
            'name': 'deal',
            'data': deal_num,
        },
    ]

    print records_date
    print sales_data
    return render_template('sales_data.html', xAxis=records_date, series=sales_data)

