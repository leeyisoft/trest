#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from .exception import ConfigError
from tornado.options import options


debug = False
cookie_secret = 'e921bfcd-ace4-4124-8657-c57a162365f6'
xsrf_cookies = False

login_pwd_rsa_encrypt = True
default_aes_secret = '883d65f06fd447f3a1e69a36e73f58e0'

valid_code_key = 'ab1195c6f0084b4f8b007d3aa7628a38'
token_key = 'f30a2331813f46d0adc2bcf26fcbbbf4'

admin_session_key = 'de0b3fb0c2f44563944a8cccca7f225a'
front_session_key = '171630947de24c969c28b2d178c4e0fe'

jwt_key = ''

oss_config = {
    'accesskeyid':'',
    'accesskey':'',
    'endpoint':'',
    'bucket_name':'',
}
# 163邮箱信息
email = {
    'smtp_sever': 'smtp.163.com',
    'smtp_port': 25,
    'from_name': 'LeeyiSoft',
    'from_addr': 'leeyisoft@163.com',
    # 授权码
    'auth_code': '',
}

sentry_url = ''
rabbitmq_config = ''
redis_config = {}
# ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if hasattr(options, 'ROOT_PATH') and os.path.exists(options.ROOT_PATH):
    ROOT_PATH = options.ROOT_PATH
else:
    raise ConfigError('请配置 ROOT_PATH')

STATIC_PATH = os.path.join(ROOT_PATH, 'statics')
TEMPLATE_PATH = os.path.join(ROOT_PATH, 'applications/admin/templates')

xheaders = True

# Super Admin 必须是 int 型数据
SUPER_ADMIN = [
    1, # admin uid
    2, #
]
# 超级管理员角色ID
# 必须是 int 型数据
SUPER_ROLE_ID = 1
# 必须是 int 型数据
DEFAULT_ROLE_ID = 2

# 系统角色，非超级管理员不允许编辑权限和删除
SYS_ROLE = [
    SUPER_ROLE_ID,
    DEFAULT_ROLE_ID,
]

# tornado全局配置
TORNADO_CONF = {
    'xsrf_cookies': xsrf_cookies,
    'login_url': '/admin/login',
    'cookie_secret': cookie_secret,
    # 'ui_modules': ui_modules,
    'template_path': TEMPLATE_PATH,
    'static_path': STATIC_PATH,
    # 安全起见，可以定期生成新的cookie 秘钥，生成方法：
    # base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
}

# ###########
# 中间件     #
# ###########
MIDDLEWARE_CLASSES = (
    'trest.middleware.dbalchemy.DBAlchemyMiddleware',
    'trest.middleware.AccessLogMiddleware',
    'trest.middleware.PeriodicCallbackMiddleware',
    'trest.middleware.PushToMQMiddleware',
    # 'tornado.httpmodule.httpmodule.HttpModuleMiddleware',
)

# 定时任务之定期调用，执行定时任务需要首先加载 middleware.PeriodicCallbackMiddleware
CRONTAB_PeriodicCallback = [
    # (
    #     'trest.models.PeriodicCallbackDemo',
    #     'demo_test',
    #     # 参数必须是一个 dict
    #     {'user_id': ''},
    #     # 每隔 1800000 毫秒(30分钟)执行一次
    #     1800000,
    # ),
]

INSTALLED_APPS = (
    'admin',
)
# 全局modules配置
COMMON_MODULES = (
    # 'module限定名',
)
# 路由modules，针对某个路由或某些路由起作用
ROUTE_MODULES = {
    # {'路由名称或正则':['module限定名','!被排除的module限定名']}
}
###########
# 缓存配置 #
###########
CACHES = {
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
        'LOCATION': '127.0.0.1:6379',
        'OPTIONS': {
            'DB': 3,
            'PASSWORD': 'abc123456',
            'PARSER_CLASS': 'redis.connection.DefaultParser',
            'POOL_KWARGS': {
                'socket_timeout': 2,
                'socket_connect_timeout': 2
            },
            'PING_INTERVAL': 120  # 定时ping redis连接池，防止被服务端断开连接（s秒）
        }
    },

}
config_cache_prefix = 'conf:'
user_cache_prefix = 'user:'
admin_cache_prefix = 'admin:'

IPV4_ONLY = True

#开启session支持
SESSION = {
    'session_cache_alias': 'default_redis',  #'session_loccache',对应cache配置
    'session_name': 'nkzpg9NKBpKS2iaK',
    'cookie_domain': '',
    'cookie_path': '/',
    'expires': 86400,  # 24 * 60 * 60, # 24 hours in seconds,0代表浏览器会话过期
    'ignore_change_ip': False,
    'httponly': True,
    'secret_key': 'fLjUfxqXtfNoIldA0A0J',
    'session_version': 'v0.1.0'
}

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

#################
# 本地化翻译文件地址#
#################
TRANSLATIONS = True  # 是否开启国际化
TRANSLATIONS_CONF = {
    'translations_dir': os.path.join(ROOT_PATH, 'datas/locales'),
    'locale_default': 'zh_CN',
    'use_accept_language': True
}

