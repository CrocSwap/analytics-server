import importlib
import json
import os,threading
from datetime import datetime, timedelta

from common.DataClasses import NetworkConfig, ServerConfig, ServiceConfig

from .CrocQueryProxy import CrocQueryProxy
from .ServiceBase import ServiceBase
from .utils import load_json

"""
    CacheDatabase
    This will be the Abstract base class for all CacheDatabases
    (Could also use an Interface. The deciding factor between Interface and Abstract class will likely be 
    the amount of code in common between all children of CacheDatabase.)
"""
# Global dictionary to keep track of locks for different function calls
function_locks = {}

class CacheDatabase:
    # TODO: Choose between AbstractClass and Interface, as requirements become clear
    pass


"""
    SimpleFileCache
    Just getting set up for Dependency Injection. SimpleFileCache is passed into the ServiceFactory to enable function caching.
"""


class SimpleFileCache(CacheDatabase):
    """
    load any existing cached result. Throws errors.
    Returns a tuple of (is from cached, result).
    The first element indicates whether the result is from cached file or not
    The second element indicates the result from cached file
    """

    @classmethod
    def load(cls, args, kwargs, cache_config):
        cache_duration = cache_config.get("duration", 0)
        if cache_duration == 0:
            return (False, None)

        timestamp = datetime.now()
        arghash = ServiceFactory.hash_args([args, kwargs, cache_config])

        resultspath = cache_config.get("path")
        assert resultspath
        resultspath_cached = (
            f"{os.path.splitext(os.path.basename(resultspath))[0]}_{arghash}"
        )

        # Check if cached results should be used
        if cache_duration and cache_duration > 0:
            parent_dir = os.path.dirname(resultspath)

            # Quick Purge Loop: Deletes cache files older than the cache window
            # lets make sure we do not fill the whole harddrive up
            for filename in os.listdir(parent_dir):
                if filename.startswith(resultspath_cached):
                    try:
                        timestamp_str = filename.rsplit(".", 1)[0].rsplit("_", 1)[-1]
                        cached_time = datetime.strptime(timestamp_str, "%Y%m%d%H%M%S")
                        if timestamp - cached_time > timedelta(seconds=cache_duration):
                            os.remove(os.path.join(parent_dir, filename))
                    except ValueError:
                        # Skip if filename does not contain timestamp
                        continue

            # Cache Loop
            for filename in os.listdir(parent_dir):
                if filename.startswith(resultspath_cached):
                    try:
                        # Strip extension before attempting conversion
                        timestamp_str = filename.rsplit(".", 1)[0].rsplit("_", 1)[-1]
                        cached_time = datetime.strptime(timestamp_str, "%Y%m%d%H%M%S")
                        if timestamp - cached_time <= timedelta(seconds=cache_duration):
                            # print(f"Loading results from cache: {filename}")
                            with open(
                                os.path.join(os.path.dirname(resultspath), filename),
                                "r",
                            ) as f:
                                resp = json.load(f)
                                return (True, resp)
                    except ValueError:
                        # Skip if filename does not contain timestamp
                        continue
        return (False, None)

    """
        Cache a result
    """
    @classmethod
    def save(cls, args, kwargs, cache_config, resp):
        cache_duration = cache_config.get("duration", 0)
        if cache_duration == 0:
            return None

        timestamp = datetime.now()
        resultspath = cache_config.get("path")
        arghash = ServiceFactory.hash_args([args, kwargs, cache_config])
        assert resultspath
        resultspath_cached = f"{resultspath.rsplit('.', 1)[0]}_{arghash}_{timestamp.strftime('%Y%m%d%H%M%S')}.json"
        with open(resultspath, "w") as f:
            json.dump(resp, f, indent=4)

        if cache_duration > 0:
            with open(resultspath_cached, "w") as f:
                json.dump(resp, f, indent=4)

    @classmethod
    def search_files(cls, args, kwargs, cache_config):
        # TODO - just changed a lot of code, so this search_files should take over the  if filename.startswith(os.path.basename(resultspath.rsplit('.', 1)[0])):
        # Just pausing in this iteration to get everything else running.
        pass

