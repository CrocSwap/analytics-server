import json
import os
import re
from enum import Enum
from typing import List, Optional

from dotenv import load_dotenv

from .utils import load_json, string_to_bool

load_dotenv()


class EntityType(Enum):
    SWAP = "swap"
    LIQCHANGE = "liqchange"
    LIMITORDER = "limitOrder"


class ChangeType(Enum):
    SWAP = "swap"
    MINT = "mint"
    CROSS = "cross"
    BURN = "burn"
    HARVEST = "harvest"
    RECOVER = "recover"


class PositionType(Enum):
    SWAP = "swap"
    KNOCKOUT = "knockout"
    AMBIENT = "ambient"
    CONCENTRATED = "concentrated"


class ContractVersion(Enum):
    V0 = "V0"
    V1 = "V1"


class ServiceConfigLevel(Enum):
    DATA = "data"
    RECORD = "record"


##############################################
# NEW DATA CLASSES BELOW
# TODO: REFACTOR ABOVE DATA CLASSES
#
class TypedConfig(dict):
    TYPING = (
        {}
    )  # Override this in the derived classes to define types for each attribute

    def __init__(self, *args, **kwargs):
        # Initialize the dict with an empty state
        super(TypedConfig, self).__init__()
        self.update(*args, **kwargs)

    def _replace_private_vars(self, value):
        pattern = re.compile(r"{{(.*?)}}")  # The pattern to look for

        def repl(match):
            env_var_name = match.group(1)
            env_var_value = os.getenv(env_var_name)
            print(env_var_name, env_var_value, flush=True)
            if env_var_value is None:
                raise KeyError(f"Private variable {env_var_name} need to be set.")
            return env_var_value

        result = pattern.sub(repl, json.dumps(value))
        return json.loads(result)

    def _enforce_typing(self, key, value):
        if key not in self.TYPING:
            return

        expected_type = self.TYPING.get(key, None)
        base_type = getattr(expected_type, "__origin__", expected_type)

        if expected_type:
            # If type is Enum, check if value is one of the enum values
            if issubclass(base_type, Enum):
                enum_members = [member.value for member in expected_type]
                if value not in enum_members:
                    raise TypeError(
                        f"Expected value to be in {enum_members} for {key}, but got {value}."
                    )
            # else check if value has the type of base_type
            elif not isinstance(value, base_type):
                raise TypeError(
                    f"Expected type {expected_type} for {key}, but got {type(value)}."
                )

    def __setattr__(self, key, value):
        # This is called when an attribute is set, not a dictionary key
        # To set a dictionary key, use __setitem__ instead

        # Replace private values with data from environment variables
        try:
            complete_value = self._replace_private_vars(value)
        except KeyError as e:
            raise e
        except Exception as e:
            print(f"Could not replace the private vars for {key} with {value} because {e}", flush=True)
            complete_value = ""
        #    raise Exception("Could not replace the private vars for {key} with {value}")

        self._enforce_typing(key, complete_value)

        super(TypedConfig, self).__setattr__(key, value)

    def __setitem__(self, key, value):
        # This is called when a dictionary key is set
        # Replace private values with data from environment variables
        try:
            complete_value = self._replace_private_vars(value)
        except KeyError as e:
            raise e
        except Exception as e:
            print(f"Could not replace the private vars for {key} with {value} because {e}", flush=True)
            complete_value = ""
        #    raise Exception("Could not replace the private vars for {key} with {value}")

        self._enforce_typing(key, complete_value)

        super(TypedConfig, self).__setitem__(key, complete_value)

    def update(self, *args, **kwargs):
        # Update each key manually to trigger __setitem__
        # Initialize from another dict or iterable of key-value pairs
        if args:
            if len(args) > 1:
                raise TypeError("expected at most 1 arguments, got %d" % len(args))
            other = dict(args[0])
            for key in other:
                self[key] = other[key]

        # Initialize from keyword arguments
        for key in kwargs:
            self[key] = kwargs[key]


