import json
import os

import requests
from web3 import Web3

from common.DataClasses import NetworkConfig


class CrocQueryProxy:
    # Simplifies the process of loading the contract
    # TODO: consider merging all configuration loading logic into a configuration provider, as it is spread between many files.
    def __init__(self, config, network: NetworkConfig):
        versionId = network["contract_version"]
        chainId = network["chainId"]
        rpc_endpoint = network["rpcs"]["infura"][0]
        self.w3 = Web3(Web3.HTTPProvider(rpc_endpoint))

        abi_data = self.load_json_file(f"CrocQuery{versionId}.json")
        abi = abi_data["abi"]
        contract_address = network["query_contract"]
        contract_address = Web3.to_checksum_address(contract_address)
        self.contract = self.w3.eth.contract(address=contract_address, abi=abi)
        self.subgraph_url = network["subgraph"]

        self.config = config
        self.network = network
        self.chain_id = chainId

    def getw3(self):
        return self.w3

    def load_json_file(self, file_name):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        common_dir = os.path.abspath(os.path.join(current_dir, "..", "configs"))
        file_path = os.path.join(common_dir, file_name)
        with open(file_path, "r") as f:
            return json.load(f)

    def query_subgraph(self, query):
        payload = {"query": query}
        response = requests.post(self.subgraph_url, json=payload)
        if response.status_code != 200:
            raise ValueError(
                f"Error: Failed to fetch query from subgraph. Status code: {response.status_code}"
            )
        return json.loads(response.text)
