# Created by John Jiang at 2018/7/6 19:01


class BaseConfig:
    # Generate by running: python -c 'import os; print(os.urandom(32))'
    SECRET_KEY = b'\x90\xf5\xf5K;\xa5\x85\xacL\x0b\x00\xdf\xb7:,\xc6}\x8b\xc3 9\x10h\xf8\x96\xf1\xb2\xf5\x16\xd1\r\xa0'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://plugin:123456@db:3306/plugins'

    # redis 作用：通用缓存、存 session、消息队列 backend
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = 'redis://redis:6379'

    # ...
    # Add your own settings here
