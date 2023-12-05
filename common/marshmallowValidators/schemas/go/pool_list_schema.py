from marshmallow import Schema, fields

from .. import (
    validate_hex,
    validate_hex_40,
    validate_positive_integer,
    serverResponce,
)


class PoolListDataSchema(Schema):
    chainId = fields.String(required=True, validate=validate_hex)
    base = fields.String(required=True, validate=validate_hex_40)
    quote = fields.String(required=True, validate=validate_hex_40)
    poolIdx = fields.Integer(required=True, validate=validate_positive_integer)

class PoolListSchema(Schema):
    data = fields.Nested(PoolListDataSchema, many=True)
    #provenance = fields.Nested(serverResponce)

