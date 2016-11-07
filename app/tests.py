# -*- coding: utf-8 -*-
# ! /usr/bin/env python
import os


# 实现统计代码行
def browseFiles(path):
    count = 0
    files = os.listdir(path)
    for item in files:
        if os.path.isfile(path + '\\' + item):
            count += countLines(path + '\\' + item)
        else:
            count += browseFiles(path + '\\' + item)
    return count


def countLines(path):
    if path.find('.cs') == -1:
        return 0
    if path.find('.Designer.cs') > -1:
        return 0
    lineNum = 0
    f = open(path, 'r')
    for count, line in enumerate(f):
        lineNum += 1
    f.close()
    return lineNum


# print browseFiles(r"E:\SpiderStarts")

# conf = {1: (u'baidu', u'\u767e\u5ea6\u65b0\u95fb', u'\u65b0\u95fb', u'http://www.baidu.com'),
#         2: (u'baidu', u'\u767e\u5ea6\u65b0\u95fb', u'\u65b0\u95fb', u'http://www.baidu.com')}
# for i in conf.items():
#     for j in i:
#         print j
import MySQLdb
from MySQLdb.cursors import DictCursor

conn = MySQLdb.connect(host="192.168.10.24", port=3306, user="root", passwd="root", charset="utf8",
                       cursorclass=DictCursor)
cur = conn.cursor()
# cur.execute(
#     "SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE table_name = '{}' AND table_schema = 'yqapp'".format(
#         views))
cur.execute(
    "SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE table_name = 'zbxx' AND table_schema = 'yqapp'")
keyword = cur.fetchall()
# cur.execute("SELECT * FROM yqapp.{} LIMIT 10".format(views))
cur.execute("SELECT * FROM yqapp.zbxx LIMIT 2")
spiderdata = cur.fetchall()
for s in spiderdata:
    for k, v in s.items():
        print "%s:%s" % (k, v)
# print spiderdata
# for k in keyword:
#     keywords.append(k[0])
# for datas in spiderdata:
#     spiderdatas.append(datas)
cur.close()
conn.close()
