from marshmallow import Schema, fields, validate, validates_schema, ValidationError

from . import (
    validate_hex,
    validate_hex_40,
    validate_hex_64,
    validate_positive_integer,
)

# See schema README for validation levels below


class PoolRecentChangesDataSchema(Schema):
    # 'Required'
    base = fields.String(required=True, validate=validate_hex_40)
    quote = fields.String(required=True, validate=validate_hex_40)
    poolIdx = fields.Integer(required=True, validate=validate_positive_integer)
    chainId = fields.String(required=True, validate=validate_hex)
    time = fields.Integer(required=True, validate=validate_positive_integer)
    tx = fields.String(required=True, validate=validate_hex_64)
    user = fields.String(required=True, validate=validate_hex_40)
    entityType = fields.String(
        required=True, validate=validate.OneOf(["limitOrder", "liqchange", "swap"])
    )

    # Conditional 'Required'
    isBid = fields.Boolean()
    isBuy = fields.Boolean()

    positionLiq = fields.String(allow_none=True)
    bidTick = fields.Integer()
    askTick = fields.Integer()
    claimableLiq = fields.String(allow_none=True)

    @validates_schema
    def validate_required_fields(self, data, **kwargs):
        if "entityType" in data:
            if data["entityType"] == "limitOrder":
                missing_fields = [
                    f
                    for f in (
                        "isBid",
                        "positionLiq",
                        "bidTick",
                        "askTick",
                        "claimableLiq",
                    )
                    if f not in data
                ]
                if missing_fields:
                    raise ValidationError(
                        f"Missing fields for limitOrder: {missing_fields}"
                    )
            if data["entityType"] == "swap" and "isBuy" not in data:
                raise ValidationError("Missing field isBuy for swap")

    # Not 'Required'
    id = fields.String()
    callIndex = fields.Integer()
    network = fields.String()
    block = fields.Integer(validate=validate_positive_integer)
    transactionIndex = fields.Integer()

    # Not 'Required' can be null
    ensResolution = fields.String(allow_none=True)

    # Verbose
    latestUpdateBlock = fields.Integer(allow_none=True)
    latestUpdateTime = fields.Integer(allow_none=True)
    liq = fields.String(allow_none=True)
    positionLiqBaseUSD = fields.Float(allow_none=True)
    positionLiqQuoteUSD = fields.Float(allow_none=True)
    positionLiqTotalUSD = fields.Float(allow_none=True)
    positionLiqBase = fields.String(allow_none=True)
    positionLiqBaseDecimalCorrected = fields.Float(allow_none=True)
    positionLiqQuote = fields.String(allow_none=True)
    positionLiqQuoteDecimalCorrected = fields.Float(allow_none=True)
    claimableLiqBaseUSD = fields.Float(allow_none=True)
    claimableLiqQuoteUSD = fields.Float(allow_none=True)
    claimableLiqTotalUSD = fields.Float(allow_none=True)
    pivotTime = fields.Integer(allow_none=True)
    apy = fields.Float(allow_none=True)
    apyWeightedPrincipal = fields.Float(allow_none=True)
    apyTime = fields.Integer(allow_none=True)
    apyFees = fields.Float(allow_none=True)
    bidTickPrice = fields.Float(allow_none=True)
    bidTickInvPrice = fields.Float(allow_none=True)
    bidTickPriceDecimalCorrected = fields.Float(allow_none=True)
    bidTickInvPriceDecimalCorrected = fields.Float(allow_none=True)
    askTickPrice = fields.Float(allow_none=True)
    askTickInvPrice = fields.Float(allow_none=True)
    askTickPriceDecimalCorrected = fields.Float(allow_none=True)
    askTickInvPriceDecimalCorrected = fields.Float(allow_none=True)
    feesLiqBaseUSD = fields.Float(allow_none=True)
    feesLiqQuoteUSD = fields.Float(allow_none=True)
    feesLiqTotalUSD = fields.Float(allow_none=True)
    feesLiq = fields.String(allow_none=True)
    feesLiqBase = fields.String(allow_none=True)
    feesLiqBaseDecimalCorrected = fields.Float(allow_none=True)
    feesLiqQuote = fields.String(allow_none=True)
    feesLiqQuoteDecimalCorrected = fields.Float(allow_none=True)
    poolHash = fields.String(allow_none=True)
    inBaseQty = fields.Boolean(allow_none=True)
    qty = fields.String(allow_none=True)
    limitPrice = fields.Float(allow_none=True)
    minOut = fields.String(allow_none=True)
    baseFlow = fields.String(allow_none=True)
    quoteFlow = fields.String(allow_none=True)
    callSource = fields.String(allow_none=True)
    source = fields.String(allow_none=True)
    # Some possible values of dex: croc, ?
    dex = fields.String(allow_none=True)
    baseSymbol = fields.String(allow_none=True)
    baseDecimals = fields.Integer(allow_none=True)
    quoteSymbol = fields.String(allow_none=True)
    quoteDecimals = fields.Integer(allow_none=True)
    price = fields.Float(allow_none=True)
    invPrice = fields.Float(allow_none=True)
    priceDecimalCorrected = fields.Float(allow_none=True)
    invPriceDecimalCorrected = fields.Float(allow_none=True)
    baseFlowDecimalCorrected = fields.Float(allow_none=True)
    quoteFlowDecimalCorrected = fields.Float(allow_none=True)
    # Some possible values of valueTokenUsed: quote, base
    valueTokenUsed = fields.String(allow_none=True)
    valuePriceUsed = fields.Integer(allow_none=True)
    valueUSD = fields.Float(allow_none=True)
    ensResolutionAge = fields.Integer(allow_none=True)
    entityId = fields.String(allow_none=True)
    timeFirstMint = fields.Integer(allow_none=True)
    tokenQtyAlert = fields.String(allow_none=True)
    totalFlowUSD = fields.Float(allow_none=True)
    totalValueUSD = fields.Integer(allow_none=True)
    # Some possible values of changeType: mint, recover, burn, harvest
    changeType = fields.String(allow_none=True)
    claimableLiqBase = fields.String(allow_none=True)
    claimableLiqBaseDecimalCorrected = fields.Float(allow_none=True)
    claimableLiqQuote = fields.String(allow_none=True)
    claimableLiqQuoteDecimalCorrected = fields.Float(allow_none=True)
    concGrowth = fields.String(allow_none=True)
    deflator = fields.String(allow_none=True)
    cacheAge = fields.Integer(allow_none=True)
    cacheTime = fields.Integer(allow_none=True)
    baseFlowUSD = fields.Float(allow_none=True)
    basePrice = fields.Float(allow_none=True)
    positionId = fields.String(allow_none=True)
    positionStorageSlot = fields.String(allow_none=True)
    # Some possible values of positionType: concentrated, ambient, knockout
    positionType = fields.String(allow_none=True)
    quoteFlowUSD = fields.Float(allow_none=True)
    quotePrice = fields.Integer(allow_none=True)
    # Some possible values of updateType: irregular_from_annotation, regular
    updateType = fields.String(allow_none=True)
    claimableLiqPivotTimes = fields.String(allow_none=True)
    invLimitPrice = fields.Float(allow_none=True)
    invLimitPriceDecimalCorrected = fields.Float(allow_none=True)
    limitOrderIdentifier = fields.String(allow_none=True)
    limitPriceDecimalCorrected = fields.Float(allow_none=True)
    merkleStorageSlot = fields.String(allow_none=True)
    pivotStorageSlot = fields.String(allow_none=True)


class PoolRecentChangesSchema(Schema):
    data = fields.Nested(PoolRecentChangesDataSchema, many=True)
