class BalanceCalculator:

    def apply_event(self, balance, event):
        amount = event["amount"]

        if event["direction"] == "credit":
            return balance + amount

        if event["direction"] == "debit":
            return balance - amount

        raise ValueError(
            f"Unknown event direction: {event['direction']}"
        )