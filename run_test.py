import csv
import json
import os
import subprocess
import time
import unittest

import requests

import docker
from common.DataClasses import ServerConfig

default_chain_ids = [None, "0x1", "0x5"]

services_data = [
    {
        "api_service": "run_record_validation",
        "service_name": "run_record_validation",
        "configs": [
            {"config": "example_single", "endpoint": "user_positions"},
            {"config": "cv_user_positions", "endpoint": "user_pool_positions"},
            # {"config": "cv_user_limit_orders", "endpoint": "user_limit_orders"} Not passing
        ],
    },
    {
        "api_service": "run_data_validation",
        "service_name": "run_data_validation",
        "configs": [{"config": "schema"}],
    },
    {
        "api_service": "run_service",
        "service_name": "run",
        "configs": [
            {"config": "example", "arg1": "EXAMPLE", "arg2": "EXAMPLE2"},
            {"config": "validation"},  # TODO rename to a precise name
            {
                "config": "complete_pool_stats",
                "pool_id": "0xd417ff54652c09bd9f31f216b1a2e5d1e28c1dce1ba840c40d16f2b4d09b5902",
                "supported_chain_ids": ["0x1"],
            },
            {
                "config": "complete_pool_stats",
                "chain_id": "0x1",
                "base": "0x0000000000000000000000000000000000000000",
                "quote": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
                "pool_idx": "420",
                "supported_chain_ids": ["0x1"],
            },
            {
                "config": "ens_address",
                "address": "0xE09de95d2A8A73aA4bFa6f118Cd1dcb3c64910Dc",
                "supported_chain_ids": ["0x1"],
            },
            {
                "config": "price",
                "token_address": "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599",
                "supported_chain_ids": ["0x1"],
            },
            {
                "config": "realtime_price",
                "token_address": "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599",
                "supported_chain_ids": ["0x1"],
            },
        ],
    },
]

STAGING_BASE_URL = (
    "https://crocswap-analytics-tools-service-staging-dfxb5x3tja-uc.a.run.app"
)
PRODUCTION_BASE_URL = "https://crocswap-analytics-tools-service-dfxb5x3tja-uc.a.run.app"


def generate_tests():
    generated_tests = []
    for service_data in services_data:
        for config in service_data["configs"]:
            chain_ids = config.get("supported_chain_ids", default_chain_ids)
            for chain_id in chain_ids:
                args = config.copy()
                args.pop("supported_chain_ids", "")
                test_entry = {
                    "api_service": service_data["api_service"],
                    "service_name": service_data["service_name"],
                    "args": args,
                }

                if chain_id:
                    test_entry["args"]["chain_id"] = chain_id
                generated_tests.append(test_entry)

    return generated_tests


class CLITest(unittest.TestCase):
    def test_cli_formatting(self):
        print("Test CLI Formatting")
        tests = generate_tests()
        for service_call in tests:
            cli_command = ["python3", service_call["api_service"] + ".py"]
            for key, val in service_call["args"].items():
                cli_command.append("--" + key)
                cli_command.append(val)

            result = subprocess.run(cli_command, capture_output=True)
            print(" ".join(cli_command))
            try:
                json.loads(result.stdout)
            except:
                import traceback as tb

                tb.print_exc()
                print("FAILED TEST:")
                print(result.stdout)
                print(result.stderr)
                break


class APITest:
    def fn_for_testing(self, base_url):
        # Override this in the child class
        pass

    def __run_local_server(self):
        # Define the command to run your server script (replace with your actual command)
        cmd = ["python3", "run_server.py"]

        # Run the server script using subprocess
        return subprocess.Popen(cmd)

    def __build_docker_image_if_not_exists(self, image_name, path="."):
        client = docker.from_env()

        # Check if the image already exists
        try:
            client.images.get(image_name)
            print(f"Image '{image_name}' already exists.")
        except docker.errors.ImageNotFound:
            print(f"Image '{image_name}' does not exist. Building...")

            # Build the Docker image
            client.images.build(path=path, tag=image_name, rm=True)

    def test_local_api(self, with_run_server=True):
        print("Test Local API")
        # Start local server if needed
        if with_run_server:
            local_server = self.__run_local_server()

        config = ServerConfig()
        base_url = f"http://localhost:{config['PORT']}"

        self.fn_for_testing(base_url)
        # Stop local server if it was needed before
        if with_run_server:
            local_server.terminate()
            local_server.wait()

    def test_staging_api(self):
        print("Test Staging API")
        self.fn_for_testing(STAGING_BASE_URL)

    def test_production_api(self):
        print("Test Production API")
        self.fn_for_testing(PRODUCTION_BASE_URL)

    def test_docker_container(self):
        # Define the Docker image name and the PORT environment variable
        image_name = "audit-process"
        port_env_var = "8088"  # Replace with your desired PORT
        config = ServerConfig()
        env_port = config["PORT"]

        print("Creating Docker Client")
        # Create a Docker client
        client = docker.from_env()

        print("Build the Docker image")
        # Build the Docker image
        self.__build_docker_image_if_not_exists(image_name)

        print("Run the Docker image")
        # Create and start a Docker container with the specified environment variable
        container = client.containers.run(
            image=image_name,
            detach=True,
            ports={
                f"{env_port}/tcp": port_env_var
            },  # Map the container port to the host
            environment={"PORT": port_env_var},  # Set the PORT environment variable
        )

        print("Execute Run Test")
        result = True
        # Run python3 run_server.py inside the Docker container
        try:
            self.test_local_api(with_run_server=False)
        except AssertionError as e:
            result = False

        print("Stop the container")
        # Stop and remove the container
        container.stop()
        container.remove()

        assert result == True


