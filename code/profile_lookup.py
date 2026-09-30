class ProfileLookup:
    def __init__(self, profiles):
        self.profiles = profiles

    def get_profile(self, user_id):
        profile = self.profiles[
            self.profiles["user_id"] == user_id
        ]

        if profile.empty:
            raise ValueError(f"Profile not found for user: {user_id}")

        return profile.iloc[0].to_dict()