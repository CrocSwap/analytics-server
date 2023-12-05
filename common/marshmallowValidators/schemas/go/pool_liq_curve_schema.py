from marshmallow import Schema, fields, validate

from .. import (
    validate_positive_integer,
    serverResponce,
)


class LiquidityBumpsDataSchema(Schema):
    bumpTick = fields.Integer(required=True, validate=validate_positive_integer)
    liquidityDelta = fields.Float(required=True)
    knockoutBidLiq = fields.Float(required=True)
    knockoutAskLiq = fields.Float(required=True)
    knockoutBidWidth = fields.Float(required=True)
    knockoutAskWidth = fields.Float(required=True)
    latestUpdateTime = fields.Integer(required=True, validate=validate_positive_integer)


class PoolLiqCurveDataSchema(Schema):
    ambientLiq = fields.Float(required=True)
    liquidityBumps = fields.Nested(LiquidityBumpsDataSchema, many=True)


class PoolLiqCurveSchema(Schema):
    data = fields.Nested(PoolLiqCurveDataSchema)
    #provenance = fields.Nested(serverResponce)
