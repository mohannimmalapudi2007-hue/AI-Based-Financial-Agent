class CurrencyConverter:

    def __init__(self, exchange_rates):
        self.exchange_rates = exchange_rates

    def convert(self, amount, from_currency, to_currency, rate_date):

        if from_currency == to_currency:
            return amount

        rates = self.exchange_rates[
            (self.exchange_rates["rate_date"] == rate_date) &
            (self.exchange_rates["from_currency"] == from_currency) &
            (self.exchange_rates["to_currency"] == to_currency)
        ]

        if rates.empty:
            raise ValueError(
                f"Exchange rate not found: "
                f"{from_currency} -> {to_currency} on {rate_date}"
            )

        rate = rates.iloc[0]["rate"]

        return amount * rate