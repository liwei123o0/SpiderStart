# -*- coding: utf-8 -*-
#! /usr/bin/env python

from django.shortcuts import render
import requests
import json
from SpiderStarts.settings import conf

def index(request):


    #获取服务器地址项目版本信息
    try:
        project = json.loads(requests.get("http://192.168.10.24:6800/listprojects.json",timeout=1).content)
        status = project['status']
    except:
        status ='no'
        projects = u"未知"
    if status =='ok':
        projects = len(project['projects'])
    else:
        projects = u"未知"
    #获取服务器地址爬虫数信息
    try:
        project = json.loads(requests.get("http://192.168.10.24:6800/listspiders.json?project=spider123",timeout=1).content)
        status = project['status']
    except:
        status ='no'
        spiders = u"未知"
    if status =='ok':
        spiders = len(project['spiders'])
    else:
        spiders = u"未知"
    #获取服务器爬虫负载均衡
    try:
        project = json.loads(requests.get("http://192.168.10.24:6800/daemonstatus.json",timeout=1).content)
        status = project['status']
    except:
        status ='no'
        running = u"未知"
        finished = u'未知'
    if status =='ok':
        running = len(project['running'])
        finished = len(project['finished'])
    else:
        running = u"未知"
        finished = u'未知'
    return  render(request, 'index.html',
                   {'projects':projects,'spiders':spiders,
                    'running':running,'finished':finished,})

def spiderjob(request):
    #获取爬虫详细数据
    try:
        project = json.loads(requests.get("http://192.168.10.24:6800/listjobs.json?project=spider123",timeout=1).content)
        status = project['status']
    except:
        status ='no'
        coutpend = 0
        coutrunn = 0
        coutfinished =0
    if status =='ok':
        coutpend = len(project['pending'])
        pending = project['pending']
        coutrunn = len(project['running'])
        running = project['running']
        coutfinished = len(project['finished'])
        finished = project['finished']
    else:
        coutpend = 0
        coutrunn = 0
        coutfinished =0
    return  render(request,'ui-elements.html',
                   {'coutpend':coutpend,
                    'coutrunn':coutrunn,
                    'coutfinished':coutfinished,
                    'pending':pending,
                    'running':running,
                    'finished':finished})