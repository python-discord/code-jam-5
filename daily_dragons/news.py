class News:
    def __init__(self, author: str, headline: str, long_description: str) -> None:
        self.author = author
        self.headline = headline
        self.long_description = long_description

    @property
    def short_description(self) -> str:
        if len(self.long_description) < 80:
            return self.long_description
        else:
            return self.long_description[:80]

    def __str__(self) -> str:
        output = f"{self.headline}\nBy: {self.author}\n\n{self.short_description}"
        return output
