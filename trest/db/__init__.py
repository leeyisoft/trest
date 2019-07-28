#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import redis
import datetime
from decimal import Decimal

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.declarative import declarative_base

from trest.utils import utime

from .dbalchemy import Connector
from .dbalchemy import Query

from ..settings_manager import settings


MetaBaseModel = declarative_base()

class Model(MetaBaseModel):
    """
    """
    __abstract__ = True
    __tablename__ = ''
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }
    __connection_name__ = 'default'

    @declared_attr
    def Q(cls) -> Query:
        return Connector.get_conn(cls.__connection_name__).query()

    @declared_attr
    def session(cls):
        slave = Connector.get_session(cls.__connection_name__)['slave']

        slave.using_master = lambda: \
            Connector.get_session(cls.__connection_name__)['master']
        return slave


    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def as_dict(self, fields = []):
        """ 模型转换为字典 """
        items = {}
        for column in self.__table__.columns:
            val = getattr(self, column.name)
            val = '' if val is None else val
            if column.name.endswith('_at'):
                items['dt_%s'%column.name] = utime.ts_to_str(int(val), to_tz=None) if val else ''
            datetime_tuple = (datetime.datetime, datetime.date, Decimal)
            if isinstance(val, datetime_tuple):
                val = str(val)
            if type(fields)==list and len(fields)>0:
                if column.name in fields:
                    items[column.name] = val
            else :
                items[column.name] = val
        return items

#指定decode_responses为True，表示输出为字符串
_default_redis_host = '127.0.0.1'
redisdb = redis.StrictRedis(
    host = settings.redis_config.get('host', _default_redis_host),
    port = settings.redis_config.get('port', 6379),
    password = settings.redis_config.get('password', ''),
    charset = settings.redis_config.get('charset', 'utf-8'),
    db = settings.redis_config.get('db', 0),
    decode_responses=True)

def mysqldb(dbt='master'):
    sess = Connector.get_session()
    return sess.get(dbt, False)
