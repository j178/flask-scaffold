# Created by John Jiang at 2018/7/6 20:44
from app.models import db

DEFAULT_DATETIME = "1001-01-01 00:00:01"


class User(db.Model):
    # __tablename__ = 'Intranet_User'
    # __table__ = db.metadata.tables[__tablename__]

    common_attrs = ("id", "name")

    name = db.Column(db.String(255), nullable=False, default="")
    type = db.Column(db.String(255), nullable=False, default="")
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_at = db.Column(db.DateTime, nullable=False, default=DEFAULT_DATETIME)
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)

    def __str__(self):
        return self.email
