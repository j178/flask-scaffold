# -*- coding: utf-8 -*-
# Created by johnj at 2020/9/25
import json
from enum import IntEnum

from werkzeug.exceptions import HTTPException


class errno(IntEnum):
    def __new__(cls, code: int, message: str = ""):
        obj = int.__new__(cls, code)  # type: ignore
        obj._value_ = code

        obj.message = message
        return obj

    def __str__(self):
        return str(self.value)

    UNKNOWN = 100, "Uknown error"
    INVALID_PARAMETERS = 101, "Invalid parameters"


class APIError(HTTPException):
    code = 400

    def __init__(self, error, message=None, response=None, **kwargs):
        """
        error 一般是 errno 的属性，如 raise APIError(errno.UNAUTHORIZED)
        description 为空时使用 error_code 默认的错误描述，也可以使用自定义的字符串。字符串中可以包含 "{name}" 这样可以被替换的部分。
        args 可以是任何关键字参数，会被格式化到 description 中。
        """
        if isinstance(error, errno):
            error_code = error.value
            # 如果没有提供 description, 使用默认的
            if message is None:
                message = error.message
        else:
            # 自定义的 error_code, 必须要提供 description
            error_code = error
            if message is None:
                raise RuntimeError("Empty error message")

        super().__init__(str(message), response)
        self.error_code = error_code
        self.kwargs = kwargs

    def get_description(self, environ=None):
        message = self.description

        if self.kwargs:
            try:
                message = message.format_map(self.kwargs)
            except KeyError:
                raise RuntimeError(f"Error when formatting error message: {message!r}")

        return message

    def get_headers(self, environ=None):
        return [("Content-Type", "application/json")]

    def get_body(self, environ=None):
        return json.dumps(
            {
                "success": False,
                "message": self.get_description(environ),
                "code": self.error_code,
            }
        )


class AuthError(APIError):
    code = 401
