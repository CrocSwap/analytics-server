from marshmallow import Schema, fields

from .. import (
    validate_hex,
    validate_hex_40,
    validate_positive_integer,
    serverResponce,
)


class PoolStatsDataSchema(Schema):
    latestTime = fields.Integer(required=True)
    baseTvl = fields.Float(required=True)
    quoteTvl = fields.Float(required=True)
    baseVolume = fields.Float(required=True)
    quoteVolume = fields.Float(required=True)
    baseFees = fields.Float(required=True)
    quoteFees = fields.Float(required=True)
    lastPriceSwap = fields.Float(required=True)
    lastPriceLiq = fields.Float(required=True)
    lastPriceIndic = fields.Float(required=True)
    feeRate = fields.Float(required=True)


class PoolStatsSchema(Schema):
    data = fields.Nested(PoolStatsDataSchema)
    #provenance = fields.Nested(serverResponce)
