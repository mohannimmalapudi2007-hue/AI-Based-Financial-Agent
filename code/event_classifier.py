class EventClassifier:

    def is_income(self, event):
        return event["direction"] == "credit"

    def is_expense(self, event):
        return event["direction"] == "debit"