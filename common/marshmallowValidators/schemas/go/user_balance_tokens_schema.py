from marshmallow import Schema, fields, validate

from .. import (
    validate_hex,
    validate_hex_40,
    validate_positive_integer,
    serverResponce,
)


class UserBalanceTokensDataSchema(Schema):
    chainId = fields.String(required=True, validate=validate_hex)
    user = fields.String(required=True, validate=validate_hex_40)
    block = fields.Integer(validate=validate_positive_integer)
    tokens = fields.String(required=True, validate=validate_hex_40, many=True)


class UserBalanceTokensSchema(Schema):
    data = fields.Nested(UserBalanceTokensDataSchema)
    #provenance = fields.Nested(serverResponce)
