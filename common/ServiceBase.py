import hashlib
import json
import subprocess

import requests
from exceptions.UnsupportedChainIdException import UnsupportedChainIdException

from .CrocQueryProxy import CrocQueryProxy as Query

# Unfortunately, these tools are not compatible with Jupyter yet
# from typing import Any, Literal, Optional, Tuple

"""
Services: Can be analytics data, or a service oriented endpoint

The base class sets up constants for all services. Includes:
- Bound Smart Contracts
- Subgraph Configurations and Constants
- Infura Keys
- Special Paths
- and more

(if you have an object that all Analytics need to access, it should be loaded in here)
"""


class ServiceBase:
    instances = None
    do_create = False

    def __init__(
        self, queryProxy: Query, config: dict, network: dict, server_config: dict
    ):
        # Check if chain_id is supported by service
        selected_chain_id = network["chainId"]
        supported_chain_ids = config.get("supported_chain_ids", [])
        if selected_chain_id not in supported_chain_ids:
            raise UnsupportedChainIdException(selected_chain_id, supported_chain_ids)

        self.crocQuery = queryProxy
        self.w3 = self.crocQuery.getw3()
        self.service_config = config
        self.service_network = network
        self.server_config = server_config

    """
     shallow copy of the service config
    """

    def get_service_config(self):
        return self.service_config.copy()

    """
     shallow copy of the server config
    """

    def get_server_config(self):
        return self.server_config.copy()

    """
     shallow copy of the network config
    """

    def get_network_config(self):
        return self.service_network.copy()

    """
    take the args, and generate a unique hash string
    """

    @staticmethod
    def hash_args(args: dict):
        # return ServiceFactory.hash_args(args)
        json_args = json.dumps(args, sort_keys=True)
        hasher = hashlib.sha256()
        hasher.update(json_args.encode("utf-8"))
        return hasher.hexdigest()

    @staticmethod
    def request_rate_limited(
        uri: str,
        params: dict = None,
        headers: dict = None,
        max_retries=5,
        retry_delay=1,
    ) -> dict:
        """Make a GET request which handles failures and rate limits retries.

        TODO: extend to handle all req types.

        args:
            max_retries: how many attempts to make before raising Exception
            retry_delay (seconds): how long to wait between reties (exp base)
        """
        for attempt in range(max_retries):
            try:
                response = requests.get(uri, params=params, headers=headers)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.HTTPError as http_err:
                # Handle HTTP errors (e.g., 429 - Too Many Requests)
                if response.status_code == 429 and attempt < max_retries - 1:
                    print(f"Rate limited. Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Increase the retry delay exponentially
                else:
                    raise Exception(f"HTTP error: {http_err}")
            except requests.exceptions.RequestException as req_err:
                # Handle other request-related errors
                raise Exception(f"Request error: {req_err}")
        raise Exception("Request error")

    @staticmethod
    def get_secret(secret_id: str, version: str = "latest") -> str:
        """Secrets accessor for GCP"""
        try:
            # Run the gcloud command to get the secret
            command = [
                "gcloud",
                "secrets",
                "versions",
                "access",
                version,
                "--secret",
                secret_id,
                "--format=json",
            ]
            result = subprocess.run(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )

            if result.returncode == 0:
                # Parse the output JSON to get the secret data
                secret_data = json.loads(result.stdout)
                return secret_data["payload"]["data"]
            else:
                print(f"Error retrieving secret. Error message: {result.stderr}")
                return None

        except Exception as e:
            print(f"Error: {e}")
            return None
