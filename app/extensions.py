# -*- coding: utf-8 -*-
# Created by johnj at 2020/9/23
from flask_caching import Cache
from redis import Redis

# For other module-level imports
cache: Cache
redis: Redis


def init_extentions(app):
    global cache, redis

    cache = Cache(app)
    redis = Redis.from_url(app.config['CACHE_REDIS_URL'],
                           decode_responses=True)

    # ...
    # Add more extensions here
