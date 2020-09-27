from flask import Blueprint

update = Blueprint("update", __name__, url_prefix="/update")

from . import views  # noqa
