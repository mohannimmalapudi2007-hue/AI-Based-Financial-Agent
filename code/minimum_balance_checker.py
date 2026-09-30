class MinimumBalanceChecker:

    def is_safe(self, balance, minimum_balance):
        return balance >= minimum_balance

    def find_lowest_balance(self, timeline):
        if not timeline:
            return None

        return min(
            item["balance_after"]
            for item in timeline
        )