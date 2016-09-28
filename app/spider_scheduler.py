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

# from apscheduler.schedulers.blocking import BlockingScheduler
# import datetime
# import logging
# logging.basicConfig(level=logging.INFO,format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',datefmt='%Y-%m-%d %H:%M:%S',filename='log1.txt',filemode='a')
# def aps_test(x):
#     print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
#     def aps_date(x):
#         scheduler = BlockingScheduler()
#         scheduler.remove_job('interval_task')
#         print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
#         scheduler = BlockingScheduler()
#         scheduler.add_job(func=aps_test, args=('定时任务',), trigger='cron', second='*/5', id='cron_task')
#         scheduler.add_job(func=aps_date, args=('一次性任务,删除循环任务',), next_run_time=datetime.datetime.now() + datetime.timedelta(seconds=12), id='date_task')
#         scheduler.add_job(func=aps_test, args=('循环任务',), trigger='interval', seconds=3, id='interval_task')
#         scheduler._logger = logging
#         scheduler.start()