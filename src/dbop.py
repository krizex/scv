#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import sys
import os
from scv.app import app
import traceback

def confirm(cfm_str):
    """
    Ask user to enter Y or N (case-insensitive).
    :return: True if the answer is Y.
    :rtype: bool
    """
    answer = ""
    while answer not in ["y", "n"]:
        answer = input(cfm_str + ' [Y/N]').lower()
    return answer == "y"


def init_db(args):
    if not confirm('OK to reset the database?'):
        print('Canceled')
        exit(0)

    from scv.app import db
    with app.app_context():
        db.drop_all()
        db.create_all()


def build_parser():
    parser = argparse.ArgumentParser(description='Database ops')
    subparsers = parser.add_subparsers()

    initdb_parser = subparsers.add_parser('init', help='init database')
    initdb_parser.set_defaults(cmd=init_db)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args(sys.argv[1:])
    args.cmd(args)


if __name__ == '__main__':
    main()
