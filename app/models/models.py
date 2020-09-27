# Created by John Jiang at 2018/7/6 20:44
from enum import IntEnum

from app.models import db

DEFAULT_DATETIME = "1001-01-01 00:00:01"


class App(db.Model):
    """A managed app"""

    common_attrs = ("id", "app_name")

    app_name = db.Column(db.String(255), nullable=False, default="")


class AppVersion(db.Model):
    """A version of the app"""

    class Type(IntEnum):
        FULL = 1
        PATCH = 2

    app_id = db.Column(db.Integer, nullable=False)
    version = db.Column(db.String(32), nullable=False)
    version_code = db.Column(db.Integer, nullable=False)
    type = db.Column(db.SmallInteger, nullable=False, default=Type.FULL)
    package_url = db.Column(db.String(1024), nullable=False)
    packzge_size = db.Column(db.Integer, nullable=False)
    package_md5 = db.Column(db.String(64), nullable=False)
    # 升级文本
    update_text = db.Column(db.Text)
    update_text_en = db.Column(db.Text)


class AppUpdate(db.Model):
    app_id = db.Column(db.Integer, nullable=False)
    app_version_id = db.Column(db.Integer, nullable=False)
    is_force = db.Column(db.Boolean, nullable=False, default=0)

    def to_dict(self):
        d = {}
        return d
