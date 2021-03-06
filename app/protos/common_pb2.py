# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: app/protos/common.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='app/protos/common.proto',
  package='jarvis.common',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x17\x61pp/protos/common.proto\x12\rjarvis.common\"H\n\rErrorResponse\x12&\n\x04\x63ode\x18\x01 \x01(\x0e\x32\x18.jarvis.common.ErrorCode\x12\x0f\n\x07message\x18\x02 \x01(\t*\xe2\x01\n\tErrorCode\x12\x0b\n\x07SUCCESS\x10\x00\x12\x0f\n\x0b\x45RROR_PARAM\x10\n\x12\x0e\n\nERROR_AUTH\x10\x14\x12\x12\n\x0e\x45RROR_DATABASE\x10\x1e\x12\x12\n\x0e\x45RROR_INTERNAL\x10(\x12\x12\n\x0e\x45RROR_NOTFOUND\x10\x32\x12\x16\n\x12\x45RROR_ALREADYEXIST\x10<\x12\x10\n\x0c\x45RROR_STATUS\x10\x46\x12\x10\n\x0c\x45RROR_METHOD\x10P\x12\x11\n\rERROR_VERSION\x10Z\x12\x1c\n\x18\x45RROR_UNCAUGHT_EXCEPTION\x10\x64\x62\x06proto3'
)

_ERRORCODE = _descriptor.EnumDescriptor(
  name='ErrorCode',
  full_name='jarvis.common.ErrorCode',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='SUCCESS', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ERROR_PARAM', index=1, number=10,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ERROR_AUTH', index=2, number=20,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ERROR_DATABASE', index=3, number=30,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ERROR_INTERNAL', index=4, number=40,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ERROR_NOTFOUND', index=5, number=50,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ERROR_ALREADYEXIST', index=6, number=60,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ERROR_STATUS', index=7, number=70,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ERROR_METHOD', index=8, number=80,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ERROR_VERSION', index=9, number=90,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ERROR_UNCAUGHT_EXCEPTION', index=10, number=100,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=117,
  serialized_end=343,
)
_sym_db.RegisterEnumDescriptor(_ERRORCODE)

ErrorCode = enum_type_wrapper.EnumTypeWrapper(_ERRORCODE)
SUCCESS = 0
ERROR_PARAM = 10
ERROR_AUTH = 20
ERROR_DATABASE = 30
ERROR_INTERNAL = 40
ERROR_NOTFOUND = 50
ERROR_ALREADYEXIST = 60
ERROR_STATUS = 70
ERROR_METHOD = 80
ERROR_VERSION = 90
ERROR_UNCAUGHT_EXCEPTION = 100



_ERRORRESPONSE = _descriptor.Descriptor(
  name='ErrorResponse',
  full_name='jarvis.common.ErrorResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='code', full_name='jarvis.common.ErrorResponse.code', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='message', full_name='jarvis.common.ErrorResponse.message', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=42,
  serialized_end=114,
)

_ERRORRESPONSE.fields_by_name['code'].enum_type = _ERRORCODE
DESCRIPTOR.message_types_by_name['ErrorResponse'] = _ERRORRESPONSE
DESCRIPTOR.enum_types_by_name['ErrorCode'] = _ERRORCODE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ErrorResponse = _reflection.GeneratedProtocolMessageType('ErrorResponse', (_message.Message,), {
  'DESCRIPTOR' : _ERRORRESPONSE,
  '__module__' : 'app.protos.common_pb2'
  # @@protoc_insertion_point(class_scope:jarvis.common.ErrorResponse)
  })
_sym_db.RegisterMessage(ErrorResponse)


# @@protoc_insertion_point(module_scope)
