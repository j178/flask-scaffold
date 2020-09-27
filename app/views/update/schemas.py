from enum import Enum

from marshmallow import Schema, fields


class Language(Enum):
    CN = "zh-CN"
    EN = "en-US"


class GetUpdateSchema(Schema):
    version = fields.Str(required=True)
    version_code = fields.Function(required=True, serialize=str, deserialize=int)
    lang = fields.Str(required=True, validate=Language)
    os_type = fields.Str()
    os_version = fields.Str()
    network_type = fields.Str()
    app_name = fields.Str()
    model = fields.Str()
    car_id = fields.Str()
    imei = fields.Str()
    pixels = fields.Str()
    mac = fields.Str()
    cpu = fields.Str()
    android_id = fields.Str()
    brand = fields.Str()
    region_name = fields.Str()
    city_id = fields.Str()


class CreateVersionSchema(Schema):
    pass


class ListVersionsSchema(Schema):
    app_name = fields.Str()
    app_id = fields.Function(serialize=str, deserialize=int)


class CreateUpdateSchema(Schema):
    app_id = fields.Int()
    app_version_id = fields.Int()
