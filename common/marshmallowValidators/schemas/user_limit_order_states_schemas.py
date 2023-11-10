from marshmallow import Schema, fields

from . import (
    validate_hex,
    validate_hex_40,
    validate_positive_integer_as_string,
    validate_positive_integer,
)


# See schema README for validation levels below
class UserLimitOrderStatesDataSchema(Schema):
    # 'Required'
    askTick = fields.Integer(required=True)
    base = fields.String(required=True, validate=validate_hex_40)
    bidTick = fields.Integer(required=True)
    chainId = fields.String(required=True, validate=validate_hex)
    isBid = fields.Boolean(required=True)
    poolIdx = fields.Integer(required=True, validate=validate_positive_integer)
    positionLiq = fields.String(
        required=True, validate=validate_positive_integer_as_string
    )
    quote = fields.String(required=True, validate=validate_hex_40)
    time = fields.Integer(required=True, validate=validate_positive_integer)
    user = fields.String(required=True, validate=validate_hex_40)

    # Not 'Required'
    block = fields.Integer(validate=validate_positive_integer)
    id = fields.String()
    network = fields.String()

    # Not 'Required' can be null
    ensResolution = fields.String(allow_none=True)

    # Verbose
    askTickInvPrice = fields.Float(allow_none=True)
    askTickInvPriceDecimalCorrected = fields.Float(allow_none=True)
    askTickPrice = fields.Float(allow_none=True)
    askTickPriceDecimalCorrected = fields.Float(allow_none=True)
    baseDecimals = fields.Integer(allow_none=True)
    basePrice = fields.Float(allow_none=True)
    baseSymbol = fields.String(allow_none=True)
    bidTickInvPrice = fields.Float(allow_none=True)
    bidTickInvPriceDecimalCorrected = fields.Float(allow_none=True)
    bidTickPrice = fields.Float(allow_none=True)
    bidTickPriceDecimalCorrected = fields.Float(allow_none=True)
    cacheAge = fields.Integer(allow_none=True)
    cacheTime = fields.Integer(allow_none=True)
    claimableLiq = fields.String(allow_none=True)
    claimableLiqBase = fields.String(allow_none=True)
    claimableLiqBaseDecimalCorrected = fields.Float(allow_none=True)
    claimableLiqBaseUSD = fields.Float(allow_none=True)
    claimableLiqPivotTimes = fields.String(allow_none=True)
    claimableLiqQuote = fields.String(allow_none=True)
    claimableLiqQuoteDecimalCorrected = fields.Float(allow_none=True)
    claimableLiqQuoteUSD = fields.Float(allow_none=True)
    claimableLiqTotalUSD = fields.Float(allow_none=True)
    concGrowth = fields.String(allow_none=True)
    deflator = fields.String(allow_none=True)
    ensResolutionAge = fields.Integer(allow_none=True)
    invLimitPrice = fields.Float(allow_none=True)
    invLimitPriceDecimalCorrected = fields.Float(allow_none=True)
    latestUpdateBlock = fields.Integer(allow_none=True)
    latestUpdateTime = fields.Integer(allow_none=True)
    limitOrderIdentifier = fields.String(allow_none=True)
    limitPrice = fields.Float(allow_none=True)
    limitPriceDecimalCorrected = fields.Float(allow_none=True)
    merkleStorageSlot = fields.String(allow_none=True)
    pivotStorageSlot = fields.String(allow_none=True)
    pivotTime = fields.Integer(allow_none=True)
    poolHash = fields.String(allow_none=True)
    positionId = fields.String(allow_none=True)
    positionLiqBase = fields.String(allow_none=True)
    positionLiqBaseDecimalCorrected = fields.Float(allow_none=True)
    positionLiqBaseUSD = fields.Float(allow_none=True)
    positionLiqQuote = fields.String(allow_none=True)
    positionLiqQuoteDecimalCorrected = fields.Float(allow_none=True)
    positionLiqQuoteUSD = fields.Float(allow_none=True)
    positionLiqTotalUSD = fields.Float(allow_none=True)
    positionStorageSlot = fields.String(allow_none=True)
    price = fields.Float(allow_none=True)
    quoteDecimals = fields.Integer(allow_none=True)
    quotePrice = fields.Integer(allow_none=True)
    quoteSymbol = fields.String(allow_none=True)
    timeFirstMint = fields.Integer(allow_none=True)
    totalValueUSD = fields.Float(allow_none=True)
    updateType = fields.String(allow_none=True)


class UserLimitOrderStatesSchema(Schema):
    data = fields.Nested(UserLimitOrderStatesDataSchema, many=True)
