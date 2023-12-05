from marshmallow import Schema, fields, validate

from .. import (
    validate_hex,
    validate_hex_40,
    validate_hex_64,
    validate_positive_integer,
    validate_postion_type,
    serverResponce,
)


class CommonDataSchema(Schema):
    chainId = fields.String(required=True, validate=validate_hex)
    base = fields.String(required=True, validate=validate_hex_40)
    quote = fields.String(required=True, validate=validate_hex_40)
    poolIdx = fields.Integer(required=True, validate=validate_positive_integer)
    bidTick = fields.Integer(required=True)
    askTick = fields.Integer(required=True)
    isBid = fields.Boolean(required=True)
    user = fields.String(required=True, validate=validate_hex_40)
    timeFirstMint = fields.Integer(required=True)
    latestUpdateTime = fields.Integer(required=True)
    lastMintTx = fields.String(required=True, validate=validate_hex_64)
    firstMintTx = fields.String(required=True, validate=validate_hex_64)
    positionType = fields.String(validate=validate_postion_type)
    ambientLiq = fields.Float(required=True)
    concLiq = fields.Float(required=True)
    rewardLiq = fields.Float(required=True)
    liqRefreshTime = fields.Integer(required=True)
    aprDuration = fields.Integer(required=True)
    aprPostLiq = fields.Integer(required=True)
    aprContributedLiq = fields.Integer(required=True)
    aprEst = fields.Float(required=True)
    positionId = fields.String(required=True)


class UserPoolPositionsSchema(Schema):
    data = fields.Nested(CommonDataSchema, many=True)
    #provenance = fields.Nested(serverResponce)


class UserPoolLimitOrdersSchema(Schema):
    data = fields.Nested(CommonDataSchema, many=True)
    #provenance = fields.Nested(serverResponce)


class UserPositionsSchema(Schema):
    data = fields.Nested(CommonDataSchema, many=True)
    #provenance = fields.Nested(serverResponce)


class PositionStatsSchema(Schema):
    data = fields.Nested(CommonDataSchema)
    #provenance = fields.Nested(serverResponce)
