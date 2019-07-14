import pygame
import os
import functools


script_dir = os.path.split(os.path.abspath(__file__))[0]
images_dir = os.path.join(script_dir, "images")
sounds_dir = os.path.join(script_dir, "sounds")
music_path = os.path.join(sounds_dir, "phyromusic.ogg")


@functools.lru_cache()
def load_image(filename):
    """Load an image from the images directory"""
    loaded_image = pygame.image.load(os.path.join(images_dir, filename))
    return loaded_image.convert_alpha()


@functools.lru_cache()
def load_sound(filename):
    """Load a sound from the sounds directory"""
    return pygame.mixer.Sound(os.path.join(sounds_dir, filename))


class ImageLoader:
    """Lazy loader for images
    with_extension: dict mapping extensionless to extensioned filenames
    """
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
    """Lazy loader for sounds
    with_extension: dict mapping extensionless to extensioned filenames
    """
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