class SimpleMemoryCache(CacheDatabase):

    _cache = {}  # In-memory cache

    @classmethod
    def load(cls, args, kwargs, cache_config):
        cache_duration = cache_config.get("duration", 0)
        if cache_duration == 0:
            return (False, None)

        timestamp = datetime.now()
        arghash = ServiceFactory.hash_args([args, kwargs, cache_config])

        key = arghash  # Use hash as the key to store/retrieve from in-memory cache

        cached_data = cls._cache.get(key)
        if cached_data:
            cached_time, resp = cached_data
            if timestamp - cached_time <= timedelta(seconds=cache_duration):
                return (True, resp)

        return (False, None)

    @classmethod
    def save(cls, args, kwargs, cache_config, resp):
        cache_duration = cache_config.get("duration", 0)
        if cache_duration == 0:
            return None

        timestamp = datetime.now()
        arghash = ServiceFactory.hash_args([args, kwargs, cache_config])
        
        cls._cache[arghash] = (timestamp, resp)  # Save data with timestamp

    @classmethod
    def search_files(cls, args, kwargs, cache_config):
        # This method will be redundant if you're not working with files.
        pass

    @classmethod
    def purge_old_cache(cls):
        # If you want to add a method to remove old cache entries
        timestamp = datetime.now()
        keys_to_delete = []
        for key, (cached_time, _) in cls._cache.items():
            if timestamp - cached_time > timedelta(seconds=cache_duration):
                keys_to_delete.append(key)

        for key in keys_to_delete:
            del cls._cache[key]

"""
ServiceFactory - A service Factory
- Runs a service from the /service/ directory
- sets up Envs and loads all configurations
- Manages caching
- Single point that can be leveraged to expand / structure job running

"""