# 白名单未开启，如需使用，请用元祖列出白名单ip
WHITELIST = False
#######
# WHITELIST = (
#     '127.0.0.1',
# '127.0.0.2',
# )

# tornado日志功能配置
# Logging中有
# NOTSET < DEBUG < INFO < WARNING < ERROR < CRITICAL 这几种级别，
# 日志会记录设置级别以上的日志
# when  时间  按照哪种时间单位滚动（可选s-按秒，m-按分钟，h-按小时，d-按天，w0-w6-按指定的星期几，midnight-在午夜）
LOGGING_DIR = 'logs/'

#其中name为getlogger指定的名字
standard_format = '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]' \
                  '[%(levelname)s][%(message)s]'
LOGGING = (
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
        'formatter': standard_format,
        'filename': 'debug_log.log'
    },
    {
        'name': 'tornado.info.log',
        'level': 'INFO',
        'log_to_stderr': True,
        'when': 'midnight',
        'interval': 1,
        'formatter': standard_format,
        'filename': 'info_log.log'
    },
    {
        'name': 'tornado.warning.log',
        'level': 'WARNING',
        'log_to_stderr': True,
        'when': 'midnight',
        'interval': 1,
        'formatter': standard_format,
        'filename': 'warning_log.log'
    },
    {
        'name': 'tornado.error.log',
        'level': 'ERROR',
        'log_to_stderr': True,
        'when': 'midnight',
        'interval': 1,
        'formatter': standard_format,
        'filename': 'error_log.log'
    },
    {
        'name': 'tornado.critical.log',
        'level': 'CRITICAL',
        'log_to_stderr': True,
        'when': 'midnight',
        'interval': 1,
        'formatter': standard_format,
        'filename': 'critical_log.log'
    },
)


#配置模版引擎
#引入相应的TemplateLoader即可
#若使用自带的请给予None
#支持mako和jinja2
#mako设置为tornado.template.mako_loader.MakoTemplateLoader
#jinj2设置为tornado.template.jinja2_loader.Jinja2TemplateLoader
#初始化参数请参照jinja的Environment或mako的TemplateLookup,不再详细给出
TEMPLATE_CONFIG = {
    'template_engine': None,
    #模版路径由tornado.handler中commonhandler重写，无需指定，模版将存在于每个应用的根目录下
    'filesystem_checks': True,  #通用选项
    'cache_directory': '../_tmpl_cache',  #模版编译文件目录,通用选项
    'collection_size': 50,  #暂存入内存的模版项，可以提高性能，mako选项,详情见mako文档
    'cache_size': 0,  #类似于mako的collection_size，设定为-1为不清理缓存，0则每次都会重编译模板
    'format_exceptions': False,  #格式化异常输出，mako专用
    'autoescape': False  #默认转义设定，jinja2专用

}


# 数据库连接字符串，
# 元祖，每组为n个数据库连接，有且只有一个master，可配与不配slave
DATABASE_CONNECTION = {
    'default': {
        'connections': [
            {
                'ROLE': 'master',
                'DRIVER': 'mysql+mysqldb',
                'UID': 'root',
                # 进过AES加密的密码，格式 aes::: + ciphertext
                'PASSWD': '',
                'HOST': '',
                'PORT': 3306,
                'DATABASE': '',
                'QUERY': {'charset': 'utf8'}
            },
            {
                'ROLE': 'slave',
                'DRIVER': 'mysql+mysqldb',
                'UID': 'root',
                # 进过AES加密的密码，格式 aes::: + ciphertext
                'PASSWD': '',
                'HOST': '',
                'PORT': 3306,
                'DATABASE': '',
                'QUERY': {'charset': 'utf8'}
            }
        ]
    }
}
# 每个定时对db进行一次ping操作，防止mysql gone away
PING_DB = 300  # (s秒)
# 每次取出ping多少个连接
PING_CONN_COUNT = 5
# sqlalchemy配置，列出部分，可自行根据sqlalchemy文档增加配置项
# 该配置项对所有连接全局共享
SQLALCHEMY_CONFIGURATION = {
    'sqlalchemy.connect_args': {
        'connect_timeout': 3
    },
    'sqlalchemy.echo': False,
    'sqlalchemy.max_overflow': 10,
    'sqlalchemy.echo_pool': False,
    'sqlalchemy.pool_timeout': 5,
    'sqlalchemy.encoding': 'utf-8',
    'sqlalchemy.pool_size': 5,
    'sqlalchemy.pool_recycle': 3600,
    'sqlalchemy.poolclass': 'QueuePool'  # 手动指定连接池类
}

PASSWORD_HASHERS = [
    # 第一个元素为默认加密方式
    'trest.utils.hasher.PBKDF2PasswordHasher',
    'trest.utils.hasher.PBKDF2SHA1PasswordHasher',
]


# 配置文件优先级 product > local > test > dev
try:
    from configs.dev import *
except ImportError as e:
    pass

try:
    from configs.test import *
except ImportError:
    pass

try:
    from configs.local import *
except ImportError:
    pass

try:
    from configs.product import *
except ImportError:
    pass
