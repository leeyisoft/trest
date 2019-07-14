#!/usr/bin/env python
# -*- coding: utf-8  -*-
import os
import six
import inspect
import importlib
import functools

from tornado.util import import_object
from tornado.web import RequestHandler

from .exception import JsonError
from .utils.encrypter import RSAEncrypter
from .settings_manager import settings
from .handler import BaseHandler


def get_modules(package="."):
    """
    获取包名下所有非__init__的模块名
    """
    modules = []
    files = os.listdir(package)
    for file in files:
        if not file.startswith('_'):
            name, ext = os.path.splitext(file)
            modules.append('.' + name)
    # endfor
    return modules

def get_handlers(app_name):
    namespace = f'{settings.ROOT_PATH}/applications/{app_name}/handlers/'
    # print(namespace)
    modules = get_modules(namespace)
    # print('modules ', type(modules), modules)
    # 将包下的所有模块，逐个导入，并调用其中的函数
    package = f'applications.{app_name}.handlers'
    handlers = []
    for module in modules:
        if not module:
            continue
        if module.startswith('..'):
            continue
        # print('module ', type(module), module)
        try:
            module = importlib.import_module(module, package)
            # print('module2 ', type(module), module)
        except Exception as e:
            # print('e ', type(e), e)
            # pass
            continue
        # print('module ', type(module), module)
        data = []
        for attr in dir(module):
            if attr.startswith('_'):
                continue
            if not attr.endswith('Handler'):
                continue

            hander = getattr(module, attr)
            # func_list = []
            # print(dir(hander))
            for name, val in inspect.getmembers(hander, lambda f: callable(f) and hasattr(f, '_path')):
                path = val._path if val._path.startswith('/') else rf'/{app_name}/{val._path}'
                method = val._method.lower()
                # print('----------------------------------------------------------------------------')
                # print('hander', type(hander), hander)
                # print('name', type(name), name)
                # print('path', type(path), path)
                # print('val', val._path, type(val), val, dir(val))
                # print("\n\n")
                NewClass = type(name, (hander,), {})
                setattr(NewClass, method, val)
                handlers.append((path, NewClass))
        # endfor
    # endfor
    return handlers

def get(*dargs, **dkargs):
    """
    """
    def wrapper(method):
        path = dargs[0]
        @functools.wraps(method)
        def _wrapper(*args, **kargs):
            # path = dargs[0]
            # self = args[0]
            # print('path ', type(path), path)
            # print('method ', type(method), method)
            # print('rest/get', type(self), self)
            # print("\n\n\n")
            return method(*args, **kargs)
        _wrapper._path = path
        _wrapper._method = 'get'
        return _wrapper
    return wrapper

def post(*dargs, **dkargs):
    """
    """
    def wrapper(method):
        path = dargs[0]
        @functools.wraps(method)
        def _wrapper(*args, **kargs):
            # path = dargs[0]
            # self = args[0]
            # print('rest/post', type(self), self)
            return method(*args, **kargs)
        _wrapper._path = path
        _wrapper._method = 'post'
        return _wrapper
    return wrapper

def put(*dargs, **dkargs):
    """
    """
    def wrapper(method):
        path = dargs[0]
        @functools.wraps(method)
        def _wrapper(*args, **kargs):
            # path = dargs[0]
            # self = args[0]
            # print('rest/put', type(self), self)
            return method(*args, **kargs)
        _wrapper._path = path
        _wrapper._method = 'put'
        return _wrapper
    return wrapper

def delete(*dargs, **dkargs):
    """
    """
    def wrapper(method):
        path = dargs[0]
        @functools.wraps(method)
        def _wrapper(*args, **kargs):
            # path = dargs[0]
            # self = args[0]
            # print('rest/delete', type(self), self)
            return method(*args, **kargs)
        _wrapper._path = path
        _wrapper._method = 'delete'
        return _wrapper
    return wrapper
