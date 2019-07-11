import random

from .constants import conf

adesc_dict = conf.get("accidents")


class AbstractAccident:
    def __init__(self):
        self.name = type(self).__name__
        self.dict = adesc_dict.get(self.name)
        if self.dict is None:
            raise NotImplementedError
        self.min_dmg = self.dict.get("min_affect")
        self.max_dmg = self.dict.get("max_affect")
        self.dpd = self.dict.get("damage_per_day", 0)
        self.highest_chance = 5
        self.dmg = self.gen_damage()
        self.chance = 0

    def __repr__(self):
        ret = f"<{self.name}: damage={self.dmg}, dpd={self.dpd}>"
        return ret

    def __str__(self):
        res = f"[{self.name}][Damage:{self.damage}]"
        return res

    @property
    def desc(self):
        return self.dict.get("description")

    def gen_damage(self):
        return random.randint(self.min_dmg, self.max_dmg)

    def dispatch_on(self, country) -> None:
        if random.randint(1, 20) in range(1, self.chance):
            country.accept_damage_from(self)  # if country is affected
        else:
            self.chance += 1
        if self.chance == self.highest_chance:  # to be updated when temperature goes up
            self.chance = 0
        self.dmg = self.gen_damage()


class Tsunami(AbstractAccident):
    def __init__(self):
        super().__init__()


class Wildfire(AbstractAccident):
    def __init__(self):
        super().__init__()


class Flood(AbstractAccident):
    def __init__(self):
        super().__init__()


class Tornado(AbstractAccident):
    def __init__(self):
        super().__init__()


class Heatwave(AbstractAccident):
    def __init__(self):
        super().__init__()


class Earthquake(AbstractAccident):
    def __init__(self):
        super().__init__()


accident_dict = {
    "tsunami": Tsunami(),
    "wildfire": Wildfire(),
    "flood": Flood(),
    "tornado": Tornado(),
    "heatwave": Heatwave(),
    "earthquake": Earthquake()
}
