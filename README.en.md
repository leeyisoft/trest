# T-Rest
* T = Tornado
* Rest = Restful

#### Description
Web MVC framework based on Tornado combined with asyncio

#### Software Architecture
Software architecture description

#### Installation

Put the following line of code into the Pipfile file [packages]
> trest = {editable = true,git = "https://gitee.com/leeyi/trest.git"}

or
> pipenv install -e git+https://gitee.com/leeyi/trest.git#egg=trest

or
> pip install git+https://gitee.com/leeyi/trest.git

#### Instructions
After pipenv install under the root directory, add server.py
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

##### The API response
Use the raise JsonError wherever
```
from trest.exception import JsonError

raise JsonError('msg')
raise JsonError('msg', 0)
raise JsonError('msg', 1, [])
raise JsonError('msg', 1, [1,2,3])
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