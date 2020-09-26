# -*- coding: utf-8 -*-
# Created by johnj at 2020/9/23
import logging

from flask.logging import default_handler
from flask_log_request_id import RequestIDLogFilter

FORMAT = "%(asctime)s - %(name)s - level=%(levelname)s - request_id=%(request_id)s - %(message)s"


def init_loggers(app):
    handler = default_handler
    handler.setFormatter(logging.Formatter(FORMAT))
    handler.addFilter(RequestIDLogFilter())
