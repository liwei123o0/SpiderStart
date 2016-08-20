# -*- coding: utf-8 -*-
#! /usr/bin/env python

aa = {'192.168.10.24': [{'name': 'spider123', 'spiders': [u'ccgpz', u'ccgpz_big', u'ccgpz_gg', u'ccgpz_xy']}]}

b =  aa.values()[0]

print  b[0]['spiders']
# print aa[aa.keys()[0]]['spiders']

for i in crawlspider.values()[0][0]['spiders']:
    print i,aa.values()[0][0]['name'],'192.168.10.24'