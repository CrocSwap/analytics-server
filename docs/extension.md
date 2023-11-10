# Logical Architecture

The Analytics Server is responsible for providing meta-data services to ambient front-end applications. If you are thinking of extending the Analytics Server, this is the right document. First, architecture will be discovered.

Overall, the Analytics server can be invoked as a CLI, an API, or a Docker container. To harmonzie these invocation vectors, all invocations run through the ServiceFactory. The ServiceFactory has the job of looking up the services' configurations, checking to see if a response is cached, and if required, invokes the services. The ServiceFactory also keeps the instance (ServiceBase) in memory, for further queries. 

Below the ServiceFactory, there are two kinds of classes that comprise the server. The ServiceBase is a generic endpoint, that when invoked, returns a precise result. Since responses are cached, this system is likely not appropriate for drawing random numbers while the caching is configured for an endpoint. The second service is a validator, and this validator is more complex, and actually pulls a large data frame fro GCGO, attaching its validation logic to each row. 
<img width="754" alt="image" src="https://github.com/hyplabs/crocswap_audit_tools/assets/4418215/1ea88a5f-ecb1-427d-9d1c-fcdd0ce3aa57">

# Adding a Service
Adding a new service takes two steps. Fist, the service must be coded as a python file. Second, the service must be registered in the ./services/ directory. After this, the service can be readily used. Below we will cover the required steps.

1. Copy the example service, and save a python file in ./common
```
from .ServiceBase import ServiceBase
class ServiceHelloWorldEcho(ServiceBase):
    def serviceFunc(self,arg): 
        return {"arg":arg,"message":"hello world"}
```
2. This service we have created can be saved in ServiceHelloWorldEcho.py . It is expected to echo back any argument passed to arg, and a hello world message, back to a user
3. Next is registration. create a /services/helloworldecho/config.json , and add in the following content.
   - chain_id: This is the default chain id that the service operates on
   - supported_chain_ids: these are the chain ids that the endpoint can support
   - results: This dict defines the list of endpoints that generate results..
   - results.value: This dict defines a ServiceConfiguration, and configures a cache location, duration in seconds, module, target function, and required parameters
```
{
    "chain_id": "0x1",
    "supported_chain_ids": [
        "0x1",
        "0x5"
    ],
    "results": {
        "value": {
            "cache": {
                "duration": 1,
                "path": "./services/example/results.json"
            },
            "module": "common.ServiceExample",
            "function": "serviceFunc",
            "params": [
                "arg"
            ]
        }
    }
}
```
4. After this, the command will be avaliable on the CLI, and API:
# Service Constants
The System has a configuration system that resides in the common folder. When within a class, all configuration values are readily avaliable as:
```
from .ServiceBase import ServiceBase
class ServiceHelloWorldEcho(ServiceBase):
    def serviceFunc(self,arg):
        # A w3 instance is provided, bound to the correct EVM chain automagically
        ens_name = self.w3.ens.name(SOME_KIND_OF_ADDRESS)

        # An instance of the crocQuery contract, connected to the right EVM, and loaded with the right ABI is avaliable
        retVal = self.crocQuery.contract.functions.queryRangePosition(**params).call()
       
        # Service Configuration values - Custom Constants set in the configuration json defined in /service/ENDPOINT/ENDPOINT.json
        service_key_values = self.get_service_config()

        # Network Configuration values - Constant values set about the chain bound to the service
        network_key_values = self.get_network_config()

        # Server Configuration values - Constants (man from the .env) that tell you about the server environment
        server_key_values = self.get_server_config()

        return {"arg":arg,"message":"hello world"}
```

<img width="687" alt="image" src="https://github.com/hyplabs/crocswap_audit_tools/assets/4418215/c78c36f8-e016-47cb-81b9-8626b3b5674d">

# On Validators
Validators may be deprecated in the fututre. At present we will avoid documenting them. In addition, the validator code (In InvestigationTools.py, and ValidatorGCGO.py) may in fact be removed in a future release, as the bulk validation tools has not been used frequently in production.

# Adding New Chains
The Network Configuration process is extensive, as each chain has many special addresses required by both the services and validators. The files are given as chain IDs, and the default chains (and templates) are ./postman/0x1.json and ./postman/0x5.json . Within, you will see many constant values that are critical to the operation of the chain. Within this file, as well, special private constants can be bound with "{{CONSTANT}}". In these cases the NetworkConfig class will search the .env file for the targeted value.

The values below will be avaliable as a key-value store in the network config, and bound as selected the chain_id parameter (or the default chain in the service config).

Importantly, the legacy of this project, is as a postman project. So if you want, it should be possible to import the configuration into postman as a environment, and re export it when you are finished playing with constants. This can be useful if you want to experiment directly with the GCGO servers, via postman, or are desiging support for new L2s. However, this process of adding an L2 is not yet documented.

./postman/0x1.json 
```
{
	"id": "480360ec-fedc-42ab-a4c5-8ad6edce7a5f",
	"name": "Görli on ambindexer.net",
	"values": [
		{
			"key": "chainId",
			"value": "0x1",
			"type": "default",
			"enabled": true
		},
		{
			"key": "dai",
			"value": "0x6b175474e89094c44da98b954eedeac495271d0f",
			"type": "default",
			"enabled": true
		},
		{
			"key": "usdc",
			"value": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
			"type": "default",
			"enabled": true
		},
		{
			"key": "account_1",
			"value": "{{CHAIN_0X1_ACCOUNT_1}}",
			"type": "default",
			"enabled": true
		},
...
```


