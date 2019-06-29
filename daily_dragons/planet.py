class Planet:
    def __init__(self):
        self.bio_diversity = 0
        self.temperature = 0
        self.co2 = 0
        self.habitable_land = 0

    @property
    def scoreboard(self):
        current_stats = {
            "bio_diversity": str(self.bio_diversity),
            "temperature": str(self.temperature),
            "co2": str(self.co2),
            "habitable_land": str(self.habitable_land),
        }

        return current_stats

    def __str__(self):
        current_stats = (
            f"bio_diversity: {str(self.bio_diversity)} \n"
            f"temperature: {str(self.temperature)} \n"
            f"co2: {str(self.co2)} \n"
            f"habitable_land: {str(self.habitable_land)} \n"
        )

        return current_stats
