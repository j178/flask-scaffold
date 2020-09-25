# -*- coding: utf-8 -*-
# Created by johnj at 2020/9/25
from functools import wraps
from marshmallow import Schema
from werkzeug.exceptions import BadRequest, NotAcceptable, UnsupportedMediaType
from flask import Flask, Request, Response, request as flask_request, jsonify
from google.protobuf import json_format
from google.protobuf.message import Message, DecodeError as ProtobufDecodeError
from google.protobuf.reflection import GeneratedProtocolMessageType


class EncodeError(Exception):
    pass


class Codec:
    mime_type: str = None

    def parse_request_data(self, request: Request) -> dict:
        raise NotImplementedError

    def make_response(self, data, status_code, headers) -> Response:
        response = jsonify(data)
        return Flask.response_class(response, status_code, headers)


class URLEncodedCodec(Codec):
    mime_type = "application/x-www-form-urlencoded"

    def parse_request_data(self, request: Request) -> dict:
        return request.values


class JsonCodec(Codec):
    mime_type = 'application/json'

    def parse_request_data(self, request) -> dict:
        return request.get_json(slient=False)


class ProtobufCodec(Codec):
    mime_type = 'application/x-protobuf'

    def __init__(self, receives: Message = None, sends: Message = None, errors: Message = None):
        assert receives or sends
        if receives:
            assert isinstance(receives, GeneratedProtocolMessageType)
        if sends:
            assert isinstance(sends, GeneratedProtocolMessageType)
        if errors:
            assert isinstance(errors, GeneratedProtocolMessageType)

        self.receive_type = receives
        self.send_type = sends
        self.error_type = errors

    def parse_request_data(self, request: Request) -> dict:
        if not self.receive_type:
            raise BadRequest

        message = self.receive_type()
        try:
            message.ParseFromString(request.get_data())
        except ProtobufDecodeError:
            raise BadRequest from None

        data_dict = json_format.MessageToDict(message)
        return data_dict

    def make_response(self, data, status_code, headers) -> Response:
        if not data:
            return Flask.response_class(
                "",
                status_code,
                headers,
                mimetype=self.mime_type
            )

        if not self.send_type:
            raise EncodeError(
                "Data could not be encoded into a protobuf message. No "
                "protobuf message type specified to send."
            )
        # if the status code is not a success code
        if status_code % 100 == 4 and self.error_type:
            response_data = self.error_type()
        else:
            response_data = self.send_type()
        json_format.ParseDict(data, response_data)

        return Flask.response_class(
            response_data.SerializeToString(),
            status_code,
            headers,
            mimetype=self.mime_type
        )


def _result_to_response_tuple(result):
    # Returned tuples are also evaluated
    if isinstance(result, tuple):
        assert 0 < len(result) <= 3
        if len(result) == 1:
            return result[0], 200, {}
        if len(result) == 2:
            return result[0], result[1], {}
        elif len(result) == 3:
            return result

    return result, 200, {}


urlencoded = URLEncodedCodec()
json = JsonCodec()
protobuf = ProtobufCodec


class api:
    def __init__(self, *codecs, schema: Schema = None):
        self.codecs = {codec.mime_type: codec for codec in codecs}
        self.mime_types = self.codecs.keys()
        self.schema = schema

    def parse_request_data(self, request):
        """
        For PUT and POST requests, convert message into a dictionary which can
        be used by app.route functions.
        """
        if request.method in ('POST', 'PUT'):
            if request.content_type in self.mime_types:
                codec = self.codecs[request.content_type]
                return codec.parse_request_data(request)
            else:
                raise UnsupportedMediaType

    def response_mimetype(self, request):
        return request.accept_mimetypes.best_match(
            self.mime_types
        )

    def __call__(self, fn):
        @wraps(fn)
        def to_response(*args, **kwargs):
            flask_request.data_dict = self.parse_request_data(flask_request)

            result = fn(*args, **kwargs)

            # Similar to flask's app.route, returned werkzeug responses are
            # passed directly back to the caller
            if isinstance(result, Response):
                return result

            # If the view method returns a default flask-style tuple throw
            # an error as when making rest API's the view method more likely
            # to return dicts and status codes than strings and headres
            if (isinstance(result, tuple) and (
                    len(result) == 0 or
                    not isinstance(result[0], dict)
            )):
                raise EncodeError(
                    "Pbj does not support flask's default tuple format "
                    "of (response, headers) or (response, headers, "
                    "status_code). Either return an instance of "
                    "flask.response_class to override pbj's response "
                    "encoding or return a tuple of (dict, status_code) "
                    "or (dict, status_code, headers)."
                )

            # Verify the server can respond to the client using
            # a mimetype the client accepts. We check after calling because
            # of the nature of Http 406
            mimetype = self.response_mimetype(flask_request)
            if not mimetype:
                raise NotAcceptable

            # If result is just an int, it must be a status code, so return
            # the response with no data and a status code
            if isinstance(result, int):
                return Flask.response_class("", mimetype=mimetype), result, []

            data, status_code, headers = _result_to_response_tuple(result)

            if not isinstance(data, dict):
                raise EncodeError(
                    "Methods decorated with api must return a dict, int "
                    "status code or flask Response."
                )

            return self.codecs[mimetype].make_response(
                data,
                status_code,
                headers
            )

        return to_response
