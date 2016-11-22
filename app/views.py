# -*- coding: utf-8 -*-
# ! /usr/bin/env python

from django.shortcuts import render
from app.tasks import setspidertask
from SpiderStarts.settings import conf
from django.http import HttpResponse
import os, time, requests, json, MySQLdb, re
from MySQLdb.cursors import DictCursor
from collections import OrderedDict


def index(request):
    listprojects = 0
    listspiders = 0
    listproject = {}
    # 获取服务器地址项目版本信息
    for i in conf:
        try:
            project = json.loads(
                requests.get("http://%s:%s/listprojects.json" % (i['http'], i['prot']), timeout=1).content)
            status = project['status']
        except:
            status = 'no'
            projects = 0
        if status == 'ok':
            projects = len(project['projects'])
            listproject[i['http']] = project['projects']
        else:
            projects = 0
        listprojects += projects

        # 获取服务器地址爬虫数信息
        if len(listproject[i['http']]) != 0:
            for j in listproject[i['http']]:
                try:
                    project = json.loads(
                        requests.get("http://%s:%s/listspiders.json?project=%s" % (i['http'], i['prot'], j),
                                     timeout=1).content)
                    status = project['status']
                except:
                    status = 'no'
                    spiders = 0
                if status == 'ok':
                    spiders = len(project['spiders'])
                else:
                    spiders = 0
                listspiders += spiders
    # 获取服务器爬虫负载均衡
    try:
        project = json.loads(requests.get("http://192.168.10.24:6800/daemonstatus.json", timeout=1).content)
        status = project['status']

    except:
        status = 'no'
        running = u"未知"
        finished = u'未知'
    if status == 'ok':
        running = len(project['running'])
        finished = len(project['finished'])
    else:
        running = u"未知"
        finished = u'未知'
    return render(request, 'index.html',
                  {'projects': listprojects, 'spiders': listspiders,
                   'running': running, 'finished': finished,})


def spiderjob(request):
    listjobs = {}
    crawlspider = {}
    cwlspider = []
    # 爬虫spiders
    for i in conf:
        try:
            project = json.loads(
                requests.get("http://%s:%s/listspiders.json?project=%s" % (i['http'], i['prot'], i['name']),
                             timeout=1).content)
            status = project['status']
        except:
            status = 'no'
            spiders = []
        if status == 'ok':
            crawlspider[i['http']] = [{'name': i['name'], 'spiders': project['spiders']}]

    # 获取爬虫详细数据
    cout = 1
    for i in conf:
        try:
            project = json.loads(
                requests.get("http://%s:%s/listjobs.json?project=%s" % (i['http'], i['prot'], i['name']),
                             timeout=1).content)
            status = project['status']
        except:
            status = 'no'
            coutpend = 0
            coutrunn = 0
            coutfinished = 0
        if status == 'ok':
            coutpend = len(project['pending'])
            pending = project['pending']
            coutrunn = len(project['running'])
            running = project['running']
            coutfinished = len(project['finished'])
            finished = project['finished']
            listjobs[i['http']] = [{'coutpend': coutpend, 'coutrunn': coutrunn, 'coutfinished': coutfinished,
                                    'pending': pending, 'running': running, 'finished': finished}]
        else:
            coutpend = 0
            coutrunn = 0
            coutfinished = 0
        # 判断字典是否有该key值
        if crawlspider.has_key(i['http']):
            for spider in crawlspider[i['http']][0]['spiders']:
                cra = cout, i['name'], spider, i['http']
                cout += 1
                cwlspider.append(list(cra))
    return render(request, 'spiderjob.html',
                  {'coutpend': coutpend,
                   'coutrunn': coutrunn,
                   'coutfinished': coutfinished,
                   'pending': pending,
                   'running': running,
                   'finished': finished,
                   'listjobs': listjobs,
                   'cwlspider': cwlspider,
                   })


