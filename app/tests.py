# -*- coding: utf-8 -*-
#! /usr/bin/env python
from django.test import TestCase
from SpiderStarts.settings import conf
# Create your tests here.

for i in conf:
    print i['http'],i['prot'],i['name']