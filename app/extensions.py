# -*- coding: utf-8 -*-
# Created by johnj at 2020/9/23
from flask_caching import Cache
from flask_log_request_id import RequestID
from flask_log_request_id.parser import x_request_id
from redis import Redis

# For other module-level imports
cache: Cache
redis: Redis


def init_extentions(app):
    global cache, redis

    cache = Cache(app)
    redis = Redis.from_url(app.config["CACHE_REDIS_URL"], decode_responses=True)

    RequestID(app, request_id_parser=x_request_id)

    # ...
    # Add more extensions here
