# -*- coding: utf-8 -*-
#! /usr/bin/env python

import time

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler


def scrapyd_curl():

    print('Tick! The time is: %s' % time.strftime('%Y-%m-%d %X',time.localtime()))

def run_interval():
    scheduler = BlockingScheduler()
    scheduler.add_job(scrapyd_curl, 'interval', seconds=3,id='test')
    scheduler.start()

def remove_jobid():
    scheduler = BlockingScheduler()
    scheduler.remove('test')
