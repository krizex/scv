#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from scv import config

__author__ = 'David Qian'

"""
Created on 09/07/2016
@author: David Qian

"""


def __init_config_dir():
    for d in (config.root_node['path'],
              config.data_node['path'],
              config.file_store['path'],
              config.logger['path']):
        if not os.path.exists(d):
            os.mkdir(d)

__init_config_dir()
