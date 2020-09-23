# Created by John Jiang at 2018/7/6 19:02
from . import BaseConfig


class Config(BaseConfig):
    DEBUG = True

    SQLALCHEMY_ECHO = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/dev.db'

    CACHE_REDIS_URL = 'redis://localhost:6379'
