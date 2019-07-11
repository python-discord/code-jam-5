import random

from .temperature import Temperature as t
from .accidents import accident_dict
from .constants import conf, constants as c
from .utils.functions import gen_temp_mul, check_temp, get_rand_keys
from .utils.name_gen import NameGen

desc_list = conf.get("descriptions", [])
adict = accident_dict
ng = NameGen()


class Country:
    def __init__(self):
        self.name = ng.generate_name(random.randint(1, 5))
        self.start_t = t(random.randint(c.MIN_TEMP, c.MAX_TEMP))
        self.type = check_temp(self.start_t, c.MAX_TEMP, c.MIN_TEMP)
        self.population = random.randint(c.MIN_POPULATION, c.MAX_POPULATION)
        self.industry_level = gen_temp_mul(1, 2)
        self.possible_accidents = get_rand_keys(adict)
        self.temperature = self.start_t.copy()
        self.dead = False
        self.sprite = None
        self.cfc = 0
        self.accident_count = 0
        self.dpd_recieve = 0

    def __repr__(self):
        ret = f"<{self.name}: t={self.temperature}, cfc={self.cfc}, population={self.population}>"
        return ret

    def __str__(self):
        res = f"[{self.name}][Temperature:{self.temperature}][CFC:{self.cfc}]" \
            f"[Population:{self.population}]"
        return res

    def attach_sprite(self, sprite):
        self.sprite = sprite

    def info(self, page):
        """Shows info about country. You can see pages and their numbers below:
        0: name, climate and start_temperature;
        1: how people handle temperatures;
        2: current population;
        3: accident_count;
        4: possible accidents;
        5: country "CFC" level.
        """
        cases = {
            0: str(self.start_t),
            2: self.population,
            3: self.accident_count,
            4: self.possible_accidents,
            5: self.cfc
        }

        base = desc_list[page]
        content = cases.get(page)

        if isinstance(base, dict):
            base = base.get(str(self.type))

        if isinstance(content, list):
            content = ', '.join(content)

        res = base.format(self.name, content)
        return res

    def accept_damage_from(self, accident):
        main = f"[x] {accident.name} has happened in {self.name}."
        if not self.dead:
            main += f" It has taken {accident.dmg} lives."
            self.dpd_recieve += accident.dpd
            self.population -= accident.dmg
        if self.population <= 0:
            self.kill()
        print(main)

    def upd(self):
        """Function that implements main temperature change logic"""
        a = self.industry_level
        b = self.temperature.value
        c = self.population
        d = a * (b/10 + abs(c)**(1/2)/100)
        self.cfc += int(d)
        a = self.cfc**(1/2)/150
        b = float("{:.2f}".format(a))
        self.temperature += b
        self.temperature = self.temperature.copy()
        if self.dead:
            return
        a = self.cfc
        b = self.temperature.value
        c = abs(int(a*b/10))
        self.population += (
            (-c)*50 if (self.temperature-self.start_t) > 40 else c
        )
        if self.population <= 0:
            self.kill()

    def kill(self):
        if not self.dead:
            self.sprite._set_alpha(200)
            self.population = 0
            self.dead = True
            print(f"[-] All people in {self.name} have died.")
