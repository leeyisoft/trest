# T-Rest
* T = Tornado
* Rest = Restful

#### 介绍
* 基于Tornado结合asyncio的web mvc框架
* 支持AMQP
*

#### 软件架构
软件架构说明

```

```

#### 安装教程

把下面一行代码放入Pipfile文件 [packages]下面
> trest = {editable = true,git = "https://gitee.com/leeyi/trest.git"}

或者直接
> pipenv install -e git+https://gitee.com/leeyi/trest.git#egg=trest

或者
> pip install git+https://gitee.com/leeyi/trest.git

#### 使用说明
在根目录下面 pipenv install 之后，添加 server.py 之后
```
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import resource
resource.setrlimit(resource.RLIMIT_NOFILE, (10240, 9223372036854775807))

from tornado.options import define

# sys.path.insert(0, '/Users/leeyi/workspace/py3/trest')
ROOT_PATH = os.getcwd()
define('ROOT_PATH', ROOT_PATH)

# 把当前目录添加到 sys.path 开头
sys.path.insert(0, ROOT_PATH)

from trest.webserver import run


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        sys.exit(0)

```
run
```
pipenv shell
run server.py
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