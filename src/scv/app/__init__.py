#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template

from scv.app.views import display_sales_data

__author__ = 'David Qian'


"""
Created on 12/19/2016
@author: David Qian

"""


app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return display_sales_data()


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080, passthrough_errors=True)