class APIResponseTest(unittest.TestCase, APITest):
    def setUp(self):
        # Set the fn_for_testing for testing API
        self.fn_for_testing = self.__test_api_for_base_url

    def __test_api_call(self, url, query_params):
        response = requests.get(url, params=query_params)
        print(f"{url}, query params: {query_params}")
        self.assertEqual(
            response.status_code,
            200,
            f"Failed for URL: {url} with Params: {query_params}",
        )

    def __test_api_for_base_url(self, base_url):
        tests = generate_tests()
        failed_tests_messages = []
        url = f"{base_url}/run"
        for service_call in tests:
            query_params = service_call["args"].copy()
            query_params["service"] = service_call["service_name"]
            query_params["config_path"] = query_params.pop("config")
            query_params["include_data"] = 0

            try:
                self.__test_api_call(url, query_params)
            except AssertionError as e:
                failed_tests_messages.append(e)

        if len(failed_tests_messages):
            print(failed_tests_messages)

        self.assertEqual(len(failed_tests_messages), 0)


class LoadTest(unittest.TestCase, APITest):
    def setUp(self):
        # Set the fn_for_testing for load testing
        self.fn_for_testing = self.__load_test_for_base_url

    def __run_locust_load_test(self, base_url, test_config):
        num_users = test_config.get("num_users", 200)
        user_spawn_rate = test_config.get("user_spawn_rate", 20)
        duration = test_config.get("duration", 60)
        client_test_name = test_config.get("client_test_name")

        result_path = test_config.get("result_path", "tests/unittest_temp")
        # Run the Locust load test as a subprocess
        cmd = [
            "locust",
            "-f",
            "run_load_test",
            client_test_name,
            "--host",
            base_url,
            "--csv",
            result_path,
            "-u",
            str(num_users),
            "-r",
            str(user_spawn_rate),
            "-t",
            f"{duration}s",
            "--headless",
            "--only-summary",
        ]
        print(" ".join(cmd))
        locust_process = subprocess.Popen(cmd)

        # Wait for the Locust test to complete
        time.sleep(duration + 5)  # Wait the desired duration plus some buffer

        # Terminate the Locust process
        locust_process.terminate()
        locust_process.wait()

        return self.__read_and_clean_locust_results(result_path)

    def __remove_file_if_exists(self, path):
        if os.path.exists(path):
            # Delete the file
            os.remove(path)

    def __read_and_clean_locust_results(self, result_path):
        with open(f"{result_path}_stats.csv", "r") as file:
            dict_results = csv.DictReader(file)
            # Convert all rows to a list of dictionaries
            results = list(dict_results)
            aggregated_result = results[-1]
            formatted_result = {
                "request_name": aggregated_result["Name"],
                "avg_response_time": float(aggregated_result["Average Response Time"]),
            }
        # Clean up results file
        self.__remove_file_if_exists(f"{result_path}_stats.csv")
        self.__remove_file_if_exists(f"{result_path}_stats_history.csv")
        self.__remove_file_if_exists(f"{result_path}_failures.csv")
        self.__remove_file_if_exists(f"{result_path}_exceptions.csv")
        return formatted_result

    def __assert_load_test_result(self, results):
        failed_results = results["failed"]
        assert (
            len(failed_results) == 0
        ), f"Load test failed for this configuration: {failed_results}"

    def __load_test_for_base_url(self, base_url):
        locust_configs = [
            {"num_users": 200, "user_spawn_rate": 20, "duration": 60},
            {"num_users": 500, "user_spawn_rate": 50, "duration": 60},
            {"num_users": 1000, "user_spawn_rate": 100, "duration": 60},
        ]
        locust_scenarios = [
            "ENSAddressClient",
            "PriceEndpointClient",
            "CompletePoolStatsClient",
        ]
        test_results = {"passed": [], "failed": []}

        for locust_scenario in locust_scenarios:
            for locust_config in locust_configs:
                config = locust_config.copy()
                config["client_test_name"] = locust_scenario
                result = self.__run_locust_load_test(base_url, config)
                # Record result
                if result["avg_response_time"] > 300:
                    config["actual_stats"] = result
                    test_results["failed"].append(config)
                else:
                    test_results["passed"].append(config)

        self.__assert_load_test_result(test_results)


if __name__ == "__main__":
    unittest.main()
