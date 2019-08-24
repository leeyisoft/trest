#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""广告位控制器

[description]
"""
from trest.exception import JsonError
from trest.router import delete
from trest.router import post
from trest.router import get
from trest.router import put
from trest.handler import BaseHandler


class DemoHandler(BaseHandler):
    @post('demo0')
    def add(self):
        return self.success(data = ['post', 'demo0'])

class Demo1Handler(BaseHandler):
    @post('demo1')
    def add(self):
        return self.success(data = ['post', 'demo1'])

class Demo2Handler(BaseHandler):
    @get('demo2')
    def get_demo2(self):
        return self.success(data = ['get', 'demo2', ])

    @get('demo2')
    def get_demo2(self):
        return self.success(data = ['get', 'demo23', ])

    @delete('demo3/(?P<id>\d*)')
    def del_demo3(self, id):
        return self.success(data = ['delete', 'demo3', id])

    @delete('demo2/(?P<id>\d*)')
    def del_demo2(self, id):
        return self.success(data = ['delete', 'demo2', id])
