# flask-scaffold

## Features

## How to use

```shell script
$ git clone git@github.com:j178/flask-scaffold.git
$ cd flask-scaffold
$ pipenv install
$ pipenv shell
```

Under development:

```shell
$ export FLASK_ENV=development
$ flask db migrate -m "xxxx"
```

or

```shell
$ FLASK_ENV=development flask db migrate -m "xxxx"
```

## Common commands

command | function
---- | ---
flask run | 启动开发服务器
flask shell | 启动调试 Shell
flask db migrate  -m *message* | 生成数据库修改记录
flask db upgrade | 升级数据库
flask routes | 查看路由记录
flask test | 执行测试用例
pipenv shell | Spawn a venv shell
pipenv install *package* | 安装新的依赖
docker-compose up -d | 启动所有服务
docker-compose run -d -p 3306:3306 db | 启动开发用数据库



## Parameter validation
`request.data_dict` contains the data has been parsed and validated.

Define a new parameter schema:
```python
from flask import request
from marshmallow import Schema, fields
from app import api

class UpdateMessageSchema(Schema):
    id = fields.Integer(required=True)
    message = fields.String(required=True)

@app.route('/message', methods=['POST'])
@api.api(api.json, schema=UpdateMessageSchema())
def update_message():
    data = request.data_dict
    ...
```

## Auth

## Protobuf support
 
## Error handling

在视图函数中，如果想提前结束流程，可以抛出 `APIError`，比如:
```python
from flask import request
from app.errors import APIError, errno

if request.data_dict.get('id'):
    raise APIError(errno.INVALID_PARAMETERS)
```

## Logging

## DB model

## Pagnination

### Query

### Save & Update

### Delete

## Add new flask subcommand

## Docker

Build images with:
```shell script
$ docker build --tag <name> --file docker/Dockerfile . 
```

You can stop the build at specific stages with the --target option:
```shell script
$ docker build --tag <name> --file docker/Dockerfile . --target <stage>
```
For example we wanted to stop at the development stage:
```shell script
$ docker build --tag poetry-project --file docker/Dockerfile --target development .
```

# Todo
- [x] 完善 Dockerfile 和 docker-compose
- [x] 增加 marshmallow 相关内容
- [ ] 增加 hmac 签名
- [x] 增加 protobuf 支持
- [ ] 完善基于 pytest 的测试框架
- [ ] 增加 trace
- [ ] 增加 metric
- [ ] 增加日志配置