class Characters:
    class Player:
        def __init__(self, member, position):  # , *args, **kwargs):
            self.name = str(member)
            self.member = member
            self.position = position
            self.eliminated = False
            self.is_active = False
            self.in_power = False

        def __str__(self):
            return type(self).__name__

        def powers(self):
            pass

    class Denier(Player):
        def __init__(self, *args, **kwargs):
            super().__init__(*args)

    class Zilla(polluter):
        def __init__(self, *args, **kwargs):
            super().__init__(*args)

    class Activist(Player):
        def __init__(self, *args, **kwargs):
            super().__init__(*args)
