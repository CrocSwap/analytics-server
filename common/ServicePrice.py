from typing import Optional

from exceptions.ExceptionBase import ExceptionBase

from .DataClasses import TokenInfo
from .ServiceBase import ServiceBase


class ServicePrice(ServiceBase):
    """Service which gets price data from CoinGecko in a FE friendly format. Currently only supports mainnet"""

    def get_price_for_token(
        self, token_address: str, asset_platform=None
    ) -> Optional[TokenInfo]:
        """Get (from coingecko) the metadata for a token by address"""
        network_config = self.get_network_config()
        CG_ENDPOINT = network_config["CG_ENDPOINT"]
        coingecko_api_key = self.get_server_config()["COIN_GECKO"]

        if not token_address:
            raise ValueError("must provide a valid token_address")

        # Currently only supports mainnet, so asset platforms is hardcoded to "ethereum"
        asset_platform = asset_platform or network_config["cg_asset_platform"]
        params = {
            "vs_currencies": "usd",
            "precision": "full",  # Get the full price without rounding
        }
        token_id = token_address.lower()
        # Ox000 is the default address for ethereum that Crocswap uses
        if token_address == "0x0000000000000000000000000000000000000000":
            uri = f"{CG_ENDPOINT}/simple/price"
            # NOTE: this is COIN GECKO ID for eth
            token_id = "ethereum"
            params["ids"] = token_id
        else:
            uri = f"{CG_ENDPOINT}/simple/token_price/{asset_platform}"
            params["contract_addresses"] = token_address

        headers = {"x-cg-pro-api-key": coingecko_api_key, "accept": "application/json"}
        try:
            resp = ServiceBase.request_rate_limited(uri, params=params, headers=headers)
        except Exception:
            raise ExceptionBase("Unable to fetch price information", status_code=500)

        # Ensure the response contains the required data.
        if token_id not in resp:
            raise ExceptionBase(
                f"No price found for token {token_address}", status_code=404
            )

        data = resp[token_id]
        return TokenInfo(usdPrice=data["usd"], usdPriceFormatted=round(data["usd"], 3))
