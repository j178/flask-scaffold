# -*- coding: utf-8 -*-
# Created by johnj at 2020/9/24

import logging
import time

from flask import current_app, redirect, request, url_for
from werkzeug.utils import secure_filename

from app.extensions import cache
from . import files

log = logging.getLogger(__name__)


@files.route('/')
def index():
    log.error('this is a test')
    return 'hello'


@files.route('/timing')
@cache.cached()
def timing():
    time.sleep(1)
    return 'hello'


@files.route('/photo', methods=['POST'])
def upload_photo():
    filename = secure_filename(request.files['photo'].filename)
    current_app.mongo.save_file(filename, request.files['photo'])
    return redirect(url_for('.get_photo', filename=filename))


@files.route('/photo/<path:filename>', methods=['GET'])
def get_photo(filename):
    return current_app.mongo.send_file(filename)
