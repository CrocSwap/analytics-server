from marshmallow import Schema, ValidationError, fields, validate, validates_schema
from . import (
    validate_hex,
    validate_hex_40,
    validate_positive_integer,
    validate_non_negative_integer,
)


class PoolPositionDataSchema(Schema):
    # 'Required' -  if these are missing it will fail validation
    user = fields.String(required=True, validate=validate_hex_40)
    bidTick = fields.Integer(required=True)
    askTick = fields.Integer(required=True)
    base = fields.String(required=True, validate=validate_hex_40)
    quote = fields.String(required=True, validate=validate_hex_40)
    poolIdx = fields.Integer(required=True, validate=validate_positive_integer)
    chainId = fields.String(required=True, validate=validate_hex)
    positionType = fields.String(
        required=True, validate=validate.OneOf(["knockout", "concentrated", "ambient"])
    )
    tx = fields.String(required=True, validate=validate_hex)

    # Not 'Required' - if these are missing the validation will NOT fail
    #                  BUT these can not come back null or validation will fail
    totalValueUSD = fields.Float()
    baseSymbol = fields.String()
    baseDecimals = fields.Integer(validate=validate_non_negative_integer)
    quoteSymbol = fields.String()
    quoteDecimals = fields.Integer(validate=validate_non_negative_integer)
    positionId = fields.String()
    network = fields.String()
    poolHash = fields.String(validate=validate_hex)
    block = fields.Integer(validate=validate_positive_integer)
    time = fields.Integer(validate=validate_positive_integer)
    positionLiq = fields.String()
    positionLiqBase = fields.String()
    positionLiqBaseDecimalCorrected = fields.Float()
    positionLiqQuote = fields.String()
    positionLiqQuoteDecimalCorrected = fields.Float()

    # Not 'Required' can be null- if these are missing or null the validation will NOT fail
    apy = fields.Float(allow_none=True)
    isBid = fields.Boolean(allow_none=True)
    timeFirstMint = fields.Integer(allow_none=True)
    limitOrderIdentifier = fields.String(allow_none=True)
    bidTickPrice = fields.Float(allow_none=True)
    bidTickInvPrice = fields.Float(allow_none=True)
    bidTickPriceDecimalCorrected = fields.Float(allow_none=True)
    bidTickInvPriceDecimalCorrected = fields.Float(allow_none=True)
    askTickPrice = fields.Float(allow_none=True)
    askTickInvPrice = fields.Float(allow_none=True)
    askTickPriceDecimalCorrected = fields.Float(allow_none=True)
    askTickInvPriceDecimalCorrected = fields.Float(allow_none=True)
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
    claimableLiqPivotTimes = fields.String(allow_none=True)

    # Verbose non used could be deleted potentially later
    # Validation will never fail on these as they are allowed to not exist or be null
    callSource = fields.String(allow_none=True)
    source = fields.String(allow_none=True)
    positionStorageSlot = fields.String(allow_none=True)
    pivotStorageSlot = fields.String(allow_none=True)
    merkleStorageSlot = fields.String(allow_none=True)
    cacheTime = fields.Integer(allow_none=True)
    cacheAge = fields.Integer(allow_none=True)
    deflator = fields.String(allow_none=True)
    concGrowth = fields.String(allow_none=True)
    tokenQtyAlert = fields.String(allow_none=True)
    updateType = fields.String(allow_none=True)
    pivotTime = fields.Integer(allow_none=True)
    latestUpdateBlock = fields.Integer(allow_none=True)
    latestUpdateTime = fields.Integer(allow_none=True)
    apyWeightedPrincipal = fields.Float(allow_none=True)
    apyTime = fields.Integer(allow_none=True)
    apyFees = fields.Float(allow_none=True)
    basePrice = fields.Float(allow_none=True)
    quotePrice = fields.Integer(allow_none=True)
    positionLiqBaseUSD = fields.Float(allow_none=True)
    positionLiqQuoteUSD = fields.Float(allow_none=True)
    positionLiqTotalUSD = fields.Float(allow_none=True)
    claimableLiqBaseUSD = fields.Float(allow_none=True)
    claimableLiqQuoteUSD = fields.Float(allow_none=True)
    claimableLiqTotalUSD = fields.Float(allow_none=True)
    ensResolution = fields.String(allow_none=True)
    ensResolutionAge = fields.Integer(allow_none=True)
    feesLiqBaseUSD = fields.Float(allow_none=True)
    feesLiqQuoteUSD = fields.Float(allow_none=True)
    feesLiqTotalUSD = fields.Float(allow_none=True)

    # check if ambient allow 0, concentrated or knockout must be non-0
    @validates_schema
    def validate_bid_ask(self, data, **kwargs):
        if "positionType" in data and data["positionType"] != "ambient":
            if "bidTick" in data and data["bidTick"] == 0 and data["askTick"] == 0:
                raise ValidationError("bidTick and askTick cannot both be 0")


class PoolPositionSchema(Schema):
    data = fields.Nested(PoolPositionDataSchema, many=True)
