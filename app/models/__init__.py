# Created by John Jiang at 2018/7/6 19:18
import re

from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import Model as BaseModel
from sqlalchemy import Column, DateTime, Integer, func, text
from sqlalchemy.ext.declarative import declared_attr

from app.errors import APIError, errno

session_options = {"expire_on_commit": False}


class Base(BaseModel):
    """Base model"""
    common_attrs = ()
    tablename_prefix = ""

    @declared_attr
    def __tablename__(cls):
        name = cls.__name__
        return (
            cls.tablename_prefix
            + name[0].lower()
            + re.sub(r"([A-Z])", lambda m: "_" + m.group(0).lower(), name[1:])
        )

    id = Column(Integer, primary_key=True, autoincrement=True)

    created_at = Column(
        DateTime, server_default=text("CURRENT_TIMESTAMP"), nullable=False
    )
    updated_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=func.now(),
        nullable=False,
    )
    deleted_at = Column(DateTime, nullable=True)

    def from_id(self, ident, raise_error=True):
        """Get instance from primary key"""
        rv = self.query.get(ident)
        if rv is None and raise_error:
            raise APIError(errno.OBJECT_NOT_FOUND, object=self.__class__.__name__)
        return rv

    def to_dict(self):
        # todo
        return {}


# Usage: from app.models import db
db: SQLAlchemy


def init_models(app):
    """Init db models"""
    global db

    Base.tablename_prefix = app.config.get("SQLALCHEMY_TABLE_NAME_PREFIX", "")
    db = SQLAlchemy(
        model_class=Base, session_options=session_options
    )

    db.init_app(app)
    db.app = app

    from .models import App, AppUpdate, AppVersion

    App.create_default_app()
    # ...
    # Import more models here

    @app.shell_context_processor
    def make_context():
        return dict(
            db=db,
            session=db.session,
            App=App,
            AppVersion=AppVersion,
            AppUpdate=AppUpdate,
        )

    return db
