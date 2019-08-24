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
pipenv shell
python server.py --port=8080
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
