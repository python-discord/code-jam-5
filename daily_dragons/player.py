class Player:
    def __init__(self, name: str, net_worth: int = 0, social_standing: int = 0) -> None:
        self.name = name
        self.net_worth = 0
        self.social_standing = 0

    def __str__(self) -> str:
        player = (
            f"{self.name} is currently worth {self.net_worth}"
            f" and has {self.social_standing} social standing"
        )

        return player
