import pygame as pg

from project.constants import BG_MUSIC, SOUNDS_BUTTONS as SND
from project.utils.loader import Load


class Sound:
    """Represents all sounds and settings for the UI."""

    pg.mixer.init()
    pg.mixer.music.load(str(BG_MUSIC))
    pg.mixer.music.play(-1)

    click = pg.mixer.Sound(str(SND["click3"]))
    check = pg.mixer.Sound(str(SND["switch1"]))
    task_completed = pg.mixer.Sound(str(SND["twoTone2"]))
    task_failed = pg.mixer.Sound(str(SND["phaserUp1"]))

    @staticmethod
    def update(vol):
        """Updates the volume of the sounds and music."""
        vol /= 100  # edit the volume to be in 0.0 - 1.0 range

        Sound.click.set_volume(vol)
        Sound.check.set_volume(vol)
        Sound.task_completed.set_volume(vol)
        Sound.task_failed.set_volume(vol)
        pg.mixer.music.set_volume(vol / 6)


Sound.update(Load.volume())
