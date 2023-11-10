from marshmallow import Schema, fields

from .. import (
    validate_hex_40,
    validate_positive_integer,
    serverResponce,
)


class ChainStatsDataSchema(Schema):
    tokenAddr = fields.String(required=True, validate=validate_hex_40)
    dexVolume = fields.Float(required=True)
    dexFees = fields.Float(required=True)
    dexTvl = fields.Float(required=True)
    latestTime = fields.Integer(required=True, validate=validate_positive_integer)


class ChainStatsSchema(Schema):
    data = fields.Nested(ChainStatsDataSchema, many=True)
    #provenance = fields.Nested(serverResponce)
