from marshmallow import Schema, fields
from . import (
    validate_positive_integer,
    validate_non_negative_integer,
    validate_non_negative_float,
    validate_positive_float,
)


class ChainStatsFreshDataSchema(Schema):
    network = fields.String(required=True)
    lookback = fields.Integer(required=True, validate=validate_non_negative_integer)
    numPools = fields.Integer(required=True, validate=validate_non_negative_integer)
    timeStart = fields.Integer(required=True, validate=validate_positive_integer)
    timeEnd = fields.Integer(required=True, validate=validate_positive_integer)
    tvl = fields.Float(required=True, validate=validate_non_negative_float)
    volume = fields.Float(required=True, validate=validate_non_negative_float)
    fees = fields.Float(required=True, validate=validate_non_negative_float)
    apy = fields.Float(required=True, validate=validate_non_negative_float)


class ChainStatsFreshSchema(Schema):
    data = fields.Nested(ChainStatsFreshDataSchema)


class ChainStatsCachedDataSchema(Schema):
    network = fields.String(required=True)
    time = fields.Integer(required=True, validate=validate_positive_integer)
    cacheTime = fields.Integer(required=True, validate=validate_positive_integer)
    tvl = fields.Float(required=True, validate=validate_non_negative_float)
    cacheTimeDiff = fields.Integer(validate=validate_positive_integer)
    volumeHour = fields.Float(validate=validate_non_negative_float)
    volumeDay = fields.Float(validate=validate_positive_float)
    volumeTotal = fields.Float(validate=validate_positive_float)
    feesHour = fields.Float(validate=validate_non_negative_float)
    feesDay = fields.Float(validate=validate_positive_float)
    feesTotal = fields.Float(validate=validate_non_negative_float)
    apyFromLastHour = fields.Float(validate=validate_non_negative_float)
    apyFromLastDay = fields.Float(validate=validate_non_negative_float)


class ChainStatsCachedSchema(Schema):
    data = fields.Nested(ChainStatsCachedDataSchema)
