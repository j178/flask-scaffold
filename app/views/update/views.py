from flask import request

from app.api import json, make_api, multipart, protobuf
from app.errors import APIError, errno
from app.models.models import App
from app.protos.update_pb2 import GetUpdateResponse

from . import update
from .schemas import (
    CreateUpdateSchema,
    CreateVersionSchema,
    GetUpdateSchema,
    ListVersionsSchema,
)


@update.route("/", methods=["GET"])
@make_api(
    codecs=[json, protobuf(sends=GetUpdateResponse)], query_schema=GetUpdateSchema()
)
def get_update():
    """Check if there is an update."""
    query_dict = request.query_dict

    app = App.from_app_name(query_dict["app_name"])
    if not app:
        raise APIError(errno.OBJECT_NOT_FOUND, object="App")

    update = app.select_update(query_dict)
    if update:
        return update.to_dict(query_dict)
    return {}


@update.route("/version", methods=["POST"])
@make_api(codecs=[json], body_schema=CreateVersionSchema())
def create_version():
    """Create a new version for an app."""
    pass


@update.route("/versions", methods=["GET"])
@make_api(codecs=[json], query_schema=ListVersionsSchema())
def list_versions():
    """List versions of an app."""
    pass


@update.route("/update", methods=["POST"])
@make_api(codecs=[multipart], body_schema=CreateUpdateSchema())
def create_update():
    """Create a new update for a version."""
    pass
