import importlib
import json
import os
import subprocess
import sys
import uuid

from hexbytes import HexBytes
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from web3 import Web3
from web3.datastructures import AttributeDict

from .ServiceFactory import ServiceFactory


class ExtendedEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, HexBytes):
            return obj.hex()

        if isinstance(obj, AttributeDict):
            return dict(obj)

        return super(ExtendedEncoder, self).default(obj)


class NewmanTest:
    record_schema = {
        "type": "object",
        "properties": {
            "data": {
                "anyOf": [
                    {
                        "type": "array",
                    },
                    {
                        "type": "object",
                    },
                    {
                        "type": "null",
                    },
                ]
            }
        },
        "required": ["data"],
    }

    execution_schema = {
        "type": "object",
        "properties": {
            "item": {
                "type": "object",
                "properties": {
                    "request": {"type": "object"},
                    "id": {"type": "string"},
                    "name": {"type": "string"},
                },
                "required": ["request", "id", "name"],
            },
            "response": {"type": "object"},
        },
        "required": ["item", "response"],
    }

    data_schema = {
        "type": "object",
        "properties": {
            "run": {
                "type": "object",
                "properties": {
                    "executions": {"type": "array"},
                    "stats": {"type": "object"},
                },
                "required": ["executions", "stats"],
            },
            "collection": {"type": "object"},
        },
        "required": ["run", "collection"],
    }

    def __init__(self):
        pass

    def validate_json(self, data, schema):
        try:
            validate(data, schema)
        except ValidationError as e:
            raise Exception(f"Invalid JSON structure: {e},{data}")

    def set_validation_functions(self, functions_dict):
        pass

    def load_data(
        self, collection, chain_id, outputfile, service_network, env_vars=None
    ):
        # TODO - remvoe env_vars as it is unused, and adds complexity, and potential errors.
        # Likely all we need is a n envfile and serviceConfig. If someone wants to configure a new variable they can supply a new env.
        # TODO - Remove:
        env_vars_flags = ""
        if env_vars:
            for key, value in env_vars.items():
                env_vars_flags += f' --env-var "{key}={value}"'

        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        postman_env = service_network.export_to_postman_env()
        env_filepath = "./postman/temp_env.json"
        with open(env_filepath, "w") as f:
            f.write(postman_env)

        # print(__file__)
        # print(parent_dir)
        command = f"newman run {collection} -e {env_filepath} -r json --reporter-json-export={outputfile} {env_vars_flags}"
        # print(command)
        try:
            subprocess.run(command, shell=True, check=True, cwd=parent_dir)
        except Exception as e:
            # Handle the exception if needed
            raise Exception("Failed while trying to load data from Newman") from e
        finally:
            # Clean up temporary files if they exist
            if os.path.exists(env_filepath):
                os.remove(env_filepath)

    def execute_validate(
        self, response_body, endpoint, config_selection, chain_id, level
    ):
        # print("VALIDATING:" + endpoint)
        have_results = False
        # 1 - fail if passed a non dict
        if not (isinstance(response_body, dict)):
            return have_results
        config = ServiceFactory.load_test(config_selection)
        if chain_id:
            config["chain_id"] = chain_id
        network = ServiceFactory.load_network(config, config["chain_id"])
        if not "env_vars" in config or not config["env_vars"]:
            config["env_vars"] = {}

        # 2 - prep validation functions. We may have many functions to apply to this row
        validationResults = []
        for function_key, function_config in config[
            "cross_validation_functions"
        ].items():
            function_config["params"] = ["data", "endpoint"]
            if not "endpoint" in function_config:
                function_config["endpoint"] = function_key

            if (
                function_config["level"] == level
                and function_config["endpoint"] == endpoint
            ):
                if function_config["endpoint"] == endpoint:
                    # TODO: Fix this or remove this endpoint comparison logic
                    # During refactor, this logic ended up checking A=A and not A=B. It may always be true.
                    have_results = True
                    try:
                        res = ServiceFactory.invoke_function(
                            kwargs={
                                "data": response_body,
                                "endpoint": endpoint,
                            },
                            function_config=function_config,
                            service_config=config,
                            service_network=network,
                        )
                    except:
                        import traceback as tb

                        res = {"valid": False, "error": tb.format_exc()}
                    validationResults.append(res)
        response_body["__validationResult"] = validationResults

        # 3 - explore the results, and treat False as a primary result, True as secondary, and None as an absence of all results
        response_body["__valid"] = None
        for validationResult in response_body["__validationResult"]:
            result = validationResult["valid"]
            if (
                response_body["__valid"] == None
            ):  # store any non None result if we have one. True values are ideal.
                response_body["__valid"] = result
            elif (
                response_body["__valid"] != None and result == False
            ):  # If we see any False, it is a fail. Lock this value in
                response_body["__valid"] = result
            else:
                pass
        return have_results

    def process_endpoint_result(self, execution, config_selection, chain_id, endpoints):
        self.validate_json(execution, self.execution_schema)

        # TODO. Good place for a data type
        request_name = execution["item"]["name"]
        request_data = execution["item"]["request"]
        response_data = execution["response"]
        post_args = request_data.get("body", {}).get("raw", "")
        status_code = response_data["code"]
        response_time = response_data.get("responseTime", 0)

        try:
            endpoint = request_data["url"]["path"][1]
        except:
            endpoint = request_data["url"]["path"][0]
        if endpoints and type(endpoints) == list:
            if endpoint not in endpoints:
                return None
        try:
            response_body = json.loads(bytes(response_data["stream"]["data"]).decode())
        except json.JSONDecodeError:
            response_body = bytes(response_data["stream"]["data"]).decode()

        protocol = request_data["url"].get("protocol", "http")
        host = ".".join(request_data["url"]["host"])
        path = "/".join(request_data["url"]["path"])
        query = "&".join(
            [f"{q['key']}={q['value']}" for q in request_data["url"]["query"]]
        )
        url = f"{protocol}://{host}/{path}?{query}"

        placeholders = {
            var["key"]: var["value"] for var in request_data["url"]["variable"]
        }
        final_url = url.format(**placeholders)

        # ,response_body,endpoint,config_selection,env_selection

        # Do all validation work
        include_the_results = False
        if isinstance(response_body, dict) and "data" in response_body:
            include_the_results = (
                self.execute_validate(
                    response_body, endpoint, config_selection, chain_id, "data"
                )
                or include_the_results
            )
            if type(response_body["data"]) == list:
                for record in response_body["data"]:
                    include_the_results = (
                        self.execute_validate(
                            record, endpoint, config_selection, chain_id, "record"
                        )
                        or include_the_results
                    )

        if include_the_results == False:
            return None
        return {
            "id": execution["item"]["id"],
            "name": execution["item"]["name"],
            "url": url,
            "final_url": final_url,
            "time": response_time,
            "responseCode": {"code": status_code, "name": response_data["status"]},
            "tests": {"Status code is 200": status_code == 200},
            "responseBody": response_body,
            "postArgs": post_args,
        }

    def parse_newman_output(self, config_selection, chain_id, endpoints=None):
        # Load the newman output file

        config = ServiceFactory.load_test(config_selection)
        if not "env_vars" in config or not config["env_vars"]:
            config["env_vars"] = {}

        data = ServiceFactory.load_json_bypath(config["outpath"])
        self.validate_json(data, self.data_schema)
        results = []

        # Iterate through each execution in the newman data
        for execution in data["run"]["executions"]:
            result = self.process_endpoint_result(
                execution, config_selection, chain_id, endpoints
            )
            if result:
                results.append(result)

        collection_id = data["collection"].get("_", {}).get("postman_id", "N/A")
        collection_name = data["collection"].get("item", [{}])[0].get("name", "N/A")

        postman_like_output = {
            "id": collection_id,
            "name": collection_name,
            "timestamp": data["run"].get("timestamp", "N/A"),
            "collection_id": collection_id,
            "folder_id": 0,
            "totalPass": data["run"]["stats"]["assertions"]["total"]
            - data["run"]["stats"]["assertions"]["failed"],
            "totalFail": data["run"]["stats"]["assertions"]["failed"],
            "results": results,
        }
        try:
            ServiceFactory.save_json_bypath(
                config["resultspath"], postman_like_output, cls=ExtendedEncoder
            )
        except Exception as e:
            print("JSON ERROR")
            import traceback as tb
