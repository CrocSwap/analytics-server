# Framework Testing
python3 run_record_validation.py --config example_single --endpoint user_positions
python3 run_service.py --config example --arg1 EXAMPLE --arg2 EXAMPLE2 --include_data=1
python3 run_service.py --config example --arg1 EXAMPLE --arg2 EXAMPLE2 --include_data=0


# CLI Operations
python3 run_record_validation.py --config cv_user_positions --include_data 0 --endpoint user_pool_positions
python3 run_record_validation.py --config cv_user_limit_orders --include_data 0 --endpoint user_limit_orders
python3 run_data_validation.py --config schema --include_data 0
python3 run_record_validation.py --chain_id 0x1 --config cv_user_limit_orders --include_data 0 --endpoint user_limit_orders
python3 run_record_validation.py --chain_id 0x5 --config cv_user_limit_orders --include_data 0 --endpoint user_limit_orders

python3 run_data_validation.py --chain_id 0x1 --config schema --include_data 0

python3 run_record_validation.py --chain_id 0x5 --config cv_user_limit_orders --include_data 0 --endpoint user_limit_orders
python3 run_data_validation.py --chain_id 0x5 --config schema --include_data 0


# TODO Services have been updated to (a) handle env, (b) use nice Formatting
# This work should also be (i) finished and (ii) applied to the validator as well
# (The main difference between the validator, and service, is a validator runs NewmanTest first, and applies the service to the resulting rows, gathering the results. But they are indeed very logically simiar)
python3 run_service.py --config example --arg1 EXAMPLE --arg2 EXAMPLE2 --include_data 1
python3 run_service.py --config example --arg1 EXAMPLE --arg2 EXAMPLE2 --include_data 0
python3 run_service.py --config all_pool_stats  --include_data 1
python3 run_service.py --config validation  --include_data 1
python3 run_service.py --config ens_address  --include_data 0 --address 0xE09de95d2A8A73aA4bFa6f118Cd1dcb3c64910Dc

python3 run_service.py --config complete_pool_stats  --include_data 1 --pool_id 0xd417ff54652c09bd9f31f216b1a2e5d1e28c1dce1ba840c40d16f2b4d09b5902
python3 run_service.py --config complete_pool_stats  --include_data 0 --pool_id 0xd417ff54652c09bd9f31f216b1a2e5d1e28c1dce1ba840c40d16f2b4d09b5902
python3 run_service.py --config complete_pool_stats  --include_data 0 --chain_id 0x1 --base 0x0000000000000000000000000000000000000000 --quote 0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48 --pool_idx 420
python3 run_service.py --chain_id 0x1 --config complete_pool_stats  --include_data 1 --pool_id 0xd417ff54652c09bd9f31f216b1a2e5d1e28c1dce1ba840c40d16f2b4d09b5902


python3 run_service.py --chain_id 0x1 --config price  --include_data 1 --token_address 0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48

http://52.10.90.134:5000/run?service=run&config_path=price&include_data=0&token=0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48


# CLI to run the server
python3 run_server.py 
# Once the server is running, try out a cross validation query
# http://SERVER:5000/run?service=run_record_validation&config_path=./tests/cv_user_positions/cv_user_positions_goerli.json&endpoint=user_txs&include_data=0
# http://SERVER:5000/run?service=run_data_validation&config_path=./tests/schema/schema.json&include_data=0
# http://SERVER:5000/run?service=run&config_path=example&arg1=hello&arg2=world&include_data=1
# http://SERVER:5000/run?service=run&config_path=example&arg1=hello&arg2=world&include_data=0
# http://SERVER:5000/run?service=run&config_path=complete_pool_stats&arg1=hello&arg2=world&include_data=0
# http://SERVER:5000/run?service=run&config_path=complete_pool_stats&arg1=hello&arg2=world&include_data=0
# http://SERVER:5000/run?service=run&config_path=validation&include_data=0
# http://SERVER:5000/run?service=run&config_path=price&include_data=0&token_address=0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48