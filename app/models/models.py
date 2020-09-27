# Created by John Jiang at 2018/7/6 20:44
import json
from enum import IntEnum, Enum

from sqlalchemy.exc import IntegrityError

from app.models import db

DEFAULT_DATETIME = "1001-01-01 00:00:01"


class Language(Enum):
    CN = 'zh-CN'
    EN = 'en-US'


class App(db.Model):
    """A managed app"""

    common_attrs = ("id", "app_name")

    app_name = db.Column(db.String(255), nullable=False, default="", unique=True)
    description = db.Column(db.String(2048), nullable=True)

    @classmethod
    def create_default_app(cls):
        default_app_name = 'com.didi.voyager.jarvis'
        app = App(app_name=default_app_name, description="Default/First app")
        db.session.add(app)
        try:
            db.session.commit()
        except IntegrityError:
            pass

    @classmethod
    def from_app_name(cls, app_name) -> 'App':
        app = db.session.query.filter_by(app_name=app_name).one_or_none()
        return app

    def latest_update(self) -> 'AppUpdate':
        return 

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
    package_size = db.Column(db.Integer, nullable=False)
    package_md5 = db.Column(db.String(64), nullable=False)
    # 升级文本
    update_text = db.Column(db.Text)
    update_text_en = db.Column(db.Text)

    app = db.relationship(App, primaryjoin='AppVersion.app_id == foreign(App.id)')

    @property
    def is_patch(self):
        return self.type == self.Type.PATCH


class AppUpdate(db.Model):
    class Type(IntEnum):
        GRAY = 1
        NORMAL = 2

    app_id = db.Column(db.Integer, nullable=False)
    app_version_id = db.Column(db.Integer, nullable=False)

    is_force = db.Column(db.Boolean, nullable=False, default=0)
    # selector condtions
    # car_id in ["1", "2", "3"] or region_name == "shanghai"
    conditions = db.Column(db.String(2048), nullable=True)
    type = db.Column(db.SmallInteger, nullable=False, default=Type.NORMAL)

    app = db.relationship(App, primaryjoin='AppUpdate.app_id == foreign(App.id)')
    app_version = db.relationship(AppVersion, primaryjoin='AppUpdate.app_version_id == foreign(AppVersion.id)')

    def to_dict(self, params):
        result = {
            'is_force': self.is_force,
            'need_update': True,
            'version': self.app_version.version,
            'version_code': str(self.app_version.version_code),
            'update_type': self.type,
        }

        if params.get('lang') == Language.CN.value:
            update_text_json = self.app_version.update_text
        else:
            update_text_json = self.app_version.update_text_en
        update_text = json.loads(update_text_json)
        result.update(update_text)

        if self.app_version.is_patch:
            result['patch_url'] = self.app_version.package_url
            result['patch_md5'] = self.app_version.package_md5
            result['patch_size'] = self.app_version.package_size
        else:
            result['update_url'] = self.app_version.package_url
            result['package_md5'] = self.app_version.package_md5
            result['package_size'] = self.app_version.package_size

        # misc
        result['pacakge_id'] = 0
        result['version_id'] = 0
        if self.is_force:
            result['update_type'] = 3

        return result

    def can_update(self, params: dict) -> bool:
        version = self.app_version
        if version.version_code <= params['version_code']:
            return False

        return True
