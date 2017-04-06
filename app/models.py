# -*- coding: utf-8 -*-
# ! /usr/bin/env python

from django.db import models
from django.contrib import admin
# 兼容python2.x和python3.x
from django.utils.encoding import python_2_unicode_compatible


# Create your models here.
# 同步数据库命令
# python manage.py makemigrations
# python manage.py migrate

# @python_2_unicode_compatible
class Login(models.Model):
    username = models.CharField(u'用户名', max_length=50)
    password = models.CharField(u'密码', max_length=50)
    part = models.CharField(u'用户权限', max_length=50)

    def __unicode__(self):  # 在Python3中用 __str__ 代替 __unicode__
        return self.username


class LoginAdmin(admin.ModelAdmin):
    list_display = ('username', 'password', 'part')

admin.site.register(Login, LoginAdmin)
