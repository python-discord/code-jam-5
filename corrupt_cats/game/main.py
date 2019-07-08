"""Main script that handles UI part of the project."""
import random
import os
import time
import itertools
import datetime
from typing import Dict, Set, List, Tuple, Union
from pathlib import Path

import arcade
import pyglet

from .core.accidents import accident_dict
from .core.country import Country
from .core.temperature import Temperature as T
from .core.constants import constants

from .ui.classes import NSprite


class Container:
    """Class that holds main variables of the game."""
    def __init__(self):
        self.path = Path(os.path.dirname(os.path.abspath(__file__)))
        self.sprites = {}
        self.sounds = {}
        self.countries = []
        self.population = 0
        self.year = datetime.datetime.now().year  # getting current year
        self.font = str(self.path/"pixel_font")

    def upd_year(self):
        self.year += 1

    def upd_total_population(self):
        self.population = sum(
            country.population for country in self.countries
        )

    def insert(
        self, sprites: Dict[str, Union[arcade.Sprite, NSprite]] = {},
        sounds: Dict[str, arcade.Sound] = {}, countries: List[Country] = []
    ):
        self.sprites = sprites
        self.sounds = sounds
        self.countries = countries
        self.upd_total_population()


container = Container()


def _init_sprites_and_textures() -> Dict[str, NSprite]:
    # we expect our project to be run from 'corrupt_cats' folder
    sprites = {}
    path = container.path/"sprites"
    for image_path in path.iterdir():
        key = image_path.name
        if "button" not in key:
            sprite = NSprite(image_path)
        else:
            if "idle" in key:
                sprite = NSprite(image_path)
            else:
                sprite = arcade.load_texture(image_path)
        sprites[key] = sprite
    ordered = {k: sprites[k] for k in sorted(sprites.keys())}
    return ordered


def _init_sounds() -> Dict[str, arcade.Sound]:
    sounds = {}
    path = container.path/"sounds"
    for sound_path in path.iterdir():
        key = sound_path.name
        sound = arcade.Sound(sound_path)
        sounds[key] = sound
    return sounds


def _make_world_info():
    """Makes a bar that shows world info."""
    countries = container.countries
    _population = list(country.population for country in countries)
    _temp = list(country.temperature for country in countries)
    _cfc = list(country.cfc for country in countries)
    total = sum(_population)
    x, n = container.population, total
    approx_cfc = sum(_cfc)/len(countries)
    hottest = list(filter(lambda x: x.temperature >= max(_temp), countries))[0]
    hpopulation = list(filter(lambda x: x.population >= max(_population), countries))[0]
    dead = [c.name for c in filter(lambda x: x.dead, countries)]
    alive = [c.name for c in filter(lambda x: not x.dead, countries)]
    info = (
        f"Start population: {x}\n"
        + f"Average CFC level: {approx_cfc}\n"
        + f"Country with the highest population: {hpopulation.name} "
        + f"[{str(hpopulation.population)}]\n"
        + f"Hottest country: {hottest.name} [{str(hottest.temperature)}]\n"
        + f"Alive countries: {len(alive)} [{n} humans]\n"
        + f"Dead countries: {len(dead)} [{x-n} humans]\n"
        + "NOTE: STATS DO NOT AUTOMATICALLY UPDATE.\nCLICK BUTTON TO REFRESH.\n"
        + "[Click left mouse button to close.]\n[Esc to exit simulation]"
    )
    return WorldInfoBar(info)


def _gen_rand_coord(wh_set: Set[Tuple[int, int]]) -> Tuple[int, int]:
    idx = random.randrange(len(wh_set))
    return list(wh_set)[idx]  # sets don't support indexing


def _upd_center_coords(
    wh_set: Set[Tuple[int, int]],
    sprite: Union[arcade.Sprite, NSprite]
):
    sprite.center_x, sprite.center_y = _gen_rand_coord(wh_set)


def _del_points(
    wh_set: Set[Tuple[int, int]],
    sprite: NSprite, prev_sprites: List[NSprite]
) -> Set[Tuple[int, int]]:
    """Deletes points from 'wh_set' to avoid collision while generating."""
    ret = wh_set
    for prev_sprite in prev_sprites:
        # zip sprite sizes; size -> Tuple[width: int, height: int]
        # sum width and height of prev_sprite and sprite
        size_sum = [sum(t) for t in zip(sprite.size, prev_sprite.size)]
        # divide elements in size_sum by -2 and turn them into integers
        half = [int(-elem/2) for elem in size_sum]
        # sum elements from prev_sprite.center tuple and from b
        # returns Tuple[int, int]
        # +16 and -16 to make country collision impossible
        x0, y0 = tuple(sum(t)-16 for t in zip(half, prev_sprite.center))  # up-left corner
        x1, y1 = tuple(sum(t)+16+1 for t in zip(size_sum, (x0, y0)))  # down-right corner
        to_cut = {*itertools.product(range(x0, x1), range(y0, y1))}  # all coords to cut
        ret = ret-to_cut  # cutting
    return set(sorted(ret))


