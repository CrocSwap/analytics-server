import time

from .DataClasses import PoolTx
from .ServiceBase import ServiceBase


class ServicePoolTxs(ServiceBase):
    def get_pool_txs_for_time_period(
        self, chain_id: str, base: str, quote: str, pool_idx: str, n_days: int
    ) -> list[PoolTx]:
        """
        Get the pool transaction history form GCGO over a given number of days (with timeout & rate limit).

        NOTE: we fetch these from GCGO because they are cached there and we can get them faster this way.
        """

        period = n_days * 24 * 60 * 60
        current_time = int(time.time())
        start_time = current_time - period
        all_transactions: list[PoolTx] = []

        while start_time < current_time:
            params = {
                "chainId": chain_id,
                "base": base,
                "quote": quote,
                "poolIdx": pool_idx,
                "n": 200,  # NOTE: max number of transactions we can get at once
                "time": start_time,  # NOTE: start time
                "period": period,  # NOTE: this is the period of time within which we will get transactions
            }
            raw_resp_data = ServiceBase.request_rate_limited(
                self.get_network_config()["GCGO_POOL_TXS"], params
            )
            if raw_resp_data:
                raw_resp_contents = raw_resp_data.get("data", {})
                if raw_resp_contents:
                    for tx_resp_data in raw_resp_contents:
                        all_transactions.append(PoolTx(**tx_resp_data))

            # Update the start time to the next interval
            start_time += period

        return [all_transaction for all_transaction in all_transactions]
