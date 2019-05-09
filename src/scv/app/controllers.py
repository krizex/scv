#!/usr/bin/env python
import datetime
from .models.housesales import Sale
__author__ = 'David Qian'

"""
Created on 12/19/2016
@author: David Qian

"""


def get_sales_data():
    records = Sale.query.order_by(Sale.date)
    #  fill the gap of them
    if not records:
        return []

    rets = []
    expt_date = records[0].date + datetime.timedelta(days=0)
    for sale in records:
        while sale.date != expt_date:
            fill_sale = Sale(date=expt_date, subscribe=0, deal=0)
            rets.append(fill_sale)
            expt_date = expt_date + datetime.timedelta(days=1)

        rets.append(sale)
        expt_date = expt_date + datetime.timedelta(days=1)

    return rets


if __name__ == '__main__':
    get_sales_data()
