# -*- coding: utf-8 -*-
#! /usr/bin/env python

from django.shortcuts import render
from app.tasks import setspidertask
from SpiderStarts.settings import conf
from django.http import HttpResponse
import os,time,requests,json,MySQLdb,re
from datetime import datetime



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
    cout = 1
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
        #判断字典是否有该key值
        if crawlspider.has_key(i['http']):
            for spider in  crawlspider[i['http']][0]['spiders']:
                cra = cout,i['name'],spider,i['http']
                cout+=1
                cwlspider.append(list(cra))
    return  render(request,'spiderjob.html',
                   {'coutpend':coutpend,
                    'coutrunn':coutrunn,
                    'coutfinished':coutfinished,
                    'pending':pending,
                    'running':running,
                    'finished':finished,
                    'listjobs':listjobs,
                    'cwlspider':cwlspider,
                    })
#任务状态页面
def spiderstatus(request):
    projects={}
    pendings = []
    runnings = []
    finishes = []
    coutp = 0
    coutr=0
    coutf = 0
    for c in conf:
        try:
            project = json.loads(requests.get("http://%s:%s/listjobs.json?project=%s"%(c['http'],c['prot'],c['name']),timeout=1).content)
        except:
            status ='no'
            project={}
        projects[c['http']] = {'finished':project['finished'],'running':project['running'],'pending':project['pending']}
        # cout +=len(project['pending'])
        if projects.has_key(c['http']):
            for pending in  projects[c['http']]['pending']:
                coutp+=1
                cra = coutp,c['http'],c['name'],pending['spider'],pending['id']
                pendings.append(list(cra))
        if projects.has_key(c['http']):
            for running in  projects[c['http']]['running']:
                coutr+=1
                cra = coutr,c['http'],c['name'],running['spider'],running['id'],running['start_time']
                runnings.append(list(cra))
        if projects.has_key(c['http']):
            for finished in  projects[c['http']]['finished']:
                coutf+=1
                cra = coutf,c['http'],c['name'],finished['spider'],finished['id'],finished['start_time'],finished['end_time']
                finishes.insert(0,list(cra))
    return render(request,'spiderstatus.html',{'pendings':pendings,'runnings':runnings,'finishes':finishes})

#根据指定参数运行指定爬虫并返回任务状态
def runspider(request):
    run = request.GET['runspider']
    runstart = json.loads(os.popen("curl %s"%run,'r').read())
    status = runstart['status']
    jobid = runstart['jobid']
    if status =='ok':
        status = u'已启动'
    return HttpResponse(u"启动状态:%s!<br>任务ID:%s"%(status,jobid))

#管局指定参数停止指定爬虫并返回状态
def stopspider(request):
    stop = request.GET['stopspider']
    stopcrawl = json.loads(os.popen("curl %s"%(stop),'r').read())
    status = stopcrawl['status']
    if status =='ok':
        status = u'已停止!'
    else:
        status=u'停止异常!'
    return HttpResponse(u"停止状态:%s"%(status))

#spider调度设置页面
def setspider(request):
    https = []

    for c in conf:
        https.append(c['http'])
    return render(request,"setspider.html",{'https':https})

#spider调度异步设置
def setspiderdata(request):

    #项目名称
    projectname = request.POST['projectname']
    #分发服务器地址
    taskhttp = request.POST['taskhttp']

    #单选框
    radio = request.POST['optionsRadiosinline']

    #单次或者每次
    try:
        one = request.POST['one']
    except:
        one = 'false'

    today = request.POST['time']

    if today =='':
        today = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

    print "projectname:%s"%projectname
    print "taskhttp:%s"%taskhttp
    print "radio:%s"%radio
    print "one:%s"%one
    print "today:%s"%today

    setspidertask.delay(projectname,taskhttp,radio,one,today)

    return HttpResponse(u"设置成功!")

#数据视图
def dataspider(request):
    keywords = []
    spiderdatas = []
    views = request.GET['view']

    conn = MySQLdb.connect(host="192.168.10.24",port=3306,user="root",passwd="root",charset="utf8")
    cur  =conn.cursor()
    cur.execute("SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE table_name = '{}' AND table_schema = 'yqapp'".format(views))
    keyword = cur.fetchall()
    cur.execute("SELECT * FROM yqapp.{} LIMIT 10".format(views))
    spiderdata = cur.fetchall()
    for k in keyword:
        keywords.append(k[0])
    for datas in spiderdata:
            spiderdatas.append(datas)
    cur.close()
    conn.close()
    return render(request,'dataspider.html',{'spiderdatas':spiderdatas,'keywords':keywords})


def spiderconfigs(request):

    return render(request,'spiderconfigs.html')