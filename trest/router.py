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
from .handler import Handler


def _get_modules(package="."):
    """
    获取包名下所有非__init__的模块名
    """
    modules = []
    files = os.listdir(package)
    for file in files:
        if file.startswith('_') or file.startswith('.'):
            continue
        if not file.endswith('.py'):
            continue
        name, ext = os.path.splitext(file)
        if name in ['common',]:
            continue
        modules.append('.' + name)
    return modules

def _get_handler_params(module, attr):
    """
    获取module下面的所有参数
    """
    if attr.startswith('_'):
        return (False, False)
    if not attr.endswith('Handler'):
        return (False, False)
    if attr in ['Handler', 'CommonHandler']:
        return (False, False)
    handler = getattr(module, attr)
    params = inspect.getmembers(handler, lambda f: callable(f) and hasattr(f, '_path'))
    if not params:
        return (False, False)
    return (handler, params)

def _get_path_method(app_name, params):
    """
    给参数按照path/method分组api，便于 _create_handlers/3创建class
    """
    path_method_dict = {}
    method_path_set = set()
    for name, val in params:
        path = val._path if val._path.startswith('/') else rf'/{app_name}/{val._path}'
        method = val._method.lower()
        if path not in path_method_dict.keys():
            path_method_dict[path] = {}
        method_path = f'{method}:{path}'
        if method_path in method_path_set:
            raise Exception(f'api repeated {method_path}')
        path_method_dict[path][method] = (path, val, name)
        method_path_set.add(method_path)
    return path_method_dict

def _create_handlers(handler, package, path_method_dict):
    handlers = []
    not_get = ['post', 'delete', 'put', 'patch']
    for (path, dt2) in path_method_dict.items():
        intersection = set(not_get) & set(dt2.keys())
        if not intersection :
            classname = f'Handler{md5(path)}'
            new_class = type(classname, (handler,), {})
            new_class.__module__ = package
        else:
            new_class = handler
        # end if
        for (method2, (path2, val2, name2)) in dt2.items():
            setattr(new_class, method2, val2)
        handlers.append((path, new_class, {'name':name2}))
    return handlers

def get_handlers(app_name):
    """ 自动加载特定APP里面的handler """
    namespace = f'{settings.ROOT_PATH}/applications/{app_name}/handlers/'
    modules = _get_modules(namespace)
    # 将包下的所有模块，逐个导入，并调用其中的函数
    package = f'applications.{app_name}.handlers'
    handlers = []
    for module in modules:
        try:
            module = importlib.import_module(module, package)
        except Exception as e:
            raise e
        for attr in dir(module):
            (handler, params) = _get_handler_params(module, attr)
            if not params:
                continue
            path_method_dict = _get_path_method(app_name, params)
            handlers += _create_handlers(handler, package, path_method_dict)
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
