from marshmallow import Schema, fields

from .. import (
    validate_hex,
    validate_hex_40,
    validate_positive_integer,
    serverResponce,
)


class commonData(Schema):
    chainId = fields.String(required=True, validate=validate_hex)
    base = fields.String(required=True, validate=validate_hex_40)
    quote = fields.String(required=True, validate=validate_hex_40)
    poolIdx = fields.Integer(required=True, validate=validate_positive_integer)
    bidTick = fields.Integer(required=True)
    askTick = fields.Integer(required=True)
    isBid = fields.Boolean(required=True)
    user = fields.String(required=True, validate=validate_hex_40)
    pivotTime = fields.Integer(required=True)
    ambientLiq = fields.Float(required=True)
    concLiq = fields.Float(required=True)
    rewardLiq = fields.Float(required=True)
    liqRefreshTime = fields.Integer(required=True)
    limitOrderId = fields.String(required=True)
    claimableLiq = fields.Float(required=True)
    crossTime = fields.Integer(required=True, validate=validate_positive_integer)
    latestUpdateTime = fields.Integer(required=True)
    timeFirstMint = fields.Integer(required=True, validate=validate_positive_integer)


class PoolLimitOrdersSchema(Schema):
    data = fields.Nested(commonData, many=True)
    #provenance = fields.Nested(serverResponce)


class LimitStatsSchema(Schema):
    data = fields.Nested(commonData)
    #provenance = fields.Nested(serverResponce)


class UserLimitOrdersSchema(Schema):
    data = fields.Nested(commonData, many=True)
    #provenance = fields.Nested(serverResponce)
