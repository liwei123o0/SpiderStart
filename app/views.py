# -*- coding: utf-8 -*-
#! /usr/bin/env python

from django.shortcuts import render
import requests
import json
from SpiderStarts.settings import conf



def index(request):
    listprojects = 0
    listspiders =0
    listproject ={}
    #获取服务器地址项目版本信息
    for i in conf:
        try:
            project = json.loads(requests.get("http://%s:%s/listprojects.json"%(i['http'],i['prot']),timeout=1).content)
            status = project['status']
        except:
            status ='no'
            projects = 0
        if status =='ok':
            projects = len(project['projects'])
            listproject[i['http']] = project['projects']
        else:
            projects = 0
        listprojects +=projects

        #获取服务器地址爬虫数信息
        if len(listproject[i['http']]) != 0:
            for j in listproject[i['http']]:
                try:
                    project = json.loads(requests.get("http://%s:%s/listspiders.json?project=%s"%(i['http'],i['prot'],j),timeout=1).content)
                    status = project['status']
                except:
                    status ='no'
                    spiders = 0
                if status =='ok':
                    spiders = len(project['spiders'])
                else:
                    spiders = 0
                listspiders +=spiders
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
                   {'projects':listprojects,'spiders':listspiders,
                    'running':running,'finished':finished,})

def spiderjob(request):
    listjobs = {}
    crawlspider ={}
    cwlspider = []
    #爬虫spiders
    for i in conf:
        try:
            project = json.loads(requests.get("http://%s:%s/listspiders.json?project=%s"%(i['http'],i['prot'],i['name']),timeout=1).content)
            status = project['status']
        except:
            status ='no'
            spiders = []
        if status =='ok':
            crawlspider[i['http']] = [{'name':i['name'],'spiders':project['spiders']}]

    #获取爬虫详细数据
    for i in conf:
        try:
            project = json.loads(requests.get("http://%s:%s/listjobs.json?project=%s"%(i['http'],i['prot'],i['name']),timeout=1).content)
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
            listjobs[i['http']] = [{'coutpend':coutpend,'coutrunn':coutrunn,'coutfinished':coutfinished,
                                    'pending':pending,'running':running,'finished':finished}]
        else:
            coutpend = 0
            coutrunn = 0
            coutfinished =0
        if crawlspider.has_key(i['http']):
            cout = 1
            for spider in  crawlspider[i['http']][0]['spiders']:
                cra = cout,i['name'],spider,i['http']
                cout+=1
                cwlspider.append(list(cra))
    return  render(request,'ui-elements.html',
                   {'coutpend':coutpend,
                    'coutrunn':coutrunn,
                    'coutfinished':coutfinished,
                    'pending':pending,
                    'running':running,
                    'finished':finished,
                    'listjobs':listjobs,
                    'cwlspider':cwlspider})

