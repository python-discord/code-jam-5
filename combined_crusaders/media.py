import pygame
import os
import functools


script_dir = os.path.split(os.path.abspath(__file__))[0]
images_dir = os.path.join(script_dir, "images")
sounds_dir = os.path.join(script_dir, "sounds")


@functools.lru_cache()
def load_image(filename):
    loaded_image = pygame.image.load(os.path.join(images_dir, filename))
    return loaded_image.convert_alpha()


@functools.lru_cache()
def load_sound(filename):
    return pygame.mixer.Sound(os.path.join(sounds_dir, filename))


class ImageLoader:
    def __init__(self):
        self.with_extension = {filename.split(".")[0]: filename
                               for filename in os.listdir(images_dir)}

    def __getitem__(self, key):
        """Loads the image.
        KeyError will be naturally raised if it does not exist.
        """
        filename = self.with_extension[key]
        return load_image(filename)


class SoundLoader:
    def __init__(self):
        self.with_extension = {filename.split(".")[0]: filename
                               for filename in os.listdir(sounds_dir)}

    def __getitem__(self, key):
        """Loads the sound.
        KeyError will be naturally raised if it does not exist.
        """
        filename = self.with_extension[key]
        return load_sound(filename)


images = ImageLoader()
sounds = SoundLoader()