class ServiceFactory:
    instances = None

    """
    Takes a postman ENV dump, and loads it into a variable for usage as an in-class environment. (not a global env)
    """

    @staticmethod
    def parse_postman_env_to_dict(data: dict):
        # TODO Marshall or validate schema!!
        result_dict = {}
        for key in [
            "id",
            "name",
            "_postman_variable_scope",
            "_postman_exported_at",
            "_postman_exported_using",
        ]:
            if key in data:
                result_dict["__" + key] = data[key]

        values_keys = []
        for item in data.get("values", []):
            if "key" in item and "value" in item and item["enabled"]:
                result_dict[item["key"]] = item["value"]
                values_keys.append(item["key"])
        result_dict["list_of_values"] = values_keys
        return result_dict

    """
    A helper to load a json from full path. 
    
    Intention: This is because many files are needed when doing validation, and caching, and they all need to be accessed relative to the base directory. In addition, it may not always be the case that the files are local in nature. One day there could be a database for configurations, or other solutions. By centralizing file access we create a single place for all data access, so upgrades and changes can happen easily.
    """

    @staticmethod
    def load_json_bypath(path):
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        original_cwd = os.getcwd()
        os.chdir(parent_dir)
        try:
            with open(path, "r") as f:
                data = json.load(f)
        finally:
            os.chdir(original_cwd)
        return data

    """
    A helper to load a json from full path
    """

    @staticmethod
    def save_json_bypath(path, data, cls=None):
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        original_cwd = os.getcwd()
        os.chdir(parent_dir)
        try:
            with open(path, "w") as f:
                # data = json.dumps(data)
                if cls:
                    json.dump(data, f, indent=4, cls=cls)
                else:
                    json.dump(data, f, indent=4)
        except:
            import traceback as tb

            print("error in save_json_bypath:")
            print(tb.format_exc())
        finally:
            os.chdir(original_cwd)
        return data

    """
    load a service configuration
    """

    @staticmethod
    def load_service(file):
        data = load_json(["services", file], file + ".json")
        return ServiceConfig(data)

    """
    load a test configuration
    """

    @staticmethod
    def load_test(file):
        data = load_json(["tests", file], file + ".json")
        return data

    """
    load local network config
    """

    @staticmethod
    def load_network(service_config: dict, chain_id: str = None):
        assert isinstance(service_config, dict)
        assert "chain_id" in service_config
        # if no chain_id
        if not chain_id or len(chain_id) <= 0:
            chain_id = service_config["chain_id"]
        else:
            service_config["chain_id"] = chain_id
        data = load_json(["postman"], chain_id + ".json")
        data = ServiceFactory.parse_postman_env_to_dict(data)
        network_config = NetworkConfig(data)
        return network_config

    """
    take the args, and generate a unique hash string
    """
    @staticmethod
    def hash_args(args: dict):
        return ServiceBase.hash_args(args)

    
    """
        Private. Do not invoke. Internal to ServiceFactory. "Invoke_*" methods to invoke. 
    """
    def _do_cached_invoke(
        func, args: list, kwargs: dict, cache_config: dict, cache_method=None
    ):
        if cache_method == None:
            cache_method = SimpleFileCache
            CacheMethod = SimpleFileCache
            assert issubclass(CacheMethod, CacheDatabase)
        (is_cached, result) = CacheMethod.load(args, kwargs, cache_config)
        
        if is_cached:
            return result
                        
        result = func(*args, **kwargs)
        CacheMethod.save(args, kwargs, cache_config, result)
        return result
    

    """
        Private. Do not invoke. Internal to ServiceFactory. "Invoke_*" methods to invoke. 
    """
    @staticmethod
    def _create_or_lookup(module_config: dict, config: dict, network: dict):
        # Load from Cache
        assert config
        assert network
        if ServiceFactory.instances == None:
            ServiceFactory.instances = {}
        instance_hash = ServiceFactory.hash_args(
            {
                "module_config": module_config["module"],
                "config": config,
                "network": network,
            }
        )
        if instance_hash in ServiceFactory.instances:
            return ServiceFactory.instances[instance_hash]

        # Find the Module
        mod_path = module_config["module"]
        module_name = mod_path.split(".")[-1]
        class_name = module_name
        if "class" in module_config:
            class_name = module_config["class"]
        module = importlib.import_module(mod_path)
        serviceClass = getattr(module, class_name)
        assert issubclass(
            serviceClass, ServiceBase
        ), "serviceClass must be a subclass of ServiceBase"

        server_config = ServerConfig()
        # TODO: Thought. Should all/some the configs be combined into some unified ServiceContext?
        queryProxy = CrocQueryProxy(config, network)
        ServiceFactory.instances[instance_hash] = serviceClass(
            queryProxy, config, network, server_config
        )
        return ServiceFactory.instances[instance_hash]

    """
    Private. Do not invoke outside of Service Factory.
    """

    @staticmethod
    def invoke_function(
        kwargs: dict, function_config: dict, service_config: dict, service_network: dict
    ):
        assert function_config
        assert service_network
        assert "function" in function_config
        assert "params" in function_config
        if not "cache" in function_config:
            function_config["cache"] = {"duration": 0}
        inst = ServiceFactory._create_or_lookup(
            function_config, service_config, service_network
        )

        func = getattr(inst, function_config["function"])
        params = {
            param: kwargs.get(param) for param in function_config.get("params", [])
        }
        
        return ServiceFactory._do_cached_invoke(
            func, args=[], kwargs=params, cache_config=function_config["cache"]
        )

    """
        The one place all cachable, network bound, config bound, services are invoked
    """

    @staticmethod
    def invoke_registered_service(
        unknown_dict: dict, config_path: str, chain_id: str, include_data: str
    ):
        service_config = ServiceFactory.load_service(config_path)
        assert service_config
        service_network = ServiceFactory.load_network(service_config, chain_id)
        assert service_network

        return ServiceFactory.invoke_dynamic_service(
            unknown_dict, service_config, service_network, include_data
        )

    """
        The one place all cachable, network bound, config bound, services are invoked
    """

    @staticmethod
    def invoke_dynamic_service(
        args: dict, config: dict, network: dict, include_data: str
    ):
        service_config = config
        service_network = network
        assert service_config
        assert service_network
        results = {}

        for module_key, function_config in service_config["results"].items():
            results[module_key] = ServiceFactory.invoke_function(
                args, function_config, config, service_network
            )

        resp = {"config": service_config, "result": results}
        if (
            str(include_data) == "0"
        ):  # Patch back to a more permissive check. It maybe is living as a string when from API
            return resp["result"]
        else:
            return resp
