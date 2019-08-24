# T-Rest
* T = Tornado
* Rest = Restful

#### Description
Web MVC framework based on Tornado combined with asyncio

#### Software Architecture
Software architecture description

#### Installation

Put the following line of code into the Pipfile file [packages]
> trest = {editable = true,git = "https://gitee.com/leeyi/trest.git",ref = "master"}

or
> pipenv install -e git+https://gitee.com/leeyi/trest.git@master#egg=trest

or
> pip install git+https://gitee.com/leeyi/trest.git#egg=trest

#### Instructions
After pipenv install under the root directory, add server.py

run
```
pipenv shell
python server.py --port 8080
```

##### The API response
Use the raise JsonError wherever
```
from trest.exception import JsonError

raise JsonError('msg')
raise JsonError('msg', 0)
raise JsonError('msg', 1, [])
raise JsonError('msg', 1, [1,2,3])
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
in applications/admin/handlers/abcd.py
# file name not start with _ and method name is unique
url like this,
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

#### Test
```
pipenv install --skip-lock
```

#### Contribution

1. Fork the repository
2. Create Feat_xxx branch
3. Commit your code
4. Create Pull Request


#### Gitee Feature

1. You can use Readme\_XXX.md to support different languages, such as Readme\_en.md, Readme\_zh.md
2. Gitee blog [blog.gitee.com](https://blog.gitee.com)
3. Explore open source project [https://gitee.com/explore](https://gitee.com/explore)
4. The most valuable open source project [GVP](https://gitee.com/gvp)
5. The manual of Gitee [https://gitee.com/help](https://gitee.com/help)
6. The most popular members  [https://gitee.com/gitee-stars/](https://gitee.com/gitee-stars/)