class PoolTx(TypedConfig):
    TYPING = {
        "blockNum": int,
        "txHash": str,
        "txTime": int,
        "user": str,
        "chainId": str,
        "base": str,
        "quote": str,
        "poolIdx": int,
        "baseFlow": int,
        "quoteFlow": int,
        "entityType": EntityType,
        "changeType": ChangeType,
        "positionType": PositionType,
        "bidTick": int,
        "askTick": int,
        "isBuy": bool,
        "inBaseQty": bool,
        "txId": str,
    }

    def __init__(self, **kwargs):
        self["blockNum"] = int(kwargs.get("blockNum"))
        self["txHash"] = kwargs.get("txHash")
        self["txTime"] = int(kwargs.get("txTime"))
        self["user"] = kwargs.get("user")
        self["chainId"] = kwargs.get("chainId")
        self["base"] = kwargs.get("base")
        self["quote"] = kwargs.get("quote")
        self["poolIdx"] = int(kwargs.get("poolIdx"))
        self["baseFlow"] = int(kwargs.get("baseFlow"))
        self["quoteFlow"] = int(kwargs.get("quoteFlow"))
        self["entityType"] = kwargs.get("entityType")
        self["changeType"] = kwargs.get("changeType")
        self["positionType"] = kwargs.get("positionType")
        self["bidTick"] = int(kwargs.get("bidTick"))
        self["askTick"] = int(kwargs.get("askTick"))
        self["isBuy"] = kwargs.get("isBuy")
        self["inBaseQty"] = kwargs.get("inBaseQty")
        self["txId"] = kwargs.get("txId")


class ExtendedPoolStats(TypedConfig):
    TYPING = {
        "txTimeRange": list[Optional[int]],
        "blockNumRange": list[Optional[int]],
        "swapVolume": int,
        "n_txs": int,
        "buy": int,
        "sell": int,
    }


class BasePoolStats(TypedConfig):
    TYPING = {
        "id": str,
        "latestTime": int,
        "baseTvl": int,
        "quoteTvl": int,
        "baseVolume": int,
        "quoteVolume": int,
        "baseFees": float,
        "quoteFees": float,
        "lastPriceSwap": float,
        "lastPriceLiq": float,
        "lastPriceIndic": float,
        "feeRate": float,
    }

    def __init__(self, **kwargs):
        self["id"] = kwargs.get("id", None)
        self["latestTime"] = int(kwargs.get("latestTime"))
        self["baseTvl"] = int(kwargs.get("baseTvl"))
        self["quoteTvl"] = int(kwargs.get("quoteTvl"))
        self["baseVolume"] = int(kwargs.get("baseVolume"))
        self["quoteVolume"] = int(kwargs.get("quoteVolume"))
        self["baseFees"] = float(kwargs.get("baseFees"))
        self["quoteFees"] = float(kwargs.get("quoteFees"))
        self["lastPriceSwap"] = float(kwargs.get("lastPriceSwap"))
        self["lastPriceLiq"] = float(kwargs.get("lastPriceLiq"))
        self["lastPriceIndic"] = float(kwargs.get("lastPriceIndic"))
        self["feeRate"] = float(kwargs.get("feeRate"))


class Pool(TypedConfig):
    TYPING = {
        "id": str,
        "chain_id": str,
        "timeCreated": int,
        "base": str,
        "quote": str,
        "pool_idx": str,
    }

    def __init__(self, **kwargs):
        self["id"] = kwargs.get("id", None)
        self["chain_id"] = kwargs.get("chain_id", None)
        self["timeCreated"] = int(kwargs.get("timeCreated"))
        self["base"] = kwargs.get("base", None)
        self["quote"] = kwargs.get("quote", None)
        self["pool_idx"] = kwargs.get("pool_idx", None)


class GraphMetadataBlock(TypedConfig):
    TYPING = {
        "hash": str,
        "number": int,
        "timestamp": int,
    }


class NativePrice(TypedConfig):
    TYPING = {
        "value": str,
        "decimals": int,
        "name": str,
        "symbol": str,
        "address": str,
    }


class TokenInfo(TypedConfig):
    TYPING = {
        "usdPrice": float,
        "usdPriceFormatted": float,
    }


class CacheConfig(TypedConfig):
    TYPING = {"duration": int, "path": str}


