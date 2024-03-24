import time

import requests
from exceptions.MissingParameterException import MissingParameterException

from .DataClasses import BasePoolStats, ExtendedPoolStats, Pool, PoolTx, ServiceConfig
from .ServiceBase import ServiceBase
from .ServiceFactory import ServiceFactory

service_get_pool_by_id_subgraph = ServiceConfig(
    {
        "chain_id": "0x1",
        "supported_chain_ids": ["0x1", "0xaa36a7"],
        "results": {
            "value": {
                "cache": {
                    "duration": 86400,  # 1 day
                    "path": "./services/complete_pool_stats/pool_info_results.json",
                },
                "module": "common.ServiceCompletePoolStats",
                "function": "get_pool_by_id_subgraph",
                "params": ["pool_id"],
            }
        },
    }
)


class ServiceCompletePoolStats(ServiceBase):
    #
    #
    # INTERNAL methods. Not exposed though API, and use internal DataClasses to enforce structure.
    #
    #
    def get_pool_list_subgraph(self) -> list[Pool]:
        """
        Get the list of pools, their base and quote tokens and other basic information from subgraph query
        """
        query = """
        query GetCreationTimeByPool {
          pools {
            id
            timeCreate
            base
            quote
            poolIdx
          }
        }
        """
        data = self.crocQuery.query_subgraph(query)
        pools_data = data.get("data", {}).get("pools")
        ret_data: list[Pool] = []
        for data in pools_data:
            ret_data.append(
                Pool(
                    id=data["id"],
                    chain_id=self.crocQuery.chain_id,
                    timeCreated=data["timeCreate"],
                    quote=data["quote"],
                    base=data["base"],
                    pool_idx=data["poolIdx"],
                )
            )
        return ret_data

    def get_pool_by_id_subgraph(self, pool_id: str) -> Pool:
        """
        Get pool data by its id from subgraph query
        """
        query = f"""
        query GetPoolById {{
          pool(id: "{pool_id}") {{
            id
            timeCreate
            base
            quote
            poolIdx
          }}
        }}
        """

        data = self.crocQuery.query_subgraph(query)
        pool_data = data.get("data", {}).get("pool")

        if not pool_data:
            raise ValueError(f"Error: No pool found with id: {pool_id}")
        return pool_data

    def get_pool_by_id_subgraph_cached(self, pool_id) -> Pool:
        results = ServiceFactory.invoke_dynamic_service(
            {"pool_id": pool_id},
            config=service_get_pool_by_id_subgraph,
            network=self.get_network_config(),
            include_data="0",
        )
        pool_data = results["value"]
        return Pool(
            id=pool_data["id"],
            chain_id=self.crocQuery.chain_id,
            timeCreated=pool_data["timeCreate"],
            quote=pool_data["quote"],
            base=pool_data["base"],
            pool_idx=pool_data["poolIdx"],
        )

    def invoke_pool_stats_service(self, pool: Pool) -> BasePoolStats:
        args = {
            "chain_id": pool["chain_id"],
            "base": pool["base"],
            "quote": pool["quote"],
            "pool_idx": pool["pool_idx"],
        }
        # Use the original config environment
        result = ServiceFactory.invoke_registered_service(
            args, "base_pool_stats", pool["chain_id"], 0
        )
        pool_stats = result["value"]
        return BasePoolStats(
            **pool_stats,
            id=pool["id"],
        )

    def get_pool_stats(
        self, chain_id: str, base: str, quote: str, pool_idx: str
    ) -> BasePoolStats:
        """
        Calculate PoolStats given a Pool, and return the updated Pool object
        """
        params = {
            "chainId": chain_id,
            "base": base,
            "quote": quote,
            "poolIdx": pool_idx,
        }
        GCGO_POOL_STATS = self.get_network_config()["GCGO_POOL_STATS"]
        response = requests.get(GCGO_POOL_STATS, params=params)  # FIXME: timeout
        if response.status_code != 200:
            raise ValueError(
                f"Error: Failed to get pool stats from GCGO. Status code: {response.status_code}"
            )

        data = response.json()
        resp_data = data.get("data", {})
        return resp_data

    def get_day_pool_txs(self, pool: Pool) -> list[PoolTx]:
        args = {
            "chain_id": pool["chain_id"],
            "base": pool["base"],
            "quote": pool["quote"],
            "pool_idx": pool["pool_idx"],
            "n_days": 1,
        }
        result = ServiceFactory.invoke_registered_service(
            args, "pool_txs", pool["chain_id"], 0
        )
        all_transactions = result["value"]
        return [PoolTx(**all_transaction) for all_transaction in all_transactions]

    def calculate_extended_stats_for_pool_txs(
        self, txs: list[PoolTx], start_timestamp: int, end_timestamp: int
    ) -> ExtendedPoolStats:
        """Calculate statistics based on a given list of pool transactions.

        NOTE: will not handle if transactions are for multiple pools.
        """
        first_block_number, last_block_number = None, None
        last_timestamp, first_timestamp = None, None
        swap_volume: int = 0
        buy: int = 0
        sell: int = 0
        n_txs: int = 0

        for tx in txs:
            block_number = tx["blockNum"]
            timestamp = tx["txTime"]

            # Only accumulate tx that is within the start_timestamp and end_timestamp
            if timestamp < start_timestamp or timestamp > end_timestamp:
                continue

            if tx["entityType"] == "swap":
                swap_volume += abs(
                    tx["baseFlow"]
                )  # NOTE (#106): negative baseFlow implies removal of baseToken, not less volume
                if tx["isBuy"]:
                    buy += 1
                else:
                    sell += 1
                n_txs += 1

            if block_number is not None:
                if last_block_number is None or block_number > last_block_number:
                    last_block_number = block_number
                if first_block_number is None or block_number < first_block_number:
                    first_block_number = block_number
            if timestamp is not None:
                if last_timestamp is None or timestamp > last_timestamp:
                    last_timestamp = timestamp
                if first_timestamp is None or timestamp < first_timestamp:
                    first_timestamp = timestamp

        eps = ExtendedPoolStats(
            txTimeRange=[first_timestamp, last_timestamp],
            blockNumRange=[first_block_number, last_block_number],
            swapVolume=swap_volume,
            n_txs=n_txs,
            buy=buy,
            sell=sell,
        )
        return eps

    #
    #
    # API Published Services (through API Interface. See /services/complete_pool_stats/)
    #  - Each takes a well defined set of parameters, which are exposed via the API handler (currently positional args, but can change)
    #
    #

    def get_other_return(self, arg):
        return "¯\_(ツ)_/¯ I am a string example and echo arg: " + str(arg)

    def get_token_metadata(self, token_addr_set):
        args = {"token_addresses": token_addr_set}
        result = ServiceFactory.invoke_registered_service(
            args, "token_metadata", self.crocQuery.chain_id, 0
        )
        return result

    def get_complete_pool_stats_by_pool(self, pool: Pool):
        token_addr_set = set([pool["base"]] + [pool["quote"]])

        # Make a series of requests to coingecko where we get
        # TODO, implement as a secondary query, which will automagically get cached by the CLI according to a caching policy
        token_metadata_results = self.get_token_metadata(list(token_addr_set))
        token_metadata = token_metadata_results["value"][0]

        stats = self.invoke_pool_stats_service(pool)
        txs = self.get_day_pool_txs(pool)

        # Current timestamp
        current_time = int(time.time())
        stats_5m = self.calculate_extended_stats_for_pool_txs(
            txs, current_time - 5 * 60, current_time
        )
        stats_1h = self.calculate_extended_stats_for_pool_txs(
            txs, current_time - 60 * 60, current_time
        )
        stats_4h = self.calculate_extended_stats_for_pool_txs(
            txs, current_time - 4 * 60 * 60, current_time
        )
        stats_24h = self.calculate_extended_stats_for_pool_txs(
            txs, current_time - 24 * 60 * 60, current_time
        )

        base_meta = token_metadata.get(pool["base"], {})
        quote_meta = token_metadata.get(pool["quote"], {})
        quote_meta_market = base_meta.get("market_data", {})
        base_meta_market = quote_meta.get("market_data", {})
        base_symbol = base_meta.get("symbol", "UNKNOWN")
        quote_symbol = quote_meta.get("symbol", "UNKNOWN")
        friendly_pool_name = f"{base_symbol}x{quote_symbol}"
        CURRENCY = self.get_network_config()["CURRENCY"]

        return {
            "friendly_pool_name": friendly_pool_name,
            "pool_id": pool["id"],
            "base_addr": pool["base"],
            "quote_addr": pool["quote"],
            "base": base_meta.get("symbol", "UNKNOWN"),
            "quote": quote_meta.get("symbol", "UNKNOWN"),
            "quote_market_cap": quote_meta_market.get("market_cap", {}).get(
                CURRENCY, "UNKNOWN"
            ),
            "base_market_cap": base_meta_market.get("market_cap", {}).get(
                CURRENCY, "UNKNOWN"
            ),
            "quote_fully_diluted_valuation": quote_meta_market.get(
                "fully_diluted_valuation", {}
            ).get(CURRENCY, "UNKNOWN"),
            "base_fully_diluted_valuation": base_meta_market.get(
                "fully_diluted_valuation", {}
            ).get(CURRENCY, "UNKNOWN"),
            "baseTvl": stats["baseTvl"],
            "total_fees": stats["quoteFees"] + stats["baseFees"],
            "time_based_stats": {
                "5m": stats_5m,
                "1h": stats_1h,
                "4h": stats_4h,
                "24h": stats_24h,
            },
        }

    def get_complete_pool_stats(
        self,
        pool_id: str = None,
        base: str = None,
        quote: str = None,
        pool_idx: str = None,
    ):
        # TODO Look up top level pool data, likely from a pool_info endpoint, which could be cached according to a relevant caching policy (if implemented as another endpoint), or via an internal function (if we want to do a new query every refresh of this endpoint).
        coingecko_api_key = self.get_server_config()["COIN_GECKO"]
        if not coingecko_api_key:
            raise Exception(
                "Unable to retrieve CoinGecko API key from GCP secrets! Please make sure COIN_GECKO is in .env"
            )

        chain_id = self.crocQuery.chain_id
        if not (pool_id or (chain_id and base and quote and pool_idx)):
            raise MissingParameterException(
                "pool_id or a combination of chain_id, base, quote and pool_idx"
            )

        if pool_id:
            pool = self.get_pool_by_id_subgraph_cached(pool_id)
        else:
            pool = Pool(
                chain_id=chain_id,
                quote=quote,
                base=base,
                pool_idx=pool_idx,
                id="",
                timeCreated=0,
            )

        return self.get_complete_pool_stats_by_pool(pool)

    def get_all_pool_stats(self):
        coingecko_api_key = self.get_server_config()["COIN_GECKO"]
        if not coingecko_api_key:
            raise Exception(
                "Unable to retrieve CoinGecko API key from GCP secrets! Please make sure COIN_GECKO is in .env"
            )

        # Get the list of pools, their base and quote token addresses and other cached information
        pools = self.get_pool_list_subgraph()
        token_addr_set = set(
            [pool.base for pool in pools] + [pool.quote for pool in pools]
        )

        # Make a series of requests to coingecko where we get
        # TODO, implement as a secondary query, which will automagically get cached by the CLI according to a caching policy
        self.get_token_metadata(list(token_addr_set))

        # For each pool get the Accumulated PoolStats from GCGO, including TVL data across aggEvents
        results = {}
        for pool in pools:
            # Access similar to how an external API will access this method, for now
            # FIXME: Propagate the rest of the top leve, pool data properly
            results[pool.id] = self.get_complete_pool_stats(pool.id)
        return results
