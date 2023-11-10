import argparse
import io
import json
import sys
import warnings

from common.InvestigationTools import InvestigationTools


def run(chain_id, config_selection, include_data, unknown_dict):
    InvestigationTools.downloadFromGraphcache(config_selection, chain_id)
    InvestigationTools.parseRawOutputFile(config_selection, chain_id)
    dat = InvestigationTools.openResultsFile(config_selection)
    final_df = InvestigationTools.prepareDataDf(dat)

    validated_df = final_df[final_df["__valid"].isin([True])]
    invalidated_df = final_df[final_df["__valid"].isin([False])]
    unknown_df = final_df[final_df["__valid"].isin([None])]

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        result = {
            "chain_id": chain_id,
            "config_selection": config_selection,
            "percentage": validated_df["__valid"].sum() / validated_df.shape[0],
            "invalid": invalidated_df.shape[0],
            "valid": validated_df.shape[0],
            "unknown": unknown_df.shape[0],
            "data": {
                "valid": validated_df.to_dict("records"),
                "invalid": invalidated_df.to_dict("records"),
                "unknown": unknown_df.to_dict("records"),
            },
        }
    if str(include_data) == "0":
        del result["data"]
    return result


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="Process command line args")
        parser.add_argument("--chain_id", default=None, help="Chain Id")
        parser.add_argument(
            "--config", default="./tests/schema/schema.json", help="Path to test config"
        )
        parser.add_argument(
            "--include_data", default="0", help="Return the record data, or not"
        )
        args = parser.parse_args()

        result = run(args.chain_id, args.config, args.include_data, {})
        print(json.dumps(result, indent=4, ensure_ascii=False))
    except:
        import traceback as tb

        tb.print_exc()
