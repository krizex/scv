#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import sys
import os
import json
from scv.app import app
from scv.app.models.housesales import Sale
import traceback
import datetime

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


def __create_records(db):
    day0 = datetime.date.today() - datetime.timedelta(days=10)
    day1 = datetime.date.today()
    db.session.add(Sale(date=day0, subscribe=100, deal=200))
    db.session.add(Sale(date=day1, subscribe=200, deal=300))
    db.session.commit()


def _restore_records(db):
    f = './dumps.json'
    with open(f) as f:
        js = json.load(f)

    for rec in js:
        s = rec['date']
        date =   '-'.join([s[:4], s[4:6], s[6:]])
        sale = Sale(date=date, subscribe=rec['subscribe'], deal=rec['deal_num'])
        db.session.add(sale)

    db.session.commit()


def insert_records(args):
    from scv.app import db
    with app.app_context():
        # __create_records(db)
        _restore_records(db)



def build_parser():
    parser = argparse.ArgumentParser(description='Database ops')
    subparsers = parser.add_subparsers()

    initdb_parser = subparsers.add_parser('init', help='init database')
    initdb_parser.set_defaults(cmd=init_db)

    initdb_parser = subparsers.add_parser('restore', help='restore records')
    initdb_parser.set_defaults(cmd=insert_records)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args(sys.argv[1:])
    args.cmd(args)


if __name__ == '__main__':
    main()
