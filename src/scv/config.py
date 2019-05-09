#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os

__author__ = 'David Qian'

"""
Created on 09/07/2016
@author: David Qian

"""


root_node = {
    'path': os.path.join(os.path.dirname(__file__), 'running')
}

data_node = {
    'path': os.path.join(root_node['path'], 'data')
}

file_store = {
    'path': os.path.join(data_node['path'], 'images')
}

scanner = {
    'interval': 24 * 3600
}

logger = {
    'path': os.path.join(root_node['path'], 'logs'),
    'file': 'scv.log',
    'level': logging.DEBUG,
    'maxBytes': 1024 * 1024 * 20,
    'backupCount': 5,
}

user = os.environ['POSTGRES_USER']
password = os.environ['POSTGRES_PASSWORD']
host = os.environ['POSTGRES_HOST']
port = os.environ['POSTGRES_PORT']
database = os.environ['POSTGRES_DB']

DATABASE_CONNECTION_URI = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(user, password, host, port, database)
