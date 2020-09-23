# Created by John Jiang at 2018/7/6 13:51
import os

# wsgi.py 和 app.py 两个文件，并且其中的 app, application, create_app 属性、方法
# 可以被 flask 自动找到并得到相应的 app 对象

from app import create_app, cli

# FLASK_ENV=development will enable FLASK_DEBUG=True by default (if no set).
app = create_app(os.getenv('FLASK_ENV', 'production'))

if os.getenv('FLASK_RUN_FROM_CLI'):
    cli.init_cli(app)