# 任务状态页面
def spiderstatus(request):
    projects = {}
    pendings = []
    runnings = []
    finishes = []
    coutp = 0
    coutr = 0
    coutf = 0

    for c in conf:

        try:
            project = json.loads(
                requests.get("http://%s:%s/listjobs.json?project=%s" % (c['http'], c['prot'], c['name']),
                             timeout=1).content)

        except:
            status = 'no'
            project = {}

        if project['status'] == 'error':
            print project['status']
            error = u'服务器:%s<br>项目名为:%s<br>无法正常加载!<br>错误信息:%s<br>请检查配置文件!' % (
                c['http'], project['message'], project['node_name'])
            return render(request, 'ERROR.html', {'error': error})

        projects[c['http']] = {'finished': project['finished'], 'running': project['running'],
                               'pending': project['pending']}
        if projects.has_key(c['http']):
            for pending in projects[c['http']]['pending']:
                coutp += 1
                cra = coutp, c['http'], c['name'], pending['spider'], pending['id']
                pendings.append(list(cra))
        if projects.has_key(c['http']):
            for running in projects[c['http']]['running']:
                coutr += 1
                cra = coutr, c['http'], c['name'], running['spider'], running['id'], running['start_time']
                runnings.append(list(cra))
        if projects.has_key(c['http']):
            for finished in projects[c['http']]['finished']:
                coutf += 1
                cra = coutf, c['http'], c['name'], finished['spider'], finished['id'], finished['start_time'], finished[
                    'end_time']
                finishes.insert(0, list(cra))
    return render(request, 'spiderstatus.html', {'pendings': pendings, 'runnings': runnings, 'finishes': finishes})


# 根据指定参数运行指定爬虫并返回任务状态
def runspider(request):
    run = request.GET['runspider']
    runstart = json.loads(os.popen("curl %s" % run, 'r').read())
    status = runstart['status']
    jobid = runstart['jobid']
    if status == 'ok':
        status = u'已启动'
    return HttpResponse(u"启动状态:%s!<br>任务ID:%s" % (status, jobid))


# 管理指定参数停止指定爬虫并返回状态
def stopspider(request):
    stop = request.GET['stopspider']
    stopcrawl = json.loads(os.popen("curl %s" % (stop), 'r').read())
    status = stopcrawl['status']
    if status == 'ok':
        status = u'已停止!'
    else:
        status = u'停止异常!'
    return HttpResponse(u"停止状态:%s" % (status))


# spider调度设置页面
def setspider(request):
    https = []

    for c in conf:
        https.append(c['http'])
    return render(request, "setspider.html", {'https': https})


# spider调度异步设置
def setspiderdata(request):
    # 项目名称
    projectname = request.POST['projectname']
    # 分发服务器地址
    taskhttp = request.POST['taskhttp']

    # 单选框
    radio = request.POST['optionsRadiosinline']

    # 单次或者每次
    try:
        one = request.POST['one']
    except:
        one = 'false'

    today = request.POST['time']

    if today == '':
        today = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    print "projectname:%s" % projectname
    print "taskhttp:%s" % taskhttp
    print "radio:%s" % radio
    print "one:%s" % one
    print "today:%s" % today

    setspidertask.delay(projectname, taskhttp, radio, one, today)

    return HttpResponse(u"设置成功!")


# 数据视图
def dataspider(request):
    # views = request.GET['view']
    conn = MySQLdb.connect(host="192.168.10.24", port=3306, user="root", passwd="root", charset="utf8",
                           cursorclass=DictCursor)
    cur = conn.cursor()
    # 根据表明查字段
    # cur.execute(
    #     "SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE table_name = '{}' AND table_schema = 'yqapp'".format(
    #         views))
    # cur.execute(
    #     "SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE table_name = 'zbxx' AND table_schema = 'yqapp'")
    # keyword = cur.fetchall()
    # cur.execute("SELECT * FROM yqapp.{} LIMIT 10".format(views))
    cur.execute("SELECT * FROM yqapp.zbxx LIMIT 10")
    spiderdatas = cur.fetchall()
    # print spiderdata
    # for k in keyword:
    #     keywords.append(k[0])
    # for datas in spiderdata:
    #     spiderdatas.append(datas)
    cur.close()
    conn.close()
    return render(request, 'dataspider.html', {'spiderdatas': spiderdatas})


# 配置文件设置
def spiderconfigs(request):
    return render(request, 'spiderconfigs.html')