def _generate_countries(sprites: Dict[str, NSprite]) -> List[Country]:
    previous, res = [], []
    country_sprites = {
        k: v.copy() for k, v in sprites.items() if k.startswith("country")
    }
    wh_set = set(
        itertools.product(
            range(64, constants.SCREEN_WIDTH-64), range(64, constants.SCREEN_HEIGHT-64)
        )
    )
    gen_set = wh_set
    for i in range(constants.COUNTRY_AMOUNT):
        key = random.choice(
            list(country_sprites.keys())
        )
        sprite = country_sprites.pop(key)
        if previous:
            gen_set = _del_points(wh_set, sprite, previous)
        _upd_center_coords(gen_set, sprite)
        previous.append(sprite)
        country = Country()
        country.attach_sprite(sprite)
        res.append(country)
    return res


def _prepare_elements():
    spdict = _init_sprites_and_textures()
    sdict = _init_sounds()
    countries = _generate_countries(spdict)
    container.insert(spdict, sdict, countries)


class WorldInfoBar:
    def __init__(self, info):
        self.sprite = container.sprites.get("info_tab.png")
        self.info = info
        self.sprite.center_x, self.sprite.center_y = (
            constants.SCREEN_WIDTH//2, constants.SCREEN_HEIGHT//2
        )

    def draw(self):
        x, y = self.sprite.center_x, self.sprite.center_y
        self.sprite.draw()
        arcade.draw_text(
            self.info, x, y, arcade.color.WHITE,
            font_size=14, font_name=container.font,
            width=self.sprite.width-32, align="center",
            anchor_x="center", anchor_y="center"
        )


