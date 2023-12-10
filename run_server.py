import argparse
import time
import psutil

from flask import Flask, jsonify, request
from flask_cors import CORS

from common.DataClasses import ServerConfig
from exceptions.ExceptionBase import (
    ExceptionBase,
    handle_exception_base,
    handle_unexpected_error,
)
from exceptions.MissingParameterException import MissingParameterException
from run_data_validation import run as run_data_validation
from run_record_validation import run as run_record_validation
from run_service import run as run_service
import logging
# Set log level to suppress HTTP request logs
log = logging.getLogger('werkzeug')
log.setLevel(logging.WARNING)

def system_resources_available(min_free_memory_percentage=10, max_cpu_percentage=80):
    virtual_memory = psutil.virtual_memory()
    cpu_usage = psutil.cpu_percent()

    return (
        virtual_memory.available
        < (virtual_memory.total * (min_free_memory_percentage / 100.0))
        or cpu_usage > max_cpu_percentage
    )


app = Flask(__name__)
CORS(
    app, origins="*"
)  # In the future we can pull CORS settings from the ServerConfig as we see fit


@app.before_request
def before_request():
    min_memory = app.config.get("MIN_FREE_MEMORY_PERCENTAGE", 10)
    max_cpu = app.config.get("MAX_CPU_PERCENTAGE", 80)
    attempts = 10
    while system_resources_available(min_memory, max_cpu) and attempts > 0:
        # Wait for 0.5 seconds and check again
        time.sleep(0.5)
        attempts -= 1

    if attempts == 0:
        # if(system_resources_available()):
        response = jsonify({"error": "System resources exceeded the threshold"})
        # response.status_code = 503
        return response, 503


app.register_error_handler(ExceptionBase, handle_exception_base)
app.register_error_handler(Exception, handle_unexpected_error)

routes = {
    "run_record_validation": {
        "function": run_record_validation,
        "arguments": ["env", "config_path", "endpoint", "include_data"],
    },
    "run_data_validation": {
        "function": run_data_validation,
        "arguments": ["env", "config_path", "include_data"],
    },
    "run": {
        "function": run_service,
        "arguments": ["env", "config_path", "include_data"],
    },
}


@app.route("/run", methods=["POST", "GET"])
def run_service():
    try:
        # Initialize an empty dictionary
        all_args = {}

        # Extract GET parameters
        all_args.update(request.args)

        # Extract POST form data
        if request.form:
            all_args.update(request.form)

        # Extract POST JSON data
        if request.is_json:
            all_args.update(request.json)

        args_positional = []
        args_kw = {}

        service_name = all_args["service"]

        if service_name not in routes:
            raise MissingParameterException("service")

        # Manually prepare the args, removing service (as it is already consumed), and setting env to a default if needed
        if "env" not in all_args:
            all_args["env"] = None
        del all_args["service"]

        route = routes[service_name]
        args_required = {arg: arg for arg in route["arguments"]}

        # Pull the required positional args
        for arg_name in route["arguments"]:
            if arg_name not in all_args:
                continue
            try:
                args_positional.append(all_args[arg_name].strip())
            except:
                args_positional.append(all_args[arg_name])
            del all_args[arg_name]
            del args_required[arg_name]
        if len(args_required) > 0:
            raise MissingParameterException(list(args_required.values())[0])

        # Add in any undeclared args, as they may be needed by a service class (analytics)
        for arg_name, arg_val in all_args.items():
            args_kw[arg_name] = arg_val

        return jsonify(route["function"](*args_positional, args_kw)), 200
    except Exception as e:
        import traceback

        return jsonify({"error": traceback.format_exc()}), 500


if __name__ == "__main__":
    sc = (
        ServerConfig()
    )  # potentially pass in vars / customize configuration if using from python directly
    parser = argparse.ArgumentParser(description="Process the port.")
    parser.add_argument(
        "--port",
        metavar="port",
        type=int,
        help="the port number to listen on",
        default=sc["PORT"],
    )
    args = parser.parse_args()
    # Setting the configuration values for memory and CPU
    app.config["MIN_FREE_MEMORY_PERCENTAGE"] = sc["MIN_RAM"]
    app.config["MAX_CPU_PERCENTAGE"] = sc["MAX_CPU"]
    if sc["FLASK_THREADED"]:
        app.run(debug=sc["FLASK_DEBUG"], port=args.port, host="0.0.0.0", threaded=True)
    else:
        app.run(
            debug=sc["FLASK_DEBUG"],
            port=args.port,
            host="0.0.0.0",
            threaded=False,
            processes=sc["FLASK_PROECESSES"],
        )
