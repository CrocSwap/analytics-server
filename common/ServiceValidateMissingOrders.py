from datetime import datetime, timedelta

from web3 import Web3

from .ServiceBase import ServiceBase

GCGO_POOL_LIMIT_ORDERS = "https://ambindexer.net/gcgo/pool_limit_orders"
GCGO_POOL_POSITION_ORDERS = "https://ambindexer.net/gcgo/pool_positions"


class ServiceValidateMissingOrders(ServiceBase):
    def grouped_liq_changes_by_key(self, liq_changes, key, with_hash):
        grouped_results = {}

        # Loop through each record in the results
        for record in liq_changes:
            record_key = record[key]
            if with_hash:
                record_key = self.hash_args(record_key)

            # Add the record to the appropriate group in the dictionary
            if record_key not in grouped_results:
                grouped_results[record_key] = []
            grouped_results[record_key].append(record)

        return grouped_results

    def query_last_24h_liq_changes(self):
        timestamp_24h_ago = int(
            (datetime.utcnow() - timedelta(hours=24)).timestamp()
        )  # 1694468659
        query = f"""
            {{
                liquidityChanges(
                    where: {{changeType_not: "cross", time_gte: {timestamp_24h_ago}}}
                    orderBy: "time"
                    orderDirection: "desc"
                ) {{
                    user
                    bidTick
                    askTick
                    isBid
                    pivotTime
                    positionType
                    changeType
                    time
                    pool {{
                        base
                        quote
                        poolIdx
                    }}
                }}
            }}
        """
        retVal = self.crocQuery.query_subgraph(query)
        liq_changes = retVal["data"]["liquidityChanges"]

        return liq_changes

    def is_liq_changes_knocked_out(self, liq_changes):
        base = Web3.to_checksum_address(liq_changes["pool"]["base"])
        quote = Web3.to_checksum_address(liq_changes["pool"]["quote"])
        poolIdx = int(liq_changes["pool"]["poolIdx"])
        params = {
            "owner": Web3.to_checksum_address(liq_changes["user"]),
            "base": base,
            "quote": quote,
            "pivot": liq_changes["pivotTime"],
            "isBid": liq_changes["isBid"],
            "poolIdx": poolIdx,
            "lowerTick": liq_changes["bidTick"],
            "upperTick": liq_changes["askTick"],
        }

        if not params["pivot"] == 0:
            bidTick = (
                liq_changes["bidTick"]
                if liq_changes["isBid"]
                else liq_changes["askTick"]
            )
            knockout_pivot = self.crocQuery.contract.functions.queryKnockoutPivot(
                base,
                quote,
                poolIdx,
                liq_changes["isBid"],
                bidTick,
            ).call()
            # Extract the second element from the returned tuple
            params["pivot"] = knockout_pivot[1]

        retVal = self.crocQuery.contract.functions.queryKnockoutTokens(**params).call()

        return retVal

    def is_position_liq_changes_knocked_out(self, liq_changes):
        base = Web3.to_checksum_address(liq_changes["pool"]["base"])
        quote = Web3.to_checksum_address(liq_changes["pool"]["quote"])
        poolIdx = int(liq_changes["pool"]["poolIdx"])
        params = {
            "owner": Web3.to_checksum_address(liq_changes["user"]),
            "base": base,
            "quote": quote,
            "poolIdx": poolIdx,
            "lowerTick": liq_changes["bidTick"],
            "upperTick": liq_changes["askTick"],
        }

        retVal = self.crocQuery.contract.functions.queryRangePosition(**params).call()

        return retVal

    def is_ambient_liq_changes_knocked_out(self, liq_changes):
        base = Web3.to_checksum_address(liq_changes["pool"]["base"])
        quote = Web3.to_checksum_address(liq_changes["pool"]["quote"])
        poolIdx = int(liq_changes["pool"]["poolIdx"])
        params = {
            "owner": Web3.to_checksum_address(liq_changes["user"]),
            "base": base,
            "quote": quote,
            "poolIdx": poolIdx,
        }

        retVal = self.crocQuery.contract.functions.queryAmbientTokens(**params).call()

        return retVal

    def get_limit_orders_for_pool(self, pool, n):
        base = pool["base"]
        quote = pool["quote"]
        pool_idx = pool["poolIdx"]

        params = {
            "chainId": self.crocQuery.chain_id,
            "base": base,
            "quote": quote,
            "poolIdx": pool_idx,
            "n": n,
        }
        raw_resp_data = ServiceBase.request_rate_limited(GCGO_POOL_LIMIT_ORDERS, params)
        if raw_resp_data:
            raw_resp_contents = raw_resp_data.get("data", [])
            return raw_resp_contents
        return []

    def get_position_orders_for_pool(self, pool, n):
        base = pool["base"]
        quote = pool["quote"]
        pool_idx = pool["poolIdx"]

        params = {
            "chainId": self.crocQuery.chain_id,
            "base": base,
            "quote": quote,
            "poolIdx": pool_idx,
            "n": n,
        }
        raw_resp_data = ServiceBase.request_rate_limited(
            GCGO_POOL_POSITION_ORDERS, params
        )
        if raw_resp_data:
            raw_resp_contents = raw_resp_data.get("data", [])
            return raw_resp_contents
        return []

    def get_missing_liq_changes_from_limit_orders(self, liq_changes, limit_orders):
        # Convert each list to a set of tuples
        graphSet = {
            (
                x["user"],
                x.get("pivotTime") or 0,
                x["pool"]["base"],
                x["pool"]["quote"],
                int(x["pool"]["poolIdx"]),
                x["bidTick"],
                x["askTick"],
                x["isBid"],
                x["positionType"],
            )
            for x in liq_changes
        }

        # Create a set for apiResults
        api_set = {
            (
                x["user"],
                x.get("pivotTime") or 0,
                x["base"],
                x["quote"],
                x["poolIdx"],
                x["bidTick"],
                x["askTick"],
                x["isBid"],
                x.get("positionType") or "knockout",
            )
            for x in limit_orders
        }

        # Find entries that are in graph_dict but not in api_set)
        missing_in_api = set(graphSet) - set(api_set)

        return list(missing_in_api)

    def get_missing_knockout_liq_changes(self, liq_changes):
        active_orders = []
        missing_orders = []
        for liq in liq_changes:
            [contractLiq, _, _, _] = self.is_liq_changes_knocked_out(liq)
            if contractLiq != 0:
                active_orders.append(liq)

        grouped_by_pool = self.grouped_liq_changes_by_key(active_orders, "pool", True)
        for pool_liq_changes in grouped_by_pool.values():
            gcgo_limit_orders = self.get_limit_orders_for_pool(
                pool_liq_changes[0]["pool"], 200
            )
            missing_order = self.get_missing_liq_changes_from_limit_orders(
                pool_liq_changes, gcgo_limit_orders
            )
            missing_orders += missing_order
        return missing_orders

    def get_missing_position_liq_changes(self, liq_changes):
        active_orders = []
        missing_orders = []
        for liq in liq_changes:
            if liq["positionType"] == "concentrated":
                [contractLiq, _, _, _] = self.is_position_liq_changes_knocked_out(liq)
            elif liq["positionType"] == "ambient":
                [contractLiq, _, _] = self.is_ambient_liq_changes_knocked_out(liq)

            if contractLiq != 0:
                active_orders.append(liq)

        grouped_by_pool = self.grouped_liq_changes_by_key(active_orders, "pool", True)

        for pool_liq_changes in grouped_by_pool.values():
            gcgo_limit_orders = self.get_position_orders_for_pool(
                pool_liq_changes[0]["pool"], 200
            )
            missing_order = self.get_missing_liq_changes_from_limit_orders(
                pool_liq_changes, gcgo_limit_orders
            )

            missing_orders += missing_order
        return missing_orders

    def validate_missing_orders(self):
        liq_changes = self.query_last_24h_liq_changes()
        gropued_liq_changes = self.grouped_liq_changes_by_key(
            liq_changes, "positionType", False
        )

        missing_orders = []
        missing_orders += self.get_missing_knockout_liq_changes(
            gropued_liq_changes.get("knockout", [])
        )
        concentrated_ambient_orders = gropued_liq_changes.get(
            "concentrated", []
        ) + gropued_liq_changes.get("ambient", [])
        missing_orders += self.get_missing_position_liq_changes(
            concentrated_ambient_orders
        )

        return missing_orders
