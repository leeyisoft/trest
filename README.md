# T-Rest
* T = Tornado
* Rest = Restful

#### 介绍
基于Tornado结合asyncio的web mvc框架

依赖 Tornado SQLAlchemy pycryptodome pytz 等

#### 软件架构
软件架构说明

```

```

#### 安装教程

把下面一行代码放入Pipfile文件 [packages]下面
> trest = {editable = true,git = "https://gitee.com/leeyi/trest.git",ref = "master"}

或者直接
> pipenv install -e git+https://gitee.com/leeyi/trest.git@master#egg=trest

或者
> pip install git+https://gitee.com/leeyi/trest.git

#### 使用说明
参考 下面Demo项目
run
```
pipenv install --skip-lock
pipenv shell
export ENV=local
python server.py --port=8080
```

f'{ROOT_PATH}/configs/{env}.ini' demo
```
# f'{ROOT_PATH}/configs/{env}.ini'
# 注意配置解析出来都是字符串，请不要带单引号或者双引号
# 例如 '0.0.0.0' "0.0.0.0" 都会报错

[sys]
arbitrary_ip = 0.0.0.0
port = 5080
local_ip = 127.0.0.1
translation = true
time_zone = Asia/Shanghai
language_code = zh-hans

login_pwd_rsa_encrypt = True
default_aes_secret = 883d65f06fd447f3a1e69a36e73f58e0
admin_session_key = de0b3fb0c2f44563944a8cccca7f225a
front_session_key = 171630947de24c969c28b2d178c4e0fe
valid_code_key = ab1195c6f0084b4f8b007d3aa7628a38
token_key = f30a2331813f46d0adc2bcf26fcbbbf4
rabbitmq_config =
sentry_url =
config_cache_prefix = conf:
user_cache_prefix = user:
admin_cache_prefix = admin:

# 超级管理员角色ID
super_role_id = 1
default_role_id = 2

[tornado]
debug = true
xsrf_cookies = true
xheaders = true
cookie_secret = e921bfcd-ace4-4124-8657-c57a162365f6

[session]
cache_alias = default_redis
name = nkzpg9NKBpKS2iaK
cookie_domain =
cookie_path = /
expires = 86400
secret = fLjUfxqXtfNoIldA0A0J
version = v0.1.0

[sqlalchemy]
# (s秒)
ping_db = 300
# 每次取出ping多少个连接
ping_conn_count = 5
connect_timeout = 3
echo = true
echo_pool = true
max_overflow = 10
pool_timeout = 5
encoding = utf8
pool_size = 5
pool_recycle = 3600
poolclass = QueuePool

[default_redis]
location = 127.0.0.1:6379
db = 0
password = abc123456
ping_interval = 120
parser_class = redis.connection.DefaultParser
socket_timeout = 2
socket_connect_timeout = 2

[redis]
host = 127.0.0.1
port = 6379
password = abc123456
charset = utf8
db = 3

[db_master]
driver = mysql+mysqldb
user = root
password = 123456
host = 127.0.0.1
port = 3306
database = db_py_admin
charset = utf8mb4

[db_slave]
driver = mysql+mysqldb
user = root
password = 123456
host = 127.0.0.1
port = 3306
database = db_py_admin
charset = utf8mb4

```

#### Demo
* [https://gitee.com/leeyi/py_admin](https://gitee.com/leeyi/py_admin/tree/dev/)
```
from trest.exception import JsonError
from trest.router import get
from trest.router import delete
from trest.router import post
from trest.router import put

"""
在 applications/admin/handlers/abcd.py
# 文件名称不以 _ 开头，明确API方法名称要唯一
url 像这样,
    /admin/welcome
    /admin/welcome2
    /welcome3
    /admin/welcome4
"""

class WelcomeHandler(CommonHandler):
    @get('welcome')
    @required_permissions()
    @tornado.web.authenticated
    def welcome_get(self, *args, **kwargs):
        """后台首页
        """
        # menu = AdminMenu.main_menu()
        # print('menu ', menu)
        # self.show('abc')
        params = {
        }
        self.render('dashboard/welcome.html', **params)

    @get('welcome2')
    @required_permissions()
    @tornado.web.authenticated
    def welcome_get2(self, *args, **kwargs):
        """后台首页
        """
        self.success(data=['welcome2'])

    @get('/welcome3')
    @required_permissions()
    @tornado.web.authenticated
    def welcome_get(self, *args, **kwargs):
        """后台首页
        """
        self.success(data=['welcome3'])

    @post('welcome4')
    @required_permissions()
    @tornado.web.authenticated
    def welcome_post(self, *args, **kwargs):
        """后台首页
        """
        self.success(data=['welcome3'])
```

##### API响应
在任意的地方使用 raise JsonError
```
from trest.exception import JsonError

raise JsonError('msg')
raise JsonError('msg', 0)
raise JsonError('msg', 1, [])
raise JsonError('msg', 1, [1,2,3])
```

#### 参与贡献

1. Fork 本仓库
2. 新建 Feat_xxx 分支
3. 提交代码
4. 新建 Pull Request


#### 码云特技

1. 使用 Readme\_XXX.md 来支持不同的语言，例如 Readme\_en.md, Readme\_zh.md
2. 码云官方博客 [blog.gitee.com](https://blog.gitee.com)
3. 你可以 [https://gitee.com/explore](https://gitee.com/explore) 这个地址来了解码云上的优秀开源项目
4. [GVP](https://gitee.com/gvp) 全称是码云最有价值开源项目，是码云综合评定出的优秀开源项目
5. 码云官方提供的使用手册 [https://gitee.com/help](https://gitee.com/help)
6. 码云封面人物是一档用来展示码云会员风采的栏目 [https://gitee.com/gitee-stars/](https://gitee.com/gitee-stars/)
