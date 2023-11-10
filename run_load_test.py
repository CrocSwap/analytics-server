import argparse
import random
import time

from locust import HttpUser, User, between, events, task

from common.DataClasses import ServerConfig
from run_service import run


class HttpLoadTest(HttpUser):
    abstract = (
        True  # Mark this User class as abstract so its not selectable from the UI
    )
    wait_time = between(1, 2)

    def __init__(self, *args, **kwargs):
        # Define the default host URL
        config = ServerConfig()
        default_host = (
            f"http://localhost:{config['PORT']}"  # Replace with your default host URL
        )
        self.host = self.host or default_host
        super().__init__(*args, **kwargs)

    # This function is used to test the service function
    def run_service_test(self, service_test_case):
        env_name = "0x1"
        include_data = "0"

        start_time = time.time()  # Start timing

        try:
            service_name = service_test_case["name"]
            run(env_name, service_name, include_data, service_test_case["params"])
            total_time = int(
                (time.time() - start_time) * 1000
            )  # Calculate response time in milliseconds
            events.request.fire(
                request_type="GET",
                name=f"Run service: {service_name}",
                response_time=total_time,
                response_length=0,
            )
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="GET",
                name=f"Run service {service_name}",
                response_time=total_time,
                exception=e,
                response_length=0,
            )

    # This function is used to test the API that calls the service
    def run_api_test(self, service_test_case):
        query_params = service_test_case["params"].copy()
        query_params["service"] = "run"
        query_params["config_path"] = service_test_case["name"]
        query_params["include_data"] = 0

        url = f"{self.host}/run"
        self.client.get(url, params=query_params, name=service_test_case["name"])


class ENSAddressClient(HttpLoadTest):
    @task
    def test_ens_address(self):
        ens_address = [
            "0xe09de95d2a8a73aa4bfa6f118cd1dcb3c64910dc",
            "0x262b58f94055B13f986722498597a43CA9f3BA6D",
            "0x11a85a45114BeEc4bce7CE742Bfa4E52f93d85D6",
            "0x2996A88B92f59468Ae0b3dE343B83e08Ffe9F754",
            "0xfAAe0B09e9A80d142A11cd846CD9329F2E96f55F",
            "0x78A2dE0E55d5898C4eeB6AEfA437299f378Ac185",
            "0xe9804B35116847552282C51762834cFc11935b8B",
            "0x2996A88B92f59468Ae0b3dE343B83e08Ffe9F754",
            "0xD94F51053b9817bc2de4DBbaC647D9a784C24406",
            "0x72CF63232D3b55e4Cd7B209067679b8f90d6B0EA",
            "0x96759a5C3dd3BcD978891bC908197f5887265Da7",
        ]
        service_test = {
            "name": "ens_address",
            "params": {"address": random.choice(ens_address)},
        }
        self.run_api_test(service_test)


class PriceEndpointClient(HttpLoadTest):
    @task
    def test_price_endpoint(self):
        address = [
            "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",  # USDC
            "0xdAC17F958D2ee523a2206206994597C13D831ec7",  # USDT
            "0xB8c77482e45F1F44dE1745F52C74426C631bDD52",  # BNB
            "0x7D1AfA7B718fb893dB30A3aBc0Cfc608AaCfeBB0",  # MATIC
            "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599",  # WBTC
            "0x514910771AF9Ca656af840dff83E8264EcF986CA",  # LINK
            "0x6B175474E89094C44Da98b954EedeAC495271d0F",  # DAI
        ]
        service_test = {
            "name": "price",
            "params": {"token_address": random.choice(address)},
        }
        self.run_api_test(service_test)


class CompletePoolStatsClient(HttpLoadTest):
    @task
    def test_complete_pool_stats(self):
        pool_ids = [
            "0x02413926f87427de1790f178f5a59ad63096045810116e18b451f26440c15e56",
            "0x098c5f5cb2458908768ba9220868aef167717ef0f251f1228c5c5769029a1a93",
            "0x0b4412ca23e70bbac6b4d2fd8f67483d87d99410fe3d3d695ce60166fe1d03b8",
            "0x0e166d562f65d19e9b4724081d6b249bac26c0657819466e03dafda89550bd54",
            "0x1bc9351f349e34a26f0ee9bf82238456e562950530299af7c533d62e28c0e017",
            "0x228b2f710d819ce46bc85c2a604d3cc89ebd50c3b87e9199a3d40265cb2390d2",
        ]

        service_test = {
            "name": "complete_pool_stats",
            "params": {"pool_id": random.choice(pool_ids)},
        }

        self.run_api_test(service_test)


class ExampleClient(HttpLoadTest):
    @task
    def test_example(self):
        service_test = {
            "name": "example",
            "params": {"arg1": "name", "arg2": "world"},
        }
        self.run_api_test(service_test)
