#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import configparser
from tornado.options import options
from .storage import storage
from .exception import ConfigError


# 检查全局变量 ROOT_PATH 设置
if hasattr(options, 'ROOT_PATH') and os.path.exists(options.ROOT_PATH):
    ROOT_PATH = options.ROOT_PATH
else:
    raise ConfigError('ROOT_PATH is not configured')

_dotenv = f'{ROOT_PATH}/.env'
dcfg = configparser.ConfigParser()
dcfg.read(_dotenv, encoding='utf8')

env = dcfg.get('sys','TREST_ENV')
# 检查系统环境变量 TREST_ENV 设置
if env not in ['local', 'dev', 'test', 'product']:
    msg = f'The system variable TREST_ENV ({env}) is not one of the local, dev, test, or product'
    raise ConfigError(msg)

class ConfigParser(configparser.ConfigParser):
    def as_dict(self):
        """
        将 configparser.ConfigParser().read() 读到的数据转换为 storage
        """
        d = storage(self._sections)
        for k in d:
            d[k] = storage(d[k])
        return d

cfg = ConfigParser()
_ini = f'{ROOT_PATH}/configs/{env}.ini'
if not(os.path.isfile(_ini) and os.access(_ini, os.R_OK)):
    raise ConfigError(f'The ENV file({_ini}) does not exist or is unreadable')
cfg.read(_ini, encoding='utf8')

settings = cfg.as_dict()
settings.ROOT_PATH = ROOT_PATH
settings.STATIC_PATH = os.path.join(ROOT_PATH, 'statics')
settings.ENV = env
settings.debug = cfg.getboolean('tornado', 'debug')
settings.xheaders = cfg.getboolean('tornado', 'xheaders')
settings.xsrf_cookies = cfg.getboolean('tornado', 'xsrf_cookies')

_app = cfg.get('sys', 'installed_app')
settings.INSTALLED_APPS = [n.strip() for n in _app.split(',') if n]

# Super Admin 必须是 int 型数据
settings.SUPER_ADMIN = [
    1, # admin uid
    2, #
]
# 超级管理员角色ID
settings.SUPER_ROLE_ID = 1
settings.DEFAULT_ROLE_ID = 2
# 系统角色，非超级管理员不允许编辑权限和删除
settings.SYS_ROLE = [
    settings.SUPER_ROLE_ID,
    settings.DEFAULT_ROLE_ID
]

# 是否开启国际化
settings.translation = cfg.getboolean('sys', 'translation')
settings.TRANSLATIONS_CONF = storage({
    'translations_dir': os.path.join(ROOT_PATH, 'datas/locales'),
    'locale_default': 'zh_CN',
    'use_accept_language': True
})

# tornado全局配置
settings.TORNADO_CONF = {
    'xsrf_cookies': settings.xsrf_cookies,
    'login_url': '/admin/login',
    'cookie_secret': cfg.get('tornado', 'cookie_secret'),
    # 'ui_modules': ui_modules,
    'template_path': os.path.join(ROOT_PATH, 'applications/admin/templates'),
    'static_path': settings.STATIC_PATH,
    # 安全起见，可以定期生成新的cookie 秘钥，生成方法：
    # base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
}

# 中间件     #
# ###########
settings.MIDDLEWARE_CLASSES = (
    'trest.middleware.dbalchemy.DBAlchemyMiddleware',
    'trest.middleware.AccessLogMiddleware',
    'trest.middleware.PushToMQMiddleware',
)

# 数据库连接字符串，
# 元祖，每组为n个数据库连接，有且只有一个master，可配与不配slave
settings.DATABASE_CONNECTION = {
    'default': {
        'connections': [
            {
                'ROLE': 'master',
                'DRIVER': cfg.get('db_master', 'driver'),
                'UID': cfg.get('db_master', 'user'),
                # 进过AES加密的密码，格式 aes::: + ciphertext
                'PASSWD': cfg.get('db_master', 'password'),
                'HOST': cfg.get('db_master', 'host'),
                'PORT': cfg.getint('db_master', 'port'),
                'DATABASE': cfg.get('db_master', 'database'),
                'QUERY': {'charset': cfg.get('db_master', 'charset')}
            },
            {
                'ROLE': 'slave',
                'DRIVER': cfg.get('db_slave', 'driver'),
                'UID': cfg.get('db_slave', 'user'),
                # 进过AES加密的密码，格式 aes::: + ciphertext
                'PASSWD': cfg.get('db_slave', 'password'),
                'HOST': cfg.get('db_slave', 'host'),
                'PORT': cfg.getint('db_slave', 'port'),
                'DATABASE': cfg.get('db_slave', 'database'),
                'QUERY': {'charset': cfg.get('db_slave', 'charset')}
            }
        ]
    }
}

