#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado.util import import_object

from ..settings_manager import settings
from .file import FileUtil
from .file import Uploader
from .object import RWLock

from ..db import redisdb
from ..db import mysqldb


def sys_config(key, field='value'):
    cache_key = '%s%s' % (settings.config_cache_prefix,key)
    cache_val = redisdb.get(cache_key)
    # print('cache_key', cache_key)
    if field=='delete_key_value':
        return redisdb.delete(cache_key)
    if cache_val:
        # print('cache_val: ', cache_val)
        return cache_val

    db = mysqldb()
    value = ''
    try:
        if field=='value':
            query = "select `value` from `sys_config` where `status`=1 and `key`='%s';" % key;
            value = db.execute(query).scalar()
            value = value if value is not None else ''
        elif type(field)==list:
            query = "select %s from `sys_config` where `status`=1 and `key`='%s';" % (','.join(field),key);
            # print('field', type(field), field)
            field = db.execute(query).fetchone()
            # print('field', type(field), field)
            value = dict(field)
        # endif
    except Exception as e:
        raise e
    finally:
        # 释放连接池
        db.remove()
    redisdb.set(cache_key, value, 86400)
    return value
