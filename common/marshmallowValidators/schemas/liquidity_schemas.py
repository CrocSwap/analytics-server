from marshmallow import Schema, fields
from . import (
    validate_hex,
    validate_hex_40,
    validate_positive_integer,
    validate_non_negative_integer,
    validate_float_constrained,
)


class LiquidityFeeDataSchema(Schema):
    # 'Required' -  if these are missing it will fail validation
    chainId = fields.String(required=True, validate=validate_hex)
    network = fields.String(required=True)
    base = fields.String(required=True, validate=validate_hex_40)
    quote = fields.String(required=True, validate=validate_hex_40)
    poolIdx = fields.Integer(required=True, validate=validate_positive_integer)
    time = fields.Integer(required=True, validate=validate_positive_integer)

    # Verbose non used could be deleted potentially later
    # Validation will never fail on these as they are allowed to not exist or be null
    latestTime = fields.Boolean()
    baseSymbol = fields.String(allow_none=True)
    baseDecimals = fields.Integer(validate=validate_non_negative_integer)
    quoteSymbol = fields.String(allow_none=True)
    quoteDecimals = fields.Integer(validate=validate_non_negative_integer)
    liquidityFee = fields.Float(required=True, validate=validate_float_constrained)


class LiquidityFeeSchema(Schema):
    data = fields.Nested(LiquidityFeeDataSchema)