class CountryInfoBar:
    def __init__(self, game):
        self.linked = game
        self.sprite = container.sprites.get("cinfo_tab.png")
        self.sprite.center_x, self.sprite.center_y = (
            constants.SCREEN_WIDTH-(self.sprite.width//2),
            constants.SCREEN_HEIGHT-(self.sprite.height//2)
        )

    def draw(self):
        c = self.linked.country
        self.sprite.draw()
        x, y = self.sprite.center_x, self.sprite.center_y
        if c is not None:
            status = "alive" if not c.dead else "dead"
            info = f"{c.name}: [t={str(c.temperature)}] [cfc={c.cfc}] [status={status}] " \
                f"[{c.population} humans]"
        else:
            info = "Click a country to view information about it."
        arcade.draw_text(
            info, x, y, arcade.color.WHITE,
            font_size=14, font_name=container.font,
            width=self.sprite.width-16, align="center",
            anchor_x="center", anchor_y="center"
        )


class SpriteButton:
    def __init__(
        self, center_x, center_y, width, height, text, color: str = 'red',
        button_height=2, font_size=14, font_name=container.font
    ):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size
        self.font = font_name
        self.button_height = button_height
        self.is_pressed = False
        self.ready = False

        textures = []
        sp_and_textures = {k: v for k, v in container.sprites.items() if color in k}
        for k, v in sp_and_textures.items():
            if isinstance(v, arcade.Sprite):
                self.sprite = v.copy()
            else:
                textures.append(v)
        for texture in textures:
            self.sprite.append_texture(texture)

    def set_ready(self, to: bool = False):
        self.ready = bool(to)

    def draw(self):
        if self.is_pressed:
            self.sprite.set_texture(1)
        elif self.ready:
            self.sprite.set_texture(2)
        else:
            self.sprite.set_texture(0)

        x, y = self.center_x, self.center_y
        self.sprite.center_x, self.sprite.center_y = x, y
        z = self.button_height
        if not self.is_pressed:
            x -= z
            y += z
        self.sprite.draw()
        arcade.draw_text(
            self.text, x, y, arcade.color.WHITE,
            font_size=self.font_size, font_name=self.font,
            width=self.width, align="center",
            anchor_x="center", anchor_y="center"
        )


class FuncButton(SpriteButton):
    def __init__(self, center_x, center_y, text, color, function, func_args=[]):
        super().__init__(center_x, constants.SCREEN_HEIGHT - center_y, 128, 32, text, color)
        self.func = function
        self.args = func_args

    def run(self):
        if self.is_pressed:
            self.func(*self.args)


class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.game_over = False
        self.paused = False
        self.info = None
        self.country = None
        self.tick = 0

    def _init_easter_egg(self):
        if random.randint(1, 20) == 13:  # 5% chance
            self.set_caption('Lemon')

    def _set_icon(self):
        img = pyglet.image.load(container.path/"sprites"/"icon.png")
        self.set_icon(img)

    def setup(self):
        arcade.set_background_color(constants.WATER_COLOR)
        self._set_icon()
        # init easter egg
        self._init_easter_egg()
        # setting up GUI elements
        self.button_list = []
        self.bar_list = []
        self.country_list = [c.sprite for c in container.countries]
        country_info_bar = CountryInfoBar(self)
        world_info_button = FuncButton(64, 16, "World Status", "red", self.make_world_info)
        pause_button = FuncButton(64, 48, "Pause", "blue", self.switch_mode)
        self.button_list.append(world_info_button)
        self.button_list.append(pause_button)
        self.bar_list.append(country_info_bar)
        arcade.play_sound(container.sounds.get("bg_ambient.wav"))

    def on_draw(self):
        arcade.start_render()
        for sprite in self.country_list:
            sprite.draw()
        for button in self.button_list:
            button.draw()
        if self.game_over:
            text = "ENTIRE HUMANITY WAS KILLED DUE\n" \
                "TO CLIMATE CHANGE AND GLOBAL WARMING.\n" \
                "PRESS [ESCAPE] TO END SIMULATION.\n" \
                "P.S. CHECK YOUR TERMINAL OUTPUT."
            arcade.draw_text(
                text, constants.SCREEN_WIDTH//2, constants.SCREEN_HEIGHT//2,
                arcade.color.RED, font_name=container.font, font_size=32,
                width=constants.SCREEN_WIDTH, align="center",
                anchor_x="center", anchor_y="center"
            )
        for bar in self.bar_list:
            bar.draw()

        arcade.draw_text(
            f"YEAR {container.year}", 92, 32, arcade.color.BLACK,
            font_name=container.font, font_size=20,
            width=constants.SCREEN_WIDTH, align="center",
            anchor_x="center", anchor_y="center"
        )
        _temp = [c.temperature.value for c in container.countries]
        _avg = T(float("{:.2f}".format(sum(_temp)/len(_temp))))
        color = (int(_avg*1.5), 0, 0, 255)
        arcade.draw_text(
            f"AVG: {str(_avg)}", 92, 64, color,
            font_name=container.font, font_size=20,
            width=constants.SCREEN_WIDTH, align="center",
            anchor_x="center", anchor_y="center"
        )

    def update(self, delta_time):
        self.tick += 1
        if not(self.tick % 6120):  # if we need to reset a song
            arcade.play_sound(container.sounds.get("bg_ambient.wav"))
        if not (self.tick % 60) and not self.paused:  # 1s = 1 day
            container.upd_year()
            print(f"[o] Year {container.year}")
            for country in container.countries:
                country.upd()
                if not country.dead:
                    for accident in country.possible_accidents:
                        accident_dict.get(accident).dispatch_on(country)
            if all(country.dead for country in container.countries) and not self.game_over:
                print(
                    "[-] Population of the Earth has completely vanished.\n"
                    + "[-] Please, be more friendly to the environment.\n"
                    + "[-] We should protect our planet, otherwise our 'simulation' can be real."
                )
                self.game_over = True
                if not self.paused: self.switch_mode()

    def switch_mode(self):
        self.paused = bool(self.paused ^ 1)  # opposite

    def on_key_release(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.close_window()
            print("[n] Wait 3 seconds...")
            time.sleep(3)

    def on_mouse_motion(self, x, y, dx, dy):
        for button in self.button_list:
            p = button.sprite.points
            x0, y0, x1, y1 = map(int, (*p[0], *p[2]))
            if x in range(x0, x1) and y in range(y0, y1):
                button.ready = True
            else:
                button.ready = False

    def on_mouse_press(self, x, y, button, key_modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:

            if self.info is not None:
                self.bar_list.remove(self.info)
                self.info = None
            further = True
            for b in self.button_list:
                p = b.sprite.points
                x0, y0, x1, y1 = map(int, (*p[0], *p[2]))
                if x in range(x0, x1) and y in range(y0, y1):
                    b.is_pressed = True
                    if isinstance(b, FuncButton):
                        b.run()
                    further = False
            if not further:
                return
            for country in container.countries:
                p = country.sprite.points
                x0, y0, x1, y1 = map(int, (*p[0], *p[2]))
                if x in range(x0, x1) and y in range(y0, y1):
                    self.country = country
                    return
            self.country = None

    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            for b in self.button_list:
                b.is_pressed = False

    def resume(self):
        self.paused = False

    def pause(self):
        self.paused = True

    def make_world_info(self):
        if self.info is None:
            self.info = _make_world_info()
            self.bar_list.append(self.info)


def main():
    print("[+] Preparing...")
    try:
        _prepare_elements()
    except ValueError:  # if preparation failed
        print("[-] Failed to load... Restarting...")
        main()  # reload
    print("[+] Starting...")
    game = Game(
        constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, constants.SCREEN_TITLE
    )
    game.setup()
    print("[+] Welcome to CorruptClimate. This is a simulation of global warming.")
    print("[+] Have Fun <3 - team corrupt_cats")
    print(f"[o] Year {container.year}")
    arcade.run()
    print("[?] See you later :3")


main()
