from marshmallow import Schema, ValidationError, fields, validates_schema
from . import (
    validate_hex,
    validate_hex_40,
    validate_positive_integer,
    validate_non_negative_float,
)


class PoolLimitOrderDataSchema(Schema):
    # 'Required' -  if these are missing it will fail validation
    base = fields.String(required=True, validate=validate_hex_40)
    quote = fields.String(required=True, validate=validate_hex_40)
    poolIdx = fields.Integer(required=True, validate=validate_positive_integer)
    chainId = fields.String(required=True, validate=validate_hex)
    isBid = fields.Boolean(required=True)
    bidTick = fields.Integer(required=True)
    askTick = fields.Integer(required=True)
    user = fields.String(required=True, validate=validate_hex_40)
    positionId = fields.String(required=True)

    positionLiq = fields.String(required=True)
    claimableLiq = fields.String(required=True)
    positionLiqBase = fields.String(required=True)
    positionLiqQuote = fields.String(required=True)
    claimableLiqBase = fields.String(required=True)
    claimableLiqQuote = fields.String(required=True)
    claimableLiqPivotTimes = fields.String(required=True)
    limitOrderIdentifier = fields.String(required=True)

    # 'Required' to exist -  if these are missing it will fail validation
    #                          BUT value can be null
    latestUpdateTime = fields.Integer(required=True, allow_none=True)

    # Not 'Required' - if these are missing the validation will NOT fail
    #                  BUT these can not come back null or validation will fail
    limitPriceDecimalCorrected = fields.Float()
    invLimitPriceDecimalCorrected = fields.Float()
    totalValueUSD = fields.Float()
    id = fields.String()
    claimableLiqTotalUSD = fields.Float()
    askTickPriceDecimalCorrected = fields.Float()
    askTickInvPriceDecimalCorrected = fields.Float()
    positionLiqBaseDecimalCorrected = fields.Float()
    positionLiqQuoteDecimalCorrected = fields.Float()
    claimableLiqBaseDecimalCorrected = fields.Float()
    claimableLiqQuoteDecimalCorrected = fields.Float()
    baseDecimals = fields.Integer()
    quoteDecimals = fields.Integer()

    # Not 'Required' can be null- if these are missing or null the validation will NOT fail
    timeFirstMint = fields.Integer(validate=validate_positive_integer, allow_none=True)
    quoteSymbol = fields.String(allow_none=True)
    baseSymbol = fields.String(allow_none=True)

    # Verbose non used could be deleted potentially later
    # Validation will never fail on these as they are allowed to not exist or be null
    network = fields.String(allow_none=True)
    block = fields.Integer(allow_none=True)
    poolHash = fields.String(allow_none=True)
    price = fields.Float(allow_none=True)
    time = fields.Integer(allow_none=True)
    updateType = fields.String(allow_none=True)
    deflator = fields.String(allow_none=True)
    concGrowth = fields.String(allow_none=True)
    pivotTime = fields.Integer(allow_none=True)
    latestUpdateBlock = fields.Integer(allow_none=True)
    pivotStorageSlot = fields.String(allow_none=True)
    merkleStorageSlot = fields.String(allow_none=True)
    bidTickPrice = fields.Float(allow_none=True)
    bidTickInvPrice = fields.Float(allow_none=True)
    bidTickPriceDecimalCorrected = fields.Float(allow_none=True)
    bidTickInvPriceDecimalCorrected = fields.Float(allow_none=True)
    askTickPrice = fields.Float(allow_none=True)
    askTickInvPrice = fields.Float(allow_none=True)
    cacheTime = fields.Integer(allow_none=True)
    cacheAge = fields.Integer(allow_none=True)
    limitPrice = fields.Float(allow_none=True)
    invLimitPrice = fields.Float(allow_none=True)
    ensResolution = fields.String(allow_none=True)
    ensResolutionAge = fields.Integer(allow_none=True)
    basePrice = fields.Float(allow_none=True)
    quotePrice = fields.Integer(allow_none=True)
    positionLiqBaseUSD = fields.Float(allow_none=True)
    positionLiqQuoteUSD = fields.Float(allow_none=True)
    positionLiqTotalUSD = fields.Float(allow_none=True)
    claimableLiqBaseUSD = fields.Float(allow_none=True)
    claimableLiqQuoteUSD = fields.Float(allow_none=True)

    # check if claimablePivotTimes is not empty if claimableLiq is non-zero
    @validates_schema
    def validate_claimable_pivot_times(self, data, **kwargs):
        if "claimableLiq" in data and data["claimableLiq"] != 0:
            if "claimablePivotTimes" in data and data["claimablePivotTimes"] == "":
                raise ValidationError(
                    "claimablePivotTimes can not be empty if claimableLiq is non-zero"
                )


class PoolLimitOrderSchema(Schema):
    data = fields.Nested(PoolLimitOrderDataSchema, many=True)
