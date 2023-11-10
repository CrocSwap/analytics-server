from marshmallow import Schema, fields

from .. import (
    validate_positive_integer,
    serverResponce,
)


class PoolCandlesDataSchema(Schema):
    priceOpen = fields.Float(required=True)
    priceClose = fields.Float(required=True)
    minPrice = fields.Float(required=True)
    maxPrice = fields.Float(required=True)
    volumeBase = fields.Float(required=True)
    volumeQuote = fields.Float(required=True)
    tvlBase = fields.Float(required=True)
    tvlQuote = fields.Float(required=True)
    feeRateOpen = fields.Float(required=True)
    feeRateClose = fields.Float(required=True)
    period = fields.Integer(required=True)
    time = fields.Integer(required=True, validate=validate_positive_integer)
    #once #5 on graphcache-go is in, this should be uncommented
    #isDecimalized = fields.Boolean()


class PoolCandlesSchema(Schema):
    data = fields.Nested(PoolCandlesDataSchema, many=True)
    #provenance = fields.Nested(serverResponce)
