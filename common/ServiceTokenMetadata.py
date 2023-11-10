import os
import pickle
from datetime import date
from typing import Any, Optional, Tuple

from .ServiceBase import ServiceBase


class ServiceTokenMetadata(ServiceBase):
    def get_token_metadata(
        self, token_addresses: set[str]
    ) -> Tuple[dict[str, Any], list[str]]:
        """Get CoinGecko metadata for all of the tokens in a set of addresses.

        This includes stuff like marketcap, it's a lot of data.

        returns the complete metadata and any addresses for which we could not fetch the metadata (5 retries default).
        """
        failed_addresses: list[str] = []
        token_metadata: dict[str, Any] = {}

        for addr in token_addresses:
            try:
                token_metadata[addr] = self.get_token_metadata_by_address(addr)
                # print(f"...retrieved token metadata for token: {addr}")
            except Exception as err:
                print(f"could not fetch metadata from coingecko for addr {addr}: {err}")
                failed_addresses.append(addr)

        return token_metadata, failed_addresses

    def get_token_metadata_by_address(self, token_address: str) -> dict[str, Any]:
        """Get (from coingecko) the metadata for a token by address.

        NOTE: assumes we are working with ethereum addresses & tokens
        """
        cg_endpoint = self.get_network_config()["CG_ENDPOINT"]
        asset_platform = "ethereum"
        if (
            token_address == "0x0000000000000000000000000000000000000000"
        ):  # NOTE: this is native eth token.
            uri = f"{cg_endpoint}/coins/{asset_platform}"
        else:
            uri = f"{cg_endpoint}/coins/{asset_platform}/contract/{token_address}"

        server_config = self.get_server_config()
        headers = {
            "x-cg-pro-api-key": server_config["COIN_GECKO"],
            "accept": "application/json",
        }
        return ServiceBase.request_rate_limited(uri, headers=headers)
