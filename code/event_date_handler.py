class EventDateHandler:

    def get_effective_date(self, event):
        settlement_date = event["settlement_date"]

        if settlement_date is not None:
            return settlement_date

        return event["event_date"]