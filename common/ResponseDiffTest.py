import json
import os
from cgi import test
from datetime import datetime
from jycm.helper import make_ignore_order_func, render_to_html
from jycm.jycm import YouchamaJsonDiffer

class ResponseDiffTest:
    def __init__(self, control_filepath, test_filepath, output_filepath, mode_file):
        self.control_filepath = control_filepath
        self.test_filepath = test_filepath
        self.output_filepath = output_filepath

        with open(mode_file, "r") as f:
            self.keys_to_check = json.load(f)
            #TODO assert something about the keys

    def get_all_json_filepaths_in_dir(self, dir):
        result = []
        for filename in os.listdir(dir):
            if filename.endswith(".json"):  # check if the file is a JSON file
                result.append(os.path.join(dir, filename))
        return result

    def load_json_file(self, file_path):
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            print(f"Error: The file {file_path} does not exist.")
        except json.JSONDecodeError:
            print(f"Error: The file {file_path} is not a valid JSON file.")
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
        return None

    """
    json_results = [
        {
            name: ...,
            ...
        }
    ]
    """

    def _find_response_in_results(self, json_results, test_name):
        for obj in json_results:
            if obj.get("name") == test_name:
                return obj
        return None  # Return None if no matching name is found

    def run(self):
        control = self.load_json_file(self.control_filepath)
        test = self.load_json_file(self.test_filepath)

        test_results = []
        for control_result in control["results"]:
            test_name = control_result["name"]
            response_body = control_result["responseBody"]

            test_result = self._find_response_in_results(test["results"], test_name)
            test_response_body = test_result["responseBody"]

            print(f"Running comparison for {test_name}")
            test_result = self.compare_json_objects(
                test_name, response_body, test_response_body
            )
            test_results.append(test_result)

        print("ResponseDiffTest: saving test results")
        self.save_test_results(test_results)

    def compare_json_objects(self, test_name, control, response):
        # construct default / passing test result
        test_result = {
            "name": test_name,
            "summary_key_diff": [],
            "full_log": {},
            "pass": True,
        }

        # Calc diff
        ycm = YouchamaJsonDiffer(
            control,
            response,
            ignore_order_func=make_ignore_order_func(["^ignore_order$"]),
        )

        try:
            diff_result = ycm.get_diff()
        except Exception:
            import traceback as tb

            tb.print_exc()

            test_result["pass"] = False
            return test_result

        # Log the diff and generate interactive HTML viewer for it if there was a difference + write out.
        # NOTE: we avoid dumping diff on empty result {'just4vis:pairs': []} which is always present.
        is_actually_diff = (
            len(diff_result.keys()) > 1 or len(diff_result.get("just4vis:pairs")) > 1
        )
        all_keys = set()

        # If no difference is present, then just return
        if not is_actually_diff:
            return test_result

        # Get fields that are difference
        # TODO: Filter by keys that we care about given the test mode
        for key in diff_result:
            for item in diff_result[key]:
                # Grab only text after the last "->" in the path
                all_keys.add(item["right_path"].split("->")[-1])

        # Filter all_keys to only higlight the fields we want to check
        if self.keys_to_check:
            fields_to_check_set = set(self.keys_to_check)
            all_keys = all_keys.intersection(fields_to_check_set)

        # convert all_keys to a list
        all_keys = list(all_keys)

        # if there are no fields that are different, just return
        if not all_keys:
            return test_result

        test_result["pass"] = False
        test_result["summary_key_diff"] = all_keys
        test_result["full_log"] = diff_result

        return test_result

    def save_test_results(self, test_results):
        num_pass = len([r for r in test_results if r["pass"]])

        summary_output = {
            "timestamp": datetime.utcnow().isoformat(),
            "totalPass": num_pass,
            "totalFail": len(test_results) - num_pass,
            "results": test_results,
        }

        summary_output_txt = json.dumps(summary_output, indent=4)
        with open(self.output_filepath, "w") as summary_log_f:
            summary_log_f.write(f"\n{summary_output_txt}")
