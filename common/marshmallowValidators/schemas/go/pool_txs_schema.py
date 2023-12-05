from marshmallow import Schema, fields, validate

from .. import (
    validate_hex,
    validate_hex_40,
    validate_hex_64,
    validate_positive_integer,
    validate_postion_type,
    serverResponce,
)


# See schema README for validation levels below
class PoolTxsDataSchema(Schema):
    blockNum = fields.Integer(required=True)
    txHash = fields.String(required=True, validate=validate_hex_64)
    txTime = fields.Integer(required=True, validate=validate_positive_integer)
    user = fields.String(required=True, validate=validate_hex_40)
    chainId = fields.String(required=True, validate=validate_hex)
    base = fields.String(required=True, validate=validate_hex_40)
    quote = fields.String(required=True, validate=validate_hex_40)
    poolIdx = fields.Integer(required=True, validate=validate_positive_integer)
    baseFlow = fields.Integer(required=True)
    quoteFlow = fields.Integer(required=True)
    entityType = fields.String(validate=validate_postion_type)
    changeType = fields.String(validate=validate_postion_type)
    positionType = fields.String(validate=validate_postion_type)
    bidTick = fields.Integer(required=True)
    askTick = fields.Integer(required=True)
    isBuy = fields.Boolean(required=True)
    inBaseQty = fields.Boolean(required=True)
    txId = fields.String(required=True, validate=validate_hex_64)


class PoolTxsSchema(Schema):
    data = fields.Nested(PoolTxsDataSchema, many=True)
    #provenance = fields.Nested(serverResponce)
