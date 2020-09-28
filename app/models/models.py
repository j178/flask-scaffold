# Created by John Jiang at 2018/7/6 20:44
import json
from enum import Enum, IntEnum

from sqlalchemy.exc import IntegrityError

from app.models import db

DEFAULT_DATETIME = "1001-01-01 00:00:01"


class Language(Enum):
    CN = "zh-CN"
    EN = "en-US"


class App(db.Model):
    """A managed app"""
    app_name = db.Column(db.String(255), nullable=False, default="", unique=True)
    description = db.Column(db.String(2048), nullable=True)

    versions = db.relationship(
        "AppVersion",
        primaryjoin="foreign(AppVersion.app_id) == remote(App.id)",
        back_populates="app",
        order_by="AppVersion.id.desc()",
        lazy="dynamic",
    )

    @classmethod
    def create_default_app(cls):
        default_app_name = "com.didi.voyager.jarvis"
        app = App(app_name=default_app_name, description="Default/First app")
        db.session.add(app)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    @classmethod
    def from_app_name(cls, app_name) -> "App":
        app = db.session.query.filter_by(app_name=app_name).one_or_none()
        return app

    def latest_version(self) -> "AppVersion":
        return self.versions.first()

    def select_update(self, query:dict) -> 'AppUpdate':
        current_version = query['version_code']
        # iterate versions from latest to oldest
        # todo cache all versions in memory for a period
        for version in self.versions:
            if current_version >= version.version_code:
                break
            update = version.select_update(query)
            if update:
                return update



class AppVersion(db.Model):
    """A version of the app"""

    class Type(IntEnum):
        FULL = 1
        PATCH = 2

    app_id = db.Column(db.Integer, nullable=False, index=True)

    version = db.Column(db.String(32), nullable=False)
    version_code = db.Column(db.Integer, nullable=False)
    type = db.Column(db.SmallInteger, nullable=False, default=Type.FULL)
    package_url = db.Column(db.String(1024), nullable=False)
    package_size = db.Column(db.Integer, nullable=False)
    package_md5 = db.Column(db.String(64), nullable=False)
    # 升级文本
    update_text = db.Column(db.Text)
    update_text_en = db.Column(db.Text)

    app = db.relationship(
        App,
        primaryjoin="foreign(AppVersion.app_id) == remote(App.id)",
        uselist=False,
        back_populates="versions",
    )
    updates = db.relationship(
        "AppUpdate",
        primaryjoin="foreign(AppUpdate.app_version_id) == remote(AppVersion.id)",
        back_populates="app_version",
        order_by="AppVersion.id.desc()",
        lazy="dynamic",
    )

    def select_update(self, query:dict):
        # todo cache updates
        for update in self.updates:
            if update.can_update(query):
                return update

    @property
    def is_patch(self):
        return self.type == self.Type.PATCH


class AppUpdate(db.Model):
    class Type(IntEnum):
        GRAY = 1
        NORMAL = 2

    app_id = db.Column(db.Integer, nullable=False, index=True)
    app_version_id = db.Column(db.Integer, nullable=False, index=True)

    is_force = db.Column(db.Boolean, nullable=False, default=0)
    # selector condtions
    # car_id in ["1", "2", "3"] or region_name == "shanghai"
    conditions = db.Column(db.String(2048), nullable=True)
    type = db.Column(db.SmallInteger, nullable=False, default=Type.NORMAL)

    app_version = db.relationship(
        AppVersion,
        uselist=False,
        primaryjoin="foreign(AppUpdate.app_version_id) == remote(AppVersion.id)",
        back_populates="updates",
    )

    def to_dict(self, params):
        result = {
            "is_force": self.is_force,
            "need_update": True,
            "version": self.app_version.version,
            "version_code": str(self.app_version.version_code),
            "update_type": self.type,
        }

        if params.get("lang") == Language.CN.value:
            update_text_json = self.app_version.update_text
        else:
            update_text_json = self.app_version.update_text_en
        update_text = json.loads(update_text_json)
        result.update(update_text)

        if self.app_version.is_patch:
            result["patch_url"] = self.app_version.package_url
            result["patch_md5"] = self.app_version.package_md5
            result["patch_size"] = self.app_version.package_size
        else:
            result["update_url"] = self.app_version.package_url
            result["package_md5"] = self.app_version.package_md5
            result["package_size"] = self.app_version.package_size

        # misc
        result["pacakge_id"] = 0
        result["version_id"] = 0
        if self.is_force:
            result["update_type"] = 3

        return result

    def can_update(self, query: dict) -> bool:
        """Determine if the update suitable for this query."""
        version = self.app_version
        # Currently we check the version_code only
        # later there will be more conditions, such as car_id, region.
        if version.version_code <= query["version_code"]:
            return False

        return True
