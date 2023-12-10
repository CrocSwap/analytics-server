from functools import partial

from common.ServiceBase import ServiceBase

from .CrocQueryProxy import CrocQueryProxy as Query
from .marshmallowValidators.schemas.go import (
    ChainStatsSchema,
    LimitStatsSchema,
    PoolCandlesSchema,
    PoolLimitOrdersSchema,
    PoolLiqCurveSchema,
    PoolListSchema,
    PoolPositionApyLeadersSchema,
    PoolPositionsSchema,
    PoolStatsSchema,
    PoolTxsSchema,
    PositionStatsSchema,
    UserBalanceTokensSchema,
    UserLimitOrdersSchema,
    UserPoolLimitOrdersSchema,
    UserPoolPositionsSchema,
    UserPositionsSchema,
    UserTxsSchema,
)


class SchemaValidator(ServiceBase):
    def __init__(self, queryProxy: Query, config: dict, env: dict, server_config: dict):
        super().__init__(queryProxy, config, env, server_config)
        self.marshmallow_schema_map = {
            "chain_stats": ChainStatsSchema(),
            "pool_candles": PoolCandlesSchema(),
            "limit_stats": LimitStatsSchema(),
            "pool_limit_orders": PoolLimitOrdersSchema(),
            "pool_liq_curve": PoolLiqCurveSchema(),
            "pool_list": PoolListSchema(),
            "pool_position_apy_leaders": PoolPositionApyLeadersSchema(),
            "pool_positions": PoolPositionsSchema(),
            "pool_stats": PoolStatsSchema(),
            "pool_txs": PoolTxsSchema(),
            "position_stats": PositionStatsSchema(),
            "user_balance_tokens": UserBalanceTokensSchema(),
            "user_limit_orders": UserLimitOrdersSchema(),
            "user_pool_limit_orders": UserPoolLimitOrdersSchema(),
            "user_pool_positions": UserPoolPositionsSchema(),
            "user_positions": UserPositionsSchema(),
            "user_txs": UserTxsSchema(),
        }

    def validSchema(self, data, endpoint):
        if not endpoint in self.marshmallow_schema_map:
            return {
                "valid": False,
                "message": endpoint + " missing from validation",
                "retVal": errors,
            }
        else:
            schema = self.marshmallow_schema_map.get(endpoint)

            result = schema.dump(data)
            errors = schema.validate(result)
            if len(errors) == 0:
                return {
                    "valid": True,
                    "message": endpoint + "passes validation",
                    "retVal": errors,
                }
            else:
                return {
                    "valid": False,
                    "message": endpoint + " failedpasses validation",
                    "retVal": errors,
                }

    def __getattr__(self, funcName):
        endpoints = list(self.marshmallow_schema_map.keys())
        if funcName.startswith("validate_endpoint_"):
            endpoint = funcName.replace("validate_endpoint_", "")
            if endpoint in endpoints:
                return self.validSchema
                # return partial(self.validate_schema, endpoint=endpoint) # -.o , love when I get to do this. And I didn't need it.
        raise AttributeError(
            f"'{type(self).__name__}' object has no attribute '{funcName}'"
        )
