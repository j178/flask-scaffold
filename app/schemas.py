# -*- coding: utf-8 -*-
# Created by johnj at 2020/9/25
from marshmallow import Schema, fields


class ErrorResponseSchema(Schema):
    class Meta:
        pass

    code = fields.Integer(required=True)
    msg = fields.String(required=True)
