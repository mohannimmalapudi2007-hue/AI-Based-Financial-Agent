from datetime import datetime, timedelta


class ForecastWindow:

    def __init__(self, days=90):
        self.days = days

    def get_end_date(self, start_date):
        start = datetime.strptime(start_date, "%Y-%m-%d").date()

        end = start + timedelta(days=self.days)

        return end.strftime("%Y-%m-%d")

    def is_within_window(self, event_date, start_date):
        end_date = self.get_end_date(start_date)

        return start_date <= event_date <= end_date