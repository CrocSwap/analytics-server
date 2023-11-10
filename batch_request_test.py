from common.ServiceFactory import ServiceFactory
import json
"""
This script tests the batch_requests service by sending a batch of requests to the service and printing the result.

The batch of requests is defined in the `args` dictionary, which contains a list of request objects. Each request object
contains a `config_path` field, a `req_id` field, and an `args` field. The `config_path` field specifies the configuration
path for the request, the `req_id` field specifies the request ID, and the `args` field contains the arguments for the request.

The `ServiceFactory.invoke_registered_service` method is used to invoke the `batch_requests` service with the `args` dictionary,
the chain ID, and the gas price.

The result of the service call is printed to the console. (Json format)
"""

args = {"data":json.loads("""
{
  "req": [
    {
      "config_path": "ens_address",
      "req_id": 0,
      "args": {
        "address": "0xE09de95d2A8A73aA4bFa6f118Cd1dcb3c64910Dc"
      }
    },
    {
      "config_path": "complete_pool_stats",
      "req_id": 1,
      "args": {
        "chain_id": "0x1",
        "pool_id": "0x02413926f87427de1790f178f5a59ad63096045810116e18b451f26440c15e56"
      }
    },
    {
      "config_path": "price",
      "req_id": 3,
      "args": {
        "chain_id": "0x1",
        "token_address": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
      }
    }
  ]
}
""")}


result = ServiceFactory.invoke_registered_service(
    args, "batch_requests", "0x1", "0"
)
print(result)