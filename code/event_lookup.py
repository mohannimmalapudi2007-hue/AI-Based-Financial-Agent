class EventLookup:
    def __init__(self, events):
        self.events = events

    def get_user_events(self, user_id):
        user_events = self.events[
            self.events["user_id"] == user_id
        ]

        return user_events.copy()