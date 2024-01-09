# Testing the server

## Purpose
The primary purpose of the script is to run the server in a variety of test scenarios (Basic, Load), across various interface channels (Python, CLI, LocalAPI, StagingAPI). This CLI tool allows for the user to easily move up and down the testing interface channels, while investigating either basic operations or load testing. IMPORTANT: The unit test currently only checks if the endpoint returns valid json. These tests do not check the accuracy fo the results.

# Getting Started

## Prerequisites
- Python installed on your system.
- Basic understanding of Python's unittest framework.

## Usage
The script is executed from the command line with specific arguments to define the command and the test case to be run.

# Command-Line Arguments
1. --command: Specifies the command configuration to use. Options include:
  1. CLICommand: Uses a command line tool for testing.
  1. StageAPI: Uses a hardcoded staging server for testing.
  1. LocalAPI: Starts and uses a local API for testing.
  1. Python: Uses native Python imports for testing. This is the default option.
2. --test: Specifies the test case to execute. Options include:
  1. BasicTest: Runs a basic set of 4 commands to validate operation.
  1. LoadTest: Executes an aggressive locust unit test. This option may lead to failures and crashes depending on the configuration of LoadTest. Use with caution.

## Running
```
python script_name.py --command [COMMAND_OPTION] --test [TEST_OPTION]
```
Replace [COMMAND_OPTION] with one of the command options (CLICommand, StageAPI, LocalAPI, Python) and [TEST_OPTION] with a test option (BasicTest, LoadTest).

## Examples
Execute a Load Test against the python class import
```
python run_test.py --command Python --test LoadTest 
```
Execute a Basic Test against the StagingAPI
```
python run_test.py --command StageAPI --test BasicTest
```