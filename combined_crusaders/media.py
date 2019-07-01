import pygame
import os


script_dir = os.path.split(os.path.abspath(__file__))[0]
images_dir = os.path.join(script_dir, "images")
sounds_dir = os.path.join(script_dir, "sounds")


def load_image(filename):
    return pygame.image.load(os.path.join(images_dir, filename)).convert_alpha()


def load_sound(filename):
    return pygame.mixer.Sound(os.path.join(sounds_dir, filename))


def load_images():
    # return dict of str:pygame.image.
    # This will be used for sprite images, background images,
    # and all other images.
    # If this turns out to not make sense with pygame's setup,
    # like sprites use a different image form,
    # we can separate this into multiple functions.
    # Our goal is to be able to greatly simplify image loading,
    # so that we only need to say
    # PolarBear(image=our_images["polar_bear"]) instead of
    # PolarBear(image=pygame.image(Image.open("Images_Path/PolarBear.jpeg"))
    # or whatever
    return {filename.split(".")[0]: load_image(filename)
            for filename in os.listdir(images_dir)}


def load_sounds():
    # return dict of str:pygame.mixer.Sound
    # Basically the same as load_images, just with sounds
    sounds_dir = os.path.join(script_dir, "sounds")
    return {filename.split(".")[0]: load_sound(filename)
            for filename in os.listdir(sounds_dir)}
