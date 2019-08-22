#!/usr/bin/env python
# -*- coding: utf-8  -*-
import os
import six
import inspect
import importlib
import functools

from tornado.util import import_object
from tornado.web import RequestHandler
from .utils.func import md5

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

async def get_handlers(app_name):
    """ 自动加载特定APP里面的handler """
    namespace = f'{settings.ROOT_PATH}/applications/{app_name}/handlers/'
    modules = get_modules(namespace)
    # 将包下的所有模块，逐个导入，并调用其中的函数
    package = f'applications.{app_name}.handlers'
    handlers = []
    not_get = ['post', 'delete', 'put', 'patch']
    for module in modules:
        if not module:
            continue
        if module.startswith('..'):
            continue
        try:
            module = importlib.import_module(module, package)
        except Exception as e:
            continue
        for attr in dir(module):
            if attr.startswith('_'):
                continue
            if not attr.endswith('Handler'):
                continue
            handler = getattr(module, attr)
            params = inspect.getmembers(handler, lambda f: callable(f) and hasattr(f, '_path'))
            temp_dict = {}
            for name, val in params:
                path = val._path if val._path.startswith('/') else rf'/{app_name}/{val._path}'
                method = val._method.lower()
                if path not in temp_dict.keys():
                    temp_dict[path] = {}
                temp_dict[path][method] = (path, val, name)
            # end for
            if not temp_dict:
                continue
            for (key, dt2) in temp_dict.items():
                intersection = set(not_get) & set(dt2.keys())
                if not intersection :
                    NewClass = type(f"Handler{md5(key)}", (handler,), {})
                else:
                    NewClass = handler
                # end if
                for (method2, (path2, val2, name2)) in dt2.items():
                    setattr(NewClass, method2, val2)
                handlers.append((key, NewClass,))
                print('key ', key, path2, NewClass)
            # endfor
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
            return method(*args, **kargs)
        _wrapper._path = path
        _wrapper._method = 'put'
        return _wrapper
    return wrapper

def head(*dargs, **dkargs):
    """
    """
    def wrapper(method):
        path = dargs[0]
        @functools.wraps(method)
        def _wrapper(*args, **kargs):
            return method(*args, **kargs)
        _wrapper._path = path
        _wrapper._method = 'head'
        return _wrapper
    return wrapper

def delete(*dargs, **dkargs):
    """
    """
    def wrapper(method):
        path = dargs[0]
        @functools.wraps(method)
        def _wrapper(*args, **kargs):
            return method(*args, **kargs)
        _wrapper._path = path
        _wrapper._method = 'delete'
        return _wrapper
    return wrapper
