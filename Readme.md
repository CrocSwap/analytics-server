# Analytics Server
These tools provide a method to submit data queries to the ambient network. This code base can be imported into python, run as a CLI, hosted as a flask API, or a docker container. 


# Install
First, you must set up a `.env` and a `./docker/.env`  according to [`./docker/example.env`](./docker/example.env) 
## CLI Quickstart
To get going with this project, on the command line, you can quickly run these commands to get the cli running. First, you must set up a .env and a ./build/.env according to 
```
pip3 install -r requirements.txt
python3 run_service.py --config example --arg1 EXAMPLE --arg2 EXAMPLE2 --include_data=1
```
Please check out the many command examples in [`docs/examples.md`](./docs/examples.md) for more information.


## LocalAPI Quickstart
You may want to run this as an api. The steps are similar
```
pip3 install -r requirements.txt
python3 run_server.py
```
Please check out the many command examples in [`docs/examples.md`](./docs/examples.md) for more information.

## Docker Quickstart
You may want to run this in a container.
```
./docker/build.sh
./docker/run.sh
```
Please check out the detailed docker instructions [`docker/readme.md`](./docker/readme.md) for more information.

Please check out the many command examples in [`docs/examples.md`](./docs/examples.md) for more information.
# Setup and Deployment Process

Refer to [`docs/setup.md`](./docs/setup.md) for more information

# Testing the server
Refer to [`docs/tests.md`](./docs/tests.md) for more information

# Core Concepts
The Golang API serves swaps and other data, but there can be concern about the accuracy of the golang API. Thus, this code base downloads API results, and validates that data in a variety of ways. 

## Data & Records
First, data can be validated on a DATA and RECORD basis. DATA is defined as an entire data set returned from and APT GET request. RECORD is an optional element from a DATA query. This framework supports validations for both. It is generally the case that a record is an order.

## Decorators & Validators
Each validator (or data-decorator) may query external data sources. Some (such as the Schema validators) compare api query results hard coded information, leading to a determination of validity. Other validation scripts (such as the cross validators) cross reference data with the graph or smart contracts, and compare the blockchain with the API. When the validation engine runs, each validator's results is summerized into a "valid": true or false value, and saved within each record. 


##### (Also) In the Future
We also have plans to extend and add Decorators. Specifically, classes that may grab an API result, such as all assets locked on chain, and combine that with public data, to generate analytics results.

An example validated record follows:
```
[{'valid': False,
  'validSchema': {'valid': False,
   'message': 'pool_limit_orders failedpasses validation',
   'retVal': {'data': {'0': {'crossTime': ['Field must be a positive integer.']},
     '1': {'crossTime': ['Field must be a positive integer.']}, 
     '113': {'crossTime': ['Field must be a positive integer.']}}}}},
 {'valid': True,
  'validNoDuplicate': {'valid': True,
   'message': 'No duplicate orders found',
   'retVal': []}}]
```

In this example, a record has two validation results. One resutl, from validSchema, is retuning false, and has some useful retVal information for consideration. A second result is from a no duplication checker, and is stating that no duplicate orders are found. It is also worth considering the structure of a simple validator, as the system is desiged to be easy to extend:


```
//ValidatorUserTxs.py
from web3 import Web3
import json,os
from .ValidatorBase import ValidatorBase

class ValidatorUserTxs(ValidatorBase):
    def validTransaction(self,tx, endpoint):
        transaction = self.w3.eth.get_transaction(tx["txHash"])
        if transaction is not None:
            return {"valid": True,
                    "transaction":transaction}
        else:
            return {"valid": False, "error": "Transaction does not exist"}
        
    def validate_txs(self,tx, endpoint):
        results = self.run_validation(tx,[("validTransaction", self.validTransaction)], endpoint)
        return [tx, results]        

```
This class, called ValidatorUserTxs, verifies if any record has a valid transaction on the blockchain. Each validator is given an instance of self.w3 to make queries. The return value of validate_txs is very important, is expected to be exact by the rest of the validation engine. Specificically, the first argument must be the DATA or RECORD, and the second return value must be the results. results is a specially constructed dict, built by the ValidatorBase class.


### Postman based
The list of queries to run, and paramaters to send, is all configured in postman. The postman collections and environments are stored in the 


## Overview
Our testing and validation codebase primarily consists of three key python classes (which can be reused in a variety of contexts):

- NewmanTest: A Postman-based testing tool that allows for dynamic testing of API endpoints, py automating postman collection execution and validation of the responses.

- Validator: A validation component responsible for verifying the integrity of the transaction records generated from the tests. This. can be dropped into any response processor, (client side, testing framework, or even server side)

- CrocQuery: A bridge component that connects the testing suite with the CrocSwap smart contracts on the Ethereum blockchain. This is a small driver class that sends requests, and packages requests, responses, and any tags, in one place.

## NewmanTest
NewmanTest, built upon the popular Postman tool, facilitates the testing of API endpoints. Each endpoint is rigorously tested, and the responses are automatically validated against predefined schema structures. This ensures that all the endpoints are functioning as expected and that the data they return is in the correct format. NewmanTest is flexible, allowing for tests to be added or modified as per the requirements of the CrocSwap platform.

## Validator
The Validator component is designed to scrutinize the results obtained from NewmanTest. It validates these results against real-time data on the blockchain, making sure our transaction records are in sync with the actual state of the smart contracts. It includes various validation methods that can be customized to suit the specific validation needs of any transaction record.

# CrocQuery
CrocQuery is the bridge between our testing suite and the Ethereum blockchain. It allows our validation methods to interact directly with the CrocSwap smart contracts deployed on the Ethereum network. The class is designed to validate various types of positions within the CrocSwap contract. By using CrocQuery, we ensure that our local transaction records align with the actual state of the blockchain.
