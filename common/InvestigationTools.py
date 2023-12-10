import importlib
import json
import sys

import pandas as pd
from pandas import json_normalize

from common.NewmanTest import NewmanTest
from common.ServiceFactory import ServiceFactory

sys.path.append("../")


class InvestigationTools:
    @staticmethod
    def downloadFromGraphcache(config_selection, chain_id=None):
        nt = NewmanTest()
        config = ServiceFactory.load_test(config_selection)
        network_config = ServiceFactory.load_network(config, chain_id=chain_id)
        if chain_id:
            config["chain_id"] = chain_id
        # print("Selecting Environemnt: "+config["environment"])

        # TODO: Refactor env_vars out
        # Disabling the env_vars for now
        config["env_vars"] = {}
        nt.load_data(
            config["collection"],
            config["chain_id"],
            config["outpath"],
            service_network=network_config,
            env_vars=config["env_vars"],
        )

    @staticmethod
    def parseRawOutputFile(config_selecton, chain_id, endpoints=None):
        nt = NewmanTest()
        nt.parse_newman_output(config_selecton, chain_id, endpoints)

    @staticmethod
    def openResultsFile(config_selecton):
        config = ServiceFactory.load_test(config_selecton)
        return ServiceFactory.load_json_bypath(config["resultspath"])

    @staticmethod
    def prepareRecordDf(dat):
        dfResults = pd.DataFrame(dat["results"])
        final_df = pd.DataFrame()

        for k, v in dfResults.iterrows():
            try:
                # Data could be an array or a single record
                data = v["responseBody"]["data"]
                data_records = []
                if isinstance(data, dict):
                    data_records = [data]
                else:
                    data_records = data

                summary_rows = pd.DataFrame(data_records)
                df_result = pd.DataFrame(summary_rows.index, columns=["Index"])
                df_result["data"] = summary_rows.to_dict("records")
                df_result["url"] = v["url"]
                endpoint = v["url"].split("/")
                endpoint = endpoint[4]
                try:
                    endpoint = endpoint.split("?")
                    endpoint = endpoint[0]
                except:
                    pass
                df_result["endpoint"] = endpoint
                try:
                    df_result["__validationResult"] = summary_rows.get(
                        "__validationResult", False
                    )
                    df_result["__validationResult"] = summary_rows["__validationResult"]
                except:
                    import traceback as tb

                    default_value = {
                        "valid": None,
                        "error": "missing in prepareRecordDf",
                        "except": tb.format_exc(),
                        "url": v["url"],
                    }
                    df_result["__validationResult"] = [
                        default_value for _ in range(len(df_result))
                    ]

                df_result["__valid"] = summary_rows.get("__valid", False)
                final_df = pd.concat([final_df, df_result], ignore_index=True)

            except:
                pass  # Sometimes we can not pull records if there is no data field, or the data field is not a list
                # import traceback as tb
                # tb.print_exc()
                # return {}

        final_df = final_df.reset_index(drop=True)
        # Drop the 'Index' column
        if "Index" in final_df.columns:
            final_df = final_df.drop(columns="Index")
        return final_df

    @staticmethod
    def prepareDataDf(dat):
        final_df = pd.DataFrame(dat["results"])

        def validate_json(cell):
            if isinstance(cell, dict):
                return cell
            try:
                json_object = json.loads(cell)
                if isinstance(json_object, dict):
                    return json_object
            except (ValueError, TypeError):
                pass
            return {}

        final_df["responseBody"] = final_df["responseBody"].apply(validate_json)
        inner = pd.DataFrame(list(final_df["responseBody"]))
        # return inner
        final_df["__valid"] = inner["__valid"]
        final_df["__validationResult"] = inner["__validationResult"]
        return final_df

    @staticmethod
    def ReportCrossvalidationSummary(kargs):
        for k in [
            "collection",
            "environment",
            "outpath",
            "contract_version",
            "envs",
            "all_validation_functions",
            "validator_file",
        ]:
            assert k in kargs

        Validator_module = importlib.import_module(kargs["validator_file"])
        Validator = Validator_module.Validator
        validator = Validator(kargs["contract_version"])

        summary_results = []
        index = 0
        for env in kargs["envs"]:
            try:
                index = index + 1
                resultspath = f"../analysis/phase_1/health_{index}_results.json"
                env_vars = env
                InvestigationTools.downloadFromGraphcache(
                    kargs["collection"], kargs["environment"], kargs["outpath"], env
                )

                InvestigationTools.parseRawOutputFile(
                    validator,
                    kargs["outpath"],
                    kargs["resultspath"],
                    kargs["all_validation_functions"],
                )

                dat = InvestigationTools.openResultsFile(kargs["resultspath"])
                final_df = InvestigationTools.prepareRecordDf(dat)
                # final_df['positionType'] = final_df.apply(lambda row: row['data'].get('positionType', False), axis=1)

                valid = final_df[final_df["__valid"].isin([True])].shape[0]
                unknown = final_df[final_df["__valid"].isin([None])].shape[0]
                invalid = final_df[final_df["__valid"].isin([False])].shape[0]
                if "__name" in env:
                    name = env["__name"]
                name = None
                result = {
                    "name": env["__name"],
                    "server": env["cacheDomain"],
                    "trial_file": kargs["resultspath"],
                    "percentage": valid / final_df.shape[0],
                    "invalid": invalid,
                    "valid": valid,
                    "unknown": unknown,
                }
                summary_results.append(result)
            except:
                import traceback as tb

                result = {
                    "name": env["__name"],
                    "server": env["cacheDomain"],
                    "trial_file": kargs["resultspath"],
                    "error": tb.format_exc(),
                    "percentage": None,
                    "invalid": None,
                    "valid": None,
                    "unknown": None,
                }
                summary_results.append(result)

        summary_df = pd.DataFrame(summary_results)
        return summary_df
