from flask import request

from app.api import json, make_api, multipart, protobuf
from app.protos.update_pb2 import GetUpdateResponse

from . import update
from .schemas import (
    CreateUpdateSchema,
    CreateVersionSchema,
    GetUpdateSchema,
    ListVersionsSchema,
)
from app.models.models import App
from app.errors import APIError, errno


@update.route("/", methods=["GET"])
@make_api(
    codecs=[json, protobuf(sends=GetUpdateResponse)], query_schema=GetUpdateSchema()
)
def get_update():
    query_dict = request.query_dict

    app = App.from_app_name(query_dict['app_name'])
    if not app:
        raise APIError(errno.OBJECT_NOT_FOUND, object="App")



@update.route("/version", methods=["POST"])
@make_api(codecs=[json], body_schema=CreateVersionSchema())
def create_version():
    pass


@update.route("/versions", methods=["GET"])
@make_api(codecs=[json], query_schema=ListVersionsSchema())
def list_versions():
    pass


@update.route("/update", methods=["POST"])
@make_api(codecs=[multipart], body_schema=CreateUpdateSchema())
def create_update():
    pass
