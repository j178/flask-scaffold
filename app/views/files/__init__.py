# -*- coding: utf-8 -*-
# Created by johnj at 2020/9/24
from flask import Blueprint

files = Blueprint("files", __name__, url_prefix="/files")

from . import views  # noqa: E402, F401
