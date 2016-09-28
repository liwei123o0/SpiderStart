# -*- coding: utf-8 -*-
#! /usr/bin/env python
import os

#实现统计代码行
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