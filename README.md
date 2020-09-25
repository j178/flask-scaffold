## 命令记录

命令 | 功能
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

开发时：
```shell
$ export FLASK_ENV=development
```

or

```shell
$ FLASK_ENV=development flask db migrate -m "xxxx"
```

# Docker

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
-[ ] 完善 Dockerfile 和 docker-compose
-[ ] 增加 marshmallow 相关内容
-[ ] 增加 hmac 签名
-[ ] 增加 protobuf 支持
-[ ] 完善基于 pytest 的测试框架
-[ ] 增加 trace
-[ ] 增加 metric
-[ ] 增加日志配置