# -*- coding: utf-8 -*-
#! /usr/bin/env python

from celery import task
import paramiko
from app.spider_scheduler import *
@task
def setspidertask(projectname,taskhttp,radio,one,datetime):
    try:
        remove_jobid()
    except :
        pass
    run_interval()
    # try:
    #     cmd = u'echo "test ok" >>/var/spool/cron/crontabs/spider'
    #     ssh = paramiko.SSHClient()
    #     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #     ssh.connect(taskhttp,22,'root', 'root',timeout=10)
    #     stdin, stdout, stderr = ssh.exec_command(cmd)
    #     out = stdout.readlines()
    #     ssh.close()
    # except:
    #     print(u"taskhttp为%s未登录成功"%taskhttp)
    return "OK"