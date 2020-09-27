from marshmallow import Schema, fields


class GetUpdateSchema(Schema):
    version = fields.Str()
    version_code = fields.Function(serialize=str, deserialize=int)


class CreateVersionSchema(Schema):
    pass


class ListVersionsSchema(Schema):
    app_name = fields.Str()
    app_id = fields.Function(serialize=str, deserialize=int)


class CreateUpdateSchema(Schema):
    app_id = fields.Int()
    app_version_id = fields.Int()
