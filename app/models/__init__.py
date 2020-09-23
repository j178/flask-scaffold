# Created by John Jiang at 2018/7/6 19:18
import re

from flask import json
from flask_sqlalchemy import BaseQuery, SQLAlchemy
from flask_sqlalchemy.model import Model as BaseModel
from sqlalchemy import Column, DateTime, Integer, Text, TypeDecorator, func, text
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import load_only
from sqlalchemy.orm.base import _generative
from sqlalchemy.orm.query import _MapperEntity


class JSONEncodedDict(TypeDecorator):
    impl = Text

    def process_bind_param(self, value, dialect):
        if value is None:
            return "{}"
        else:
            return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)


MutableDict.associate_with(JSONEncodedDict)

session_options = {"expire_on_commit": False}


class Query(BaseQuery):
    @_generative()
    def only_common_attrs(self):
        for ent in self._entities:
            if isinstance(ent, _MapperEntity):
                class_ = ent.entities[0]
                if getattr(class_, "common_attrs", None):
                    # inline query.options()
                    self._attributes = self._attributes.copy()
                    if "_unbound_load_dedupes" not in self._attributes:
                        self._attributes["_unbound_load_dedupes"] = set()

                    opt = load_only(*getattr(class_, "common_attrs"))
                    self._with_options = self._with_options + (opt,)
                    opt.process_query(self)


class Base(BaseModel):
    common_attrs = ()

    @declared_attr
    def __tablename__(cls):
        name = cls.__name__
        return name[0].lower() + re.sub(
            r"([A-Z])", lambda m: "_" + m.group(0).lower(), name[1:]
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


# Usage: from app.models import db
db: SQLAlchemy


def init_models(app):
    global db

    db = SQLAlchemy(
        model_class=Base, query_class=Query, session_options=session_options
    )

    db.init_app(app)

    # reflect_tables(app)

    from .user import User

    # ...
    # Import more models here

    @app.shell_context_processor
    def make_context():
        return dict(db=db, query=db.session.query, User=User)

    return db
