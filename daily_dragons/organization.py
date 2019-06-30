class Organization:
    """
    Organizations come in two varities: Companies or NGOs
    Generally companies will negatively affect the planet
    while NGOs / non-profits will have positive affects
    """

    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description

    def __str__(self) -> str:
        summary = f"{self.name}\n{self.description}\n"

        return summary
