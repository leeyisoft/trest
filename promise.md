## 代码相关约定
* 各个INSTALLED_APP之间不要夸应用调用，不同App需要使用的模型放到common/models/xxx.py文件里，避免跨越App引用模型
* 每个App应该有自己的CommonHandler，如无必要，请直接使用 ` from trest.handler import BaseHandler `
* handlers 层 接受请求参数、校验参数，请求services，响应结果，后续处理调用；
* models 层 单纯的和数据表做映射关系，可以在这里添加虚拟熟悉，格式化数据等功能；
* services 层 供handlers层或者其他脚本调用需要事务性的的功能，由它来引入models，操作数据库，比如用户注册功能；数据列表功能，都可以定义到services里面；
* services 层 方法return 数据类型，尽量以少些代码为原则，从数据库里面出来的是 对象，就直接返回，不要特意转化为字典类型了；如果是方法从多张表里面聚合数据，返回数据类型根据事情情况确定；
* 在第一个发布版本之前的“数据库结构、数据变动”，不会给出相应update的SQL语句（如有需要、或者其他建议，欢迎留言）
* 异常信息务必记录到`SysLogger.error(e, exc_info=True)`记录到日志里面，便于排查错误
* 只定义了一个API 通过不同的请求方式，来执行不同的操作（<span style="color:red;">查询用get 添加用post 更新用put 删除用delete</span>） [参考](https://blog.csdn.net/dxftctcdtc/article/details/9197639)

## 数据库相关约定
* 数据库密码经过AES加密，没有明文存储，进过AES加密的密码，格式 aes::: + ciphertext
* 数据库使用utf8mb4编码
* 数据库和时间相关的字段统一使用Unix时间戳格式 bigint(13)，单位为毫秒
* 数据库表的主键统一用 bigint(20)
* 数据库和利息相关字段数据类型统一用 decimal(4,4)
* 数据库和金额相关字段数据类型统一用 decimal(16,2)

## 其他约定
* 其他约定遵从[Python风格规范](http://zh-google-styleguide.readthedocs.io/en/latest/google-python-styleguide/python_language_rules/)、[Python 编码规范](http://liyangliang.me/posts/2015/08/simple-python-style-guide/)