class ServiceFunctionConfig(TypedConfig):
    TYPING = {
        "cache": CacheConfig,
        "module": str,
        "function": str,
        "params": List[str],
        "level": ServiceConfigLevel,
        "endpoint": str,
    }


class ServiceConfig(TypedConfig):
    TYPING = {
        "chain_id": str,
        "supported_chain_ids": List[str],
        "contract_version": str,
        "results": dict[str, ServiceFunctionConfig],
    }


class NetworkConfig(TypedConfig):
    TYPING = {
        "chainId": str,
        "rpcs": dict[str, List[str]],
        "network_id": str,
        "contract_version": ContractVersion,
        "subgraph": str,
        "dex_contract": str,
        "query_contract": str,
        "query_contract_abi": str,
        "poa_middleware": bool,
        "enable_rpc_cache": bool,
        "enable_subgraph_cache": bool,
        "dai": str,
        "usdc": str,
        "account_1": str,
        "account_2": str,
        "nativeEth": str,
        "poolIdx": str,
        "limit_1_pivot_time": str,
        "limit_1_is_bid": str,
        "limit_1_bid_tick": str,
        "limit_1_ask_tick": str,
        "range_1_bid_tick": str,
        "range_1_ask_tick": str,
        "cacheDomain": str,
        "wolsk.eth": str,
        "wbtc": str,
        "miyuki.eth": str,
        "account_12": str,
        "protocol": str,
        "dumpJson": str,
        "CG_ENDPOINT": str,
        "GCGO_POOL_STATS": str,
        "GCGO_POOL_TXS": str,
        "CURRENCY": str,
        "network_id": str,
        "contract_version": str,
        "cg_asset_platform": str,
        # Postman env related keys
        "__id": str,
        "__name": str,
        "___postman_variable_scope": str,
        "___postman_exported_at": str,
        "___postman_exported_using": str,
        "list_of_values": List[str],
    }

    def __init__(self, data):
        super().__init__(data)
        networks_data = load_json(
            ["configs"], f"networks{self['contract_version']}.json"
        )
        network_data = networks_data[self["chainId"]]
        self.update(network_data)

    def export_to_postman_env(self):
        # Initialize an empty Postman environment dictionary
        postman_env = {"values": []}

        # Extract the list of keys that should be in 'values'
        list_of_values = self.get("list_of_values", [])

        # Populate 'values' array and other metadata
        for key, value in self.items():
            if key == "list_of_values":
                continue  # Skip the 'list_of_values' key

            if key.startswith("__"):
                # Add as metadata
                postman_env[key[2:]] = value  # Remove '__' prefix
            elif key in list_of_values:
                # Add to 'values' array
                postman_env["values"].append(
                    {"key": key, "value": value, "enabled": True, "type": "default"}
                )

        # Convert to JSON
        return json.dumps(postman_env, indent=4)


class ServerConfig(TypedConfig):
    TYPING = {
        "COIN_GECKO": str,
        "FLASK_DEBUG": bool,
        "FLASK_SHOW_TRACEBACK": bool,
        "PORT": int,
        "FLASK_THREADED": bool,
        "FLASK_PROECESSES": int,
        "MAX_CPU": int,
        "MIN_RAM": int,
    }

    def __init__(self):
        self["COIN_GECKO"] = os.getenv("COIN_GECKO")
        self["FLASK_DEBUG"] = string_to_bool(os.getenv("FLASK_DEBUG", "False"))
        self["FLASK_SHOW_TRACEBACK"] = string_to_bool(
            os.getenv("FLASK_SHOW_TRACEBACK", "True")
        )
        
        self["FLASK_THREADED"] = string_to_bool(
            os.getenv("FLASK_THREADED", "True")
        )
        self["FLASK_PROECESSES"] = int(
            os.getenv("FLASK_PROECESSES", "80")
        )
        self["PORT"] = int(os.getenv("PORT", 8080))

        self["MAX_CPU"] = int(
            os.getenv("MAX_CPU", "80")
        )    
        self["MIN_RAM"] = int(
            os.getenv("MIN_RAM", "10")
        )
