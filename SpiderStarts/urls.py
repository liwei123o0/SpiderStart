# -*- coding: utf-8 -*-
# ! /usr/bin/env python
"""SpiderStarts URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # 登陆
    url(r'^login/', Login),
    url(r'^login_view/', Login_View),
    # 爬虫管理页面连接
    url(r'^$', index),
    url(r'^spiderjob/', spiderjob),
    url(r'^spiderstatus/', spiderstatus),
    url(r'^runspider/', runspider),
    url(r'^stopspider/', stopspider),
    url(r'^setspider/', setspider),
    url(r'^setspiderdata/', setspiderdata),
    url(r'^dataspider/', dataspider),
    url(r'^dataspidertest/', dataspidertest),
    url(r'^datanews/', datanews),
    url(r'^datajob/', datajob),
    url(r'^datazbxx/', datazbxx),
    # 爬虫规则管理连接
    url(r'^spiderconfigs/', spiderconfigs),
    url(r'^configstomysql/', configstomysql),
    url(r'^configfile/', configfile),
    url(r'^servercpu/', servercpu),
    url(r'^serversql/', serverSQL),
    url(r'^servernetwork/', servernetwork),

]