# sqlalchemy配置，列出部分，可自行根据sqlalchemy文档增加配置项
# 该配置项对所有连接全局共享
settings.SQLALCHEMY_CONFIGURATION = {
    'sqlalchemy.connect_args': {
        'connect_timeout': cfg.getint('sqlalchemy', 'connect_timeout')
    },
    'sqlalchemy.echo': cfg.getboolean('sqlalchemy', 'echo'),
    'sqlalchemy.max_overflow': cfg.getint('sqlalchemy', 'max_overflow'),
    'sqlalchemy.echo_pool': cfg.getboolean('sqlalchemy', 'echo_pool'),
    'sqlalchemy.pool_timeout': cfg.getint('sqlalchemy', 'pool_timeout'),
    'sqlalchemy.encoding': cfg.get('sqlalchemy', 'encoding'),
    'sqlalchemy.pool_size': cfg.getint('sqlalchemy', 'pool_size'),
    'sqlalchemy.pool_recycle': cfg.getint('sqlalchemy', 'pool_recycle'),
    # 手动指定连接池类
    'sqlalchemy.poolclass': cfg.get('sqlalchemy', 'poolclass'),
}

###########
# 缓存配置 #
###########
settings.CACHES = {
    'default': {
        'BACKEND': 'trest.cache.backends.localcache.LocMemCache',
        'LOCATION': 'process_cache',
        'OPTIONS': {
            'MAX_ENTRIES': 10000,
            'CULL_FREQUENCY': 3
        }
    },
    'default_redis': {
        'BACKEND': 'trest.cache.backends.rediscache.RedisCache',
        'LOCATION': cfg.get('default_redis', 'location'),
        'OPTIONS': {
            'DB': cfg.getint('default_redis', 'db'),
            'PASSWORD': cfg.get('default_redis', 'password'),
            'PARSER_CLASS': cfg.get('default_redis', 'parser_class'),
            'POOL_KWARGS': {
                'socket_timeout': cfg.getint('default_redis', 'socket_timeout'),
                'socket_connect_timeout': cfg.getint('default_redis', 'socket_connect_timeout')
            },
            # 定时ping redis连接池，防止被服务端断开连接（s秒）
            'PING_INTERVAL': cfg.getint('default_redis', 'ping_interval')
        }
    },
}

settings.PASSWORD_HASHERS = [
    # 第一个元素为默认加密方式
    'trest.utils.hasher.PBKDF2PasswordHasher',
    'trest.utils.hasher.PBKDF2SHA1PasswordHasher',
]

#配置模版引擎
#引入相应的TemplateLoader即可
#若使用自带的请给予None
#支持mako和jinja2
#mako设置为tornado.template.mako_loader.MakoTemplateLoader
#jinj2设置为tornado.template.jinja2_loader.Jinja2TemplateLoader
#初始化参数请参照jinja的Environment或mako的TemplateLookup,不再详细给出
settings.TEMPLATE_CONFIG = storage({
    'template_engine': None,
    #模版路径由tornado.handler中commonhandler重写，无需指定，模版将存在于每个应用的根目录下
    'filesystem_checks': True,  #通用选项
    'cache_directory': '../_tmpl_cache',  #模版编译文件目录,通用选项
    'collection_size': 50,  #暂存入内存的模版项，可以提高性能，mako选项,详情见mako文档
    'cache_size': 0,  #类似于mako的collection_size，设定为-1为不清理缓存，0则每次都会重编译模板
    'format_exceptions': False,  #格式化异常输出，mako专用
    'autoescape': False  #默认转义设定，jinja2专用
})

# tornado日志功能配置
# Logging中有
# NOTSET < DEBUG < INFO < WARNING < ERROR < CRITICAL 这几种级别，
# 日志会记录设置级别以上的日志
# when  时间  按照哪种时间单位滚动（可选s-按秒，m-按分钟，h-按小时，d-按天，w0-w6-按指定的星期几，midnight-在午夜）
settings.LOGGING_DIR = os.path.join(ROOT_PATH, 'logs/')

#其中name为getlogger指定的名字
settings.standard_format = '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]' \
                  '[%(levelname)s][%(message)s]'
settings.LOGGING = (
    {
        'name': 'access_log',
        'log_to_stderr': True,
        'filename': 'access_log.log'
    },
    {
        'name': 'tornado.debug.log',
        'level': 'DEBUG',
        'log_to_stderr': True,
        'when': 'w0',
        'interval': 1,
        'formatter': settings.standard_format,
        'filename': 'debug_log.log'
    },
    {
        'name': 'tornado.info.log',
        'level': 'INFO',
        'log_to_stderr': True,
        'when': 'midnight',
        'interval': 1,
        'formatter': settings.standard_format,
        'filename': 'info_log.log'
    },
    {
        'name': 'tornado.warning.log',
        'level': 'WARNING',
        'log_to_stderr': True,
        'when': 'midnight',
        'interval': 1,
        'formatter': settings.standard_format,
        'filename': 'warning_log.log'
    },
    {
        'name': 'tornado.error.log',
        'level': 'ERROR',
        'log_to_stderr': True,
        'when': 'midnight',
        'interval': 1,
        'formatter': settings.standard_format,
        'filename': 'error_log.log'
    },
    {
        'name': 'tornado.critical.log',
        'level': 'CRITICAL',
        'log_to_stderr': True,
        'when': 'midnight',
        'interval': 1,
        'formatter': settings.standard_format,
        'filename': 'critical_log.log'
    },
)
