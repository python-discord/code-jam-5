class Player:
    def __init__(self, name: str, net_worth: int = 0, social_standing: int = 0) -> None:
        self.name = name
        self.net_worth = net_worth
        self.social_standing = social_standing

    def get_roi(self, roi: float) -> None:
        self.net_worth *= roi

    def __str__(self) -> str:
        player = (
            f"{self.name} is currently worth {self.net_worth}"
            f" and has {self.social_standing} social standing"
        )

        return player
