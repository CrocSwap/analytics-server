from marshmallow import Schema, fields, validate

from . import (
    validate_hex,
    validate_hex_40,
    validate_non_negative_integer,
    validate_positive_integer,
    validate_positive_integer_as_string,
)


# See schema README for validation levels below
class UserPositionsDataSchema(Schema):
    # 'Required'
    askTick = fields.Integer(required=True)
    base = fields.String(required=True, validate=validate_hex_40)
    bidTick = fields.Integer(required=True)
    chainId = fields.String(required=True, validate=validate_hex)
    poolIdx = fields.Integer(required=True, validate=validate_positive_integer)
    positionLiq = fields.String(
        required=True, validate=validate_positive_integer_as_string
    )
    quote = fields.String(required=True, validate=validate_hex_40)
    time = fields.Integer(required=True, validate=validate_positive_integer)
    tx = fields.String(required=True)
    user = fields.String(required=True, validate=validate_hex_40)

    # Not 'Required'
    askTickInvPrice = fields.Float()
    askTickInvPriceDecimalCorrected = fields.Float()
    askTickPrice = fields.Float()
    askTickPriceDecimalCorrected = fields.Float()
    baseDecimals = fields.Integer(validate=validate_non_negative_integer)
    basePrice = fields.Float()
    baseSymbol = fields.String()
    block = fields.Integer(validate=validate_positive_integer)
    bidTickPrice = fields.Float()
    bidTickInvPrice = fields.Float()
    bidTickPriceDecimalCorrected = fields.Float()
    bidTickInvPriceDecimalCorrected = fields.Float()
    cacheAge = fields.Integer()
    cacheTime = fields.Integer()
    callSource = fields.String()
    claimableLiqBaseUSD = fields.Float()
    claimableLiqPivotTimes = fields.String()
    claimableLiqQuoteUSD = fields.Float()
    claimableLiqTotalUSD = fields.Float()
    concGrowth = fields.String()
    deflator = fields.String()
    feesLiqBaseUSD = fields.Float()
    feesLiqQuoteUSD = fields.Float()
    feesLiqTotalUSD = fields.Float()
    isBid = fields.Boolean()
    limitOrderIdentifier = fields.String()
    network = fields.String()
    poolHash = fields.String(validate=validate_hex)
    positionId = fields.String()
    positionLiqBase = fields.String()
    positionLiqBaseDecimalCorrected = fields.Float()
    positionLiqBaseUSD = fields.Float()
    positionLiqQuote = fields.String()
    positionLiqQuoteDecimalCorrected = fields.Float()
    positionLiqQuoteUSD = fields.Float()
    positionLiqTotalUSD = fields.Float()
    positionType = fields.String(
        validate=validate.OneOf(["concentrated", "knockout", "ambient"])
    )
    quoteDecimals = fields.Integer(validate=validate_non_negative_integer)
    quotePrice = fields.Integer()
    quoteSymbol = fields.String()
    source = fields.String()
    totalValueUSD = fields.Float()
    updateType = fields.String()

    # Not 'Required' can be null
    timeFirstMint = fields.Integer(allow_none=True, validate=validate_positive_integer)

    # Verbose
    apy = fields.Float(allow_none=True)
    apyFees = fields.Float(allow_none=True)
    apyTime = fields.Integer(allow_none=True)
    apyWeightedPrincipal = fields.Float(allow_none=True)
    claimableLiq = fields.String(allow_none=True)
    claimableLiqBase = fields.String(allow_none=True)
    claimableLiqBaseDecimalCorrected = fields.Float(allow_none=True)
    claimableLiqQuote = fields.String(allow_none=True)
    claimableLiqQuoteDecimalCorrected = fields.Float(allow_none=True)
    feesLiq = fields.String(allow_none=True)
    feesLiqBase = fields.String(allow_none=True)
    feesLiqBaseDecimalCorrected = fields.Float(allow_none=True)
    feesLiqQuote = fields.String(allow_none=True)
    feesLiqQuoteDecimalCorrected = fields.Float(allow_none=True)
    latestUpdateBlock = fields.Integer(allow_none=True)
    latestUpdateTime = fields.Integer(allow_none=True)
    merkleStorageSlot = fields.String(allow_none=True)
    pivotStorageSlot = fields.String(allow_none=True, validate=validate_hex)
    pivotTime = fields.Integer(allow_none=True)
    positionStorageSlot = fields.String(allow_none=True)


class UserPositionsSchema(Schema):
    data = fields.Nested(UserPositionsDataSchema, many=True)