# 配置文件存储在到mysql库
def configstomysql(request):
    # 获取配置文件内容数据
    configs = request.POST

    conn = MySQLdb.connect(host="192.168.10.24", port=3306, user="root", passwd="root", charset="utf8")
    cur = conn.cursor()

    # 写入mysql数据库
    try:
        cur.execute(
            "INSERT INTO yqapp.configs(spidername,domain,spidertype,site,listurl,listxpath,pagexpath) \
    VALUES ('%s','%s','%s','%s','%s','%s','%s')" \
            % (configs['spidername'], configs['domain'], configs['spidertype'], configs['site'], configs['listurl'],
               configs['listxpath'], configs['pagexpath'],))
        conn.commit()

    except:
        return HttpResponse(u"已存在'%s'为名称的配置文件" % (configs['spidername']))
    # 格式化内容规则字段
    keys = configs.keys()
    f = re.findall(r'field\d+', str(keys))
    for i in xrange(len(f)):
        if configs['field%s' % i] == '' or configs['xpath%s' % i] == '':
            continue
        cur.execute(
            "UPDATE yqapp.configs SET %s='%s' WHERE spidername='%s'" % (
                configs['field%s' % i], configs['xpath%s' % i], configs['spidername']))
        conn.commit()

    cur.close()
    conn.close()
    return HttpResponse(u"提交成功!")


# 配置文件展示
def configfile(request):
    # cursorclass参数查询返回字典格式
    conn = MySQLdb.connect(host="192.168.10.24", port=3306, user="root", passwd="root", charset="utf8",
                           cursorclass=DictCursor)
    cur = conn.cursor()
    cur.execute("SELECT spidername,site,spidertype,listurl FROM yqapp.configs")
    keyword = cur.fetchall()
    cur.close()
    conn.close()
    keywords = list(keyword)
    return render(request, 'configfile.html', {'keywords': keywords})


def servercpu(request):
    return render(request, 'servercpu.html')


def serverSQL(request):
    return render(request, 'serverSQL.html')


def servernetwork(request):
    return render(request, 'servernetwork.html')


def dataspidertest(request):
    conn = MySQLdb.connect(host="192.168.10.24", port=3306, user="root", passwd="root", charset="utf8",
                           cursorclass=DictCursor)
    cur = conn.cursor()
    cur.execute("SELECT url,name as '标题',author as '来源',pubtime as '发布时间',zbtype as '采集类型',zbje as '中标金额',\
diqu as '地区',content as '内容' FROM yqapp.zbxx_gy WHERE name LIKE '%贵阳%' GROUP BY pubtime DESC LIMIT 20 ")
    spiderdatas = cur.fetchall()
    cur.close()
    conn.close()
    return render(request, 'dataspider.html', {'spiderdatas': spiderdatas})


def datanews(request):
    conn = MySQLdb.connect(host="192.168.10.24", port=3306, user="root", passwd="root", charset="utf8",
                           cursorclass=DictCursor)
    cur = conn.cursor()
    cur.execute(
        "SELECT url,title as '标题',pubtime as '发布时间',content as '内容' FROM yqapp.news GROUP BY pubtime DESC LIMIT 20 ")
    spiderdatas = cur.fetchall()
    cur.close()
    conn.close()
    return render(request, 'dataspider.html', {'spiderdatas': spiderdatas})


def datajob(request):
    conn = MySQLdb.connect(host="192.168.10.24", port=3306, user="root", passwd="root", charset="utf8",
                           cursorclass=DictCursor)
    cur = conn.cursor()
    cur.execute("SELECT url,name as '公司名称', jobname as '职位名称', pay as '薪资',didian as '地点',\
 number as '招聘人数',pubtime as '发布时间' FROM yqapp.zhaopin GROUP BY pubtime DESC LIMIT 20 ")
    spiderdatas = cur.fetchall()
    cur.close()
    conn.close()
    return render(request, 'dataspider.html', {'spiderdatas': spiderdatas})


def datazbxx(request):
    conn = MySQLdb.connect(host="192.168.10.24", port=3306, user="root", passwd="root", charset="utf8",
                           cursorclass=DictCursor)
    cur = conn.cursor()
    cur.execute("SELECT XB_URL AS 'url',XB_TITLE AS '标题',XB_PM AS '品目',XB_XMLXR AS '项目联系人',XB_XMLXDH AS '项目联系人电话',\
XB_CGDW AS '采购单位',XB_CGDWDZ AS '采购单位地址', XB_CGDWLXFS AS '采购单位联系方式',\
XB_ZBRQ AS '中标日期',XB_ZBJE AS '中标金额',XB_KBSJ AS '开标时间',XB_CONTENT AS '内容',XB_REGION AS '地区' FROM xbzx.zhaobiao_xy_bak GROUP BY XB_PUBTIME DESC LIMIT 20 ")
    spiderdatas = cur.fetchall()
    cur.close()
    conn.close()
    return render(request, 'dataspider.html', {'spiderdatas': spiderdatas})
