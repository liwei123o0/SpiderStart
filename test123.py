# -*- coding: utf-8 -*-
#! /usr/bin/env python
from SpiderStarts.settings import conf

import requests
import json

project = json.loads(
    requests.get("http://192.168.10.25:6800/listjobs.json?project=app").content
)
print project['status']