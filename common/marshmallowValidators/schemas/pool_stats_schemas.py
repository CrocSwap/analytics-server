from marshmallow import Schema, ValidationError, fields, validates_schema

from . import (
    validate_positive_integer,
    validate_non_negative_integer,
    validate_non_negative_float,
    validate_hex,
    validate_hex_40,
)


class PoolStatsFreshDataSchema(Schema):
    # 'Required' -  if these are missing it will fail validation
    chainId = fields.String(required=True, validate=validate_hex)
    network = fields.String(required=True)
    base = fields.String(required=True, validate=validate_hex_40)
    quote = fields.String(required=True, validate=validate_hex_40)
    poolIdx = fields.Integer(required=True, validate=validate_positive_integer)

    lookback = fields.Integer(required=True, validate=validate_positive_integer)
    timeStart = fields.Integer(required=True, validate=validate_positive_integer)
    timeEnd = fields.Integer(required=True, validate=validate_positive_integer)
    tvl = fields.Float(required=True, validate=validate_non_negative_float)
    volume = fields.Float(required=True, validate=validate_non_negative_float)
    fees = fields.Float(required=True, validate=validate_non_negative_float)
    apy = fields.Float(required=True, validate=validate_non_negative_float)

    # Not 'Required' - if these are missing the validation will NOT fail
    #                  BUT these can not come back null or validation will fail
    volumeTotalFromCache = fields.Float(validate=validate_non_negative_float)
    volumeTotalFromNew = fields.Float(validate=validate_non_negative_float)
    volumeTotalCacheTime = fields.Integer(validate=validate_positive_integer)
    volumeTotalCacheAge = fields.Integer(validate=validate_positive_integer)

    latestTime = fields.Boolean()
    addTotalVolume = fields.Boolean()
    simpleCalc = fields.Boolean()
    returnSource = fields.Boolean()
    baseDecimals = fields.Integer(validate=validate_non_negative_integer)
    quoteDecimals = fields.Integer(validate=validate_non_negative_integer)

    # Not 'Required' can be null- if these are missing or null the validation will NOT fail
    volumeTotal = fields.Float(allow_none=True, validate=validate_non_negative_float)
    tokenUsed = fields.String(allow_none=True)
    baseSymbol = fields.String(allow_none=True)
    quoteSymbol = fields.String(allow_none=True)

    # check if needs to return extra fields based on passed in flags
    @validates_schema
    def validate_required_fields(self, data, **kwargs):
        if "addTotalVolume" in data and data["addTotalVolume"] is True:
            missing_fields = [
                f
                for f in (
                    "volumeTotalFromCache",
                    "volumeTotalFromNew",
                    "volumeTotalCacheTime",
                    "volumeTotalCacheAge",
                )
                if f not in data
            ]
            if missing_fields:
                raise ValidationError(f"Missing fields: {missing_fields}")


class PoolStatsFreshSchema(Schema):
    data = fields.Nested(PoolStatsFreshDataSchema)
