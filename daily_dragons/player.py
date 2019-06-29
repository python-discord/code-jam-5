class Player:
    def __init__(self, name):
        self.name = name
        self.net_worth = 0
        self.social_standing = 0

    def __str__(self):
        player = (
            f"{self.name} is currently worth {self.net_worth}"
            f" and has {self.social_standing} social standing"
        )

        return player
