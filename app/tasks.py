# -*- coding: utf-8 -*-
#! /usr/bin/env python

from celery import task

@task
def add(x,y):

    return x+y