# -*- coding: utf-8 -*-
# Created by johnj at 2020/9/25
from marshmallow import Schema, fields


class ErrorResponseSchema(Schema):
    class Meta:
        pass

    success = fields.Boolean(required=True)
    code = fields.Integer(required=True)
    message = fields.String(required=True)
