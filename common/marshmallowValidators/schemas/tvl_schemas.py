from marshmallow import Schema, fields
from . import (
    validate_hex,
    validate_hex_40,
    validate_positive_integer,
    validate_non_negative_integer,
    validate_non_negative_float,
)


class PoolTvlDataSchema(Schema):
    # 'Required' -  if these are missing it will fail validation
    chainId = fields.String(required=True, validate=validate_hex)
    network = fields.String(required=True)
    base = fields.String(required=True, validate=validate_hex_40)
    quote = fields.String(required=True, validate=validate_hex_40)
    poolIdx = fields.Integer(required=True, validate=validate_non_negative_integer)
    tvl = fields.Float(required=True, validate=validate_non_negative_float)

    # Not 'Required' - if these are missing the validation will NOT fail
    #                  BUT these can not come back null or validation will fail
    time = fields.Integer(validate=validate_positive_integer)

    # Verbose non used could be deleted potentially later
    # Validation will never fail on these as they are allowed to not exist or be null
    latestTime = fields.Boolean(allow_none=True)
    baseSymbol = fields.String(allow_none=True)
    baseDecimals = fields.Integer(
        allow_none=True, validate=validate_non_negative_integer
    )
    quoteSymbol = fields.String(allow_none=True)
    quoteDecimals = fields.Integer(
        allow_none=True, validate=validate_non_negative_integer
    )


class PoolTvlSchema(Schema):
    data = fields.Nested(PoolTvlDataSchema)


class TvlSeriesDataSchema(Schema):
    time = fields.Integer(required=True, validate=validate_positive_integer)
    tvl = fields.Float(validate=validate_non_negative_float)
    method = fields.String(required=True)
    interpDistLower = fields.Integer(validate=validate_positive_integer)
    interpDistHigher = fields.Integer(validate=validate_positive_integer)
    interpBadness = fields.Float()


class SourceDataSchema(Schema):
    time = fields.Integer(validate=validate_positive_integer)
    tvl = fields.Float(validate=validate_non_negative_float)


class PoolTvlSeriesDataSchema(Schema):
    # 'Required' -  if these are missing it will fail validation
    chainId = fields.String(required=True, validate=validate_hex)
    network = fields.String(required=True)
    base = fields.String(required=True, validate=validate_hex_40)
    quote = fields.String(required=True, validate=validate_hex_40)
    poolIdx = fields.Integer(required=True, validate=validate_non_negative_integer)
    series = fields.Nested(TvlSeriesDataSchema, required=True, many=True)

    # Not 'Required' - if these are missing the validation will NOT fail
    #                  BUT these can not come back null or validation will fail
    resolution = fields.Integer(validate=validate_non_negative_integer)
    n = fields.Integer(validate=validate_non_negative_integer)
    latestTime = fields.Boolean()
    baseDecimals = fields.Integer(validate=validate_non_negative_integer)
    quoteDecimals = fields.Integer(validate=validate_non_negative_integer)
    timeStart = fields.Integer(validate=validate_positive_integer)
    timeEnd = fields.Integer(validate=validate_positive_integer)
    sourceData = fields.Nested(SourceDataSchema, many=True)

    # Not 'Required' can be null- if these are missing or null the validation will NOT fail
    baseSymbol = fields.String(allow_none=True)
    quoteSymbol = fields.String(allow_none=True)


class PoolTvlSeriesSchema(Schema):
    data = fields.Nested(PoolTvlSeriesDataSchema)
