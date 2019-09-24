# T-Rest
* T = Tornado
* Rest = Restful

#### 介绍
基于Tornado结合asyncio的web mvc框架

依赖 Tornado SQLAlchemy pycryptodome pytz 等

#### 软件架构
```
tree -I '*svn|*node_module*|*git|py3|*.pyc|__pycache__|statics'
.
├── LICENSE
├── Pipfile
├── README.md
├── applications
│   ├── common
│   │   ├── const.py
│   │   ├── models
│   │   │   └── *.py
│   │   ├── filters
│   │   │   ├── filters/requests
│   │   │   │ └── *.py
│   │   │   └── filters/responses
│   │   │     └── *.py
│   │   ├── services
│   │   │   └── *.py
│   │   └── utils.py
│   ├── app1
│   │   ├── handlers
│   │   │   └── *.py
│   │   ├── models
│   │   │   └── *.py
│   │   ├── modules.py
│   │   ├── services
│   │   │   └── *.py
│   │   ├── filters
│   │   │   ├── filters/requests
│   │   │   │ └── *.py
│   │   │   └── filters/responses
│   │   │     └── *.py
│   │   ├── templates
│   │   │   └── */*.html
│   │   └── utils.py
│   └── app2
│   └── app3
├── configs
│   ├── dev.yaml
│   └── local.yaml
├── datas
│   ├── locales
│   │   ├── en_US.csv
│   │   └── zh_CN.csv
│   ├── menu
│   │   └── menu0.json
│   ├── mysql
│   │   └── *.sql
│   ├── nginx_vhost.conf
│   ├── production_deploy.md
│   ├── supervisor_tornado.conf
│   └── supervisord.conf
├── logs
│   └── *.log
├── server.py
└── tests
    └── *_test.py
```
软件架构说明

* .env 环境配置文件，只有一个section [sys]，一个变量 TREST_ENV
* configs 应用配置文件
    * configs/local.yaml 本地开发环境相关配置
    * configs/dev.yaml 开发环境相关配置
    * configs/test.yaml 测试环境相关配置
    * configs/product.yaml 生产环境相关配置
* applications 应用rest api相关代码
    * applications/common/models 公共应用数据模型层
    * applications/common/services 公共应用服务层
    * applications/common/filters/requests 公共应用请求过滤器层
    * applications/common/filters/responses 公共应用响应过滤器层
    * applications/common/const.py 公共应用常量
    * applications/common/utils.py 公共应用助手函数
    * applications/app1 独立应用
    * applications/app1/handlers app1用控制器层
    * applications/app1/models app1用数据模型层
    * applications/app1/services app1应用服务层
    * applications/app1/templates app1应用视图层
    * applications/app1/filters/requests app1应用请求过滤器层
    * applications/app1/filters/responses app1应用响应过滤器层
* datas 数据
    * datas/locales 多语言数据
    * datas/json JSON数据文件
    * datas/sql SQL数据文件
    * \*\.* 其他数据文件
* logs 日志文件
* statics Web静态资源
* tests 测试脚本
* server.py 项目入口文件
* README.md 项目说明文件
* Pipfile pipenv配置文件
* LICENSE 开源许可证
* .gitignore Git忽略文件

#### 安装教程

把下面一行代码放入Pipfile文件 [packages]下面
> trest = {editable = true,git = "https://gitee.com/leeyi/trest.git",ref = "master"}

或者直接
> pipenv install -e git+https://gitee.com/leeyi/trest.git@master#egg=trest

或者
> pip install git+https://gitee.com/leeyi/trest.git

#### 使用说明
参考 下面Demo项目，

在项目根目录（ ROOT_PATH ）下面创建 server.py 文件
```
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import resource
resource.setrlimit(resource.RLIMIT_NOFILE, (10240, 9223372036854775807))

from tornado.options import define

abs_file = os.path.abspath(sys.argv[0])
ROOT_PATH = abs_file[:abs_file.rfind('/')]
define('ROOT_PATH', ROOT_PATH)

# 把当前目录添加到 sys.path 开头
sys.path.insert(0, ROOT_PATH)

from trest.webserver import run


if __name__ == "__main__":
    try:
       server = run()
    except KeyboardInterrupt:
        sys.exit(0)

```

在 项目根目录（ ROOT_PATH ） 下面创建 [.env 文件](https://gitee.com/leeyi/trest/blob/master/demo_dot.env)
```
# TREST_ENV is not one of the local, dev, test, or product
TREST_ENV : dev

```

run
```
pipenv install --skip-lock
pipenv shell
python server.py --port=5080
python tests/app_demo/server.py --port=5081
```

f'{ROOT_PATH}/configs/{env}.yaml' demo

like this [./tests/app_demo/configs/dev.yaml](https://gitee.com/leeyi/trest/blob/master/tests/app_demo/configs/dev.yaml)

# [开发约定](https://gitee.com/leeyi/trest/blob/master/promise.md)

* 开发约定 [https://gitee.com/leeyi/trest/blob/master/promise.md](https://gitee.com/leeyi/trest/blob/master/promise.md)
* 其他约定遵从[Python风格规范](http://zh-google-styleguide.readthedocs.io/en/latest/google-python-styleguide/python_language_rules/) 、 [Python 编码规范](http://liyangliang.me/posts/2015/08/simple-python-style-guide/)

#### Demo
* [https://gitee.com/leeyi/py_admin](https://gitee.com/leeyi/py_admin/tree/dev/)
```
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
[description]
"""
from trest.router import put
from trest.router import get
from trest.router import post
from trest.router import delete
from trest.handler import Handler
from trest.exception import JsonError


class DemoHandler(Handler):
    @post('demo0')
    def add(self):
        return self.success(data = ['post', 'demo0'])

class Demo1Handler(Handler):
    @post('demo1')
    def add(self):
        return self.success(data = ['post', 'demo1'])

class Demo2Handler(Handler):
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
