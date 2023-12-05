from web3 import Web3

from .ServiceBase import ServiceBase


class ValidatorUserTxs(ServiceBase):
    def validTransaction(self, tx, endpoint):
        transaction = self.w3.eth.get_transaction(tx["txHash"])
        if transaction is not None:
            return {"valid": True, "transaction": transaction}
        else:
            return {"valid": False, "error": "Transaction does not exist"}


class ValidatorUserPositions(ServiceBase):
    def validRangePosition(
        self, data, endpoint
    ):  # A basic validator that cross validates liquidity in a record
        params = {
            "owner": Web3.to_checksum_address(data["user"]),
            "base": Web3.to_checksum_address(data["base"]),
            "quote": Web3.to_checksum_address(data["quote"]),
            "poolIdx": data["poolIdx"],
            "lowerTick": data["bidTick"],
            "upperTick": data["askTick"],
        }
        retVal = self.crocQuery.contract.functions.queryRangePosition(**params).call()
        valid = False
        if retVal[0] == data["concLiq"]:
            valid = True

            return {"valid": valid, "retVal": retVal}
        else:
            # print("Found invalid match"+str(params) + str(retVal))
            return {
                "valid": False,
                "message": "ValidatorUserPositions.py, concLiq did not match",
                "retVal": retVal,
            }


class ValidatorUserLimitOrders(ServiceBase):
    #
    # TX LEVEL
    #

    def validKnockoutTokens(
        self, data, endpoint
    ):  # A basic validator that cross validates liquidity
        params = {
            "owner": Web3.to_checksum_address(data["user"]),
            "base": Web3.to_checksum_address(data["base"]),
            "quote": Web3.to_checksum_address(data["quote"]),
            "pivot": data["pivotTime"],
            "isBid": data["isBid"],
            "poolIdx": data["poolIdx"],
            "lowerTick": data["bidTick"],
            "upperTick": data["askTick"],
        }
        if params["pivot"] == 0:
            knockout_pivot = self.crocQuery.contract.functions.queryKnockoutPivot(
                Web3.to_checksum_address(data["base"]),
                Web3.to_checksum_address(data["quote"]),
                data["poolIdx"],
                data["isBid"],
                data["bidTick"] if data["isBid"] else data["askTick"],
            ).call()
            # Extract the second element from the returned tuple
            params["pivot"] = knockout_pivot[1]

        retVal = self.crocQuery.contract.functions.queryKnockoutTokens(**params).call()
        # if random.random() > 0.90: #USED TO POISON THE DATA, DURING DEVELOPMENT OF A VALIDATOR
        #    retVal[0] = -10 # Poisoning the data is an important part of testing any validation method
        [contractLiq, _, _, knockedOut] = retVal

        valid = False
        liq = data["concLiq"]
        if knockedOut:
            liq = data["claimableLiq"]

        if contractLiq == liq:
            valid = True

            return {"valid": valid, "retVal": retVal}
        else:
            print("Found invalid match" + str(params) + str(retVal))
            return {
                "valid": False,
                "message": "ValidatorUserPositions.py, liq did not match",
                "retVal": retVal,
            }

    #
    # DATA LEVEL
    #
    def validNoDuplicate(self, data, endpoint):
        records = data["data"]
        duplicates = []

        for i in range(len(records)):
            for j in range(i + 1, len(records)):
                if self.areOrdersDuplicates(records[i], records[j]):
                    duplicates.append((records[i], records[j]))

        if duplicates:
            return {
                "valid": False,
                "message": "Duplicate orders found",
                "retVal": duplicates,
            }
        else:
            return {
                "valid": True,
                "message": "No duplicate orders found",
                "retVal": [],
            }

    def areOrdersDuplicates(self, order1, order2):
        # Check if unique fields are the same
        unique_fields = [
            "base",
            "quote",
            "poolIdx",
            "bidTick",
            "askTick",
            "user",
            "ambientLiq",
            "concLiq",
        ]
        for field in unique_fields:
            if order1[field] != order2[field]:
                return False

        # Check if numeric fields are the same
        numeric_fields = [
            "ambientLiq",
            "concLiq",
            "claimableLiq",
        ]  # Add more fields if necessary
        for field in numeric_fields:
            if order1[field] != 0 and order1[field] == order2[field]:
                return True

        return False


class ValidatorUserBalanceTokens(ServiceBase):
    def validUserBalanceTokens(
        self, data, endpoint
    ):  # A basic validator that cross validates user tokens
        # Get data from subgraph
        tx = data["data"]
        user_address = Web3.to_checksum_address(tx["user"])
        query = f"""
            {{
                userBalances(first: 1000, orderBy: time, orderDirection: desc, where: {{ user: "{user_address}" }}) {{
                    user
                    token
                }}
            }}
        """
        retVal = self.crocQuery.query_subgraph(query)
        user_balances_result = retVal["data"]["userBalances"]
        user_tokens_result = [balance["token"] for balance in user_balances_result]

        # if random.random() > 0.90: #USED TO POISON THE DATA, DURING DEVELOPMENT OF A VALIDATOR
        #    retVal[0] = -10 # Poisoning the data is an important part of testing any validation method
        if set(user_tokens_result) == set(tx["tokens"]):
            return {"valid": True, "retVal": user_balances_result}
        else:
            print("Found invalid match" + str(user_address) + str(retVal))
            return {
                "valid": False,
                "message": "ValidatorUserBalanceTokens.py, user tokens did not match",
                "retVal": retVal,
            }


ValidatorPoolPositions = ValidatorUserPositions
ValidatorUserPositions = ValidatorUserPositions
ValidatorPositionStats = ValidatorUserPositions
ValidatorUserPoolPositions = ValidatorUserPositions
ValidatorUserPoolLimitOrders = ValidatorUserLimitOrders
ValidatorLimitStats = ValidatorUserLimitOrders
ValidatorPoolLimitOrders = ValidatorUserLimitOrders
