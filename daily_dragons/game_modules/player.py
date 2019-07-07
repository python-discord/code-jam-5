class Player:
    def __init__(self, name: str, net_worth: int = 1_000_000_000) -> None:
        self.name = name
        self.net_worth = net_worth

    def get_roi(self, roi: float) -> None:
        investment_return = 100_000_000 * roi
        self.net_worth += investment_return

    def __str__(self) -> str:
        player = (
            f"{self.name} is currently worth {self.net_worth}"
            f" and has {self.social_standing} social standing"
        )

        return player
