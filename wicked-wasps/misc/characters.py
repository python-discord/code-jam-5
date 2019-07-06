class Characters:
    class Player:
        def __init__(self, member):
            self.name = str(member)
            self.member = member
            self.position = None

        def __str__(self):
            return type(self).__name__

        def powers(self):
            pass

    class polluter(Player):
        def __init__(self, member):
            super().__init__(member)

    class Zilla(polluter):
        def __init__(self, member):
            super().__init__(member)

    class green_activist(Player):
        def __init__(self, member):
            super().__init__(member)
