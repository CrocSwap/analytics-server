import argparse
import json

from common.ServiceFactory import ServiceFactory


def run(chain_id: str, service_name: str, include_data: str, unknown_dict: dict):
    args = unknown_dict
    if "chain_id" in args:
        chain_id = args["chain_id"]

    # print("args",args)
    result = ServiceFactory.invoke_registered_service(
        args, service_name, chain_id, include_data
    )
    return result


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="Process command line args")
        parser.add_argument("--chain_id", default=None, help="Chain Id")
        parser.add_argument(
            "--config",
            default="./services/example/example.json",
            help="Path to test config",
        )
        parser.add_argument(
            "--include_data", default="0", help="Return the meta data, or not"
        )

        args, unknown = parser.parse_known_args()
        # convert unknown arguments into dict
        unknown_dict = {}
        for arg in unknown:
            if arg.startswith(("--")):
                key = arg.lstrip("-")
                if key in unknown_dict:
                    unknown_dict[key] = [unknown_dict[key]]
                unknown_dict[key] = None
            elif key in unknown_dict:
                if isinstance(unknown_dict[key], list):
                    unknown_dict[key].append(arg)
                else:
                    unknown_dict[key] = arg
            else:
                key = arg
                unknown_dict[key] = None
        result = run(args.chain_id, args.config, args.include_data, unknown_dict)
        print(json.dumps(result, indent=4, ensure_ascii=False))
    except:
        import traceback as tb

        print(
            "error with "
            + str([args.chain_id, args.config, args.include_data, str(unknown_dict)])
        )
        tb.print_exc()
