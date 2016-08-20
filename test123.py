# -*- coding: utf-8 -*-
#! /usr/bin/env python
from SpiderStarts.settings import conf

crawlspider = {'192.168.10.24': [{'name': 'spider123', 'spiders': [u'ccgpz', u'ccgpz_big', u'ccgpz_gg', u'ccgpz_xy']}]}

for c in conf:
    if crawlspider.has_key(c['http']):
        cout = 1
        for spider in  crawlspider[c['http']][0]['spiders']:
            cra = cout,c['name'],spider,c['http']
            print cra
            cout+=1
