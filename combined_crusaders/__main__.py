# Some of this skeleton was stolen from the aliens pygame example
import pygame
import os
from pygame.locals import KEYDOWN, K_ESCAPE, QUIT, Rect
# I hate * imports but I want it to work for the skeleton

script_dir = os.path.split(os.path.abspath(__file__))[0]
if not pygame.image.get_extended():
    raise SystemExit("Sorry, extended image module required")


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
    return {"polar_bear": pygame.image.load(
        os.path.join(script_dir, 'images', "polar_bear.jpeg")).convert()}


def load_sounds():
    # return dict of str:pygame.mixer.Sound
    # Basically the same as load_images, just with sounds
    return {"beep": pygame.mixer.Sound(
        os.path.join(script_dir, 'sounds', "beep.wav"))}


pygame.init()
screenrect = Rect(0, 0, 640, 480)
fullscreen = False
winstyle = 0
bestdepth = pygame.display.mode_ok(screenrect.size, winstyle, 32)
screen = pygame.display.set_mode(screenrect.size, winstyle, bestdepth)
images = load_images()
sounds = load_sounds()
# Having this at module-level feels icky,
# but it's better than having at class level or object level.
# We can change this later once we having a working game
# OOOO, wait, we can use a cool functools thing I learned about with some
# load_image and load_sound that lazy loads and caches the result!
# I'll handle that.


class Button(pygame.sprite.Sprite):
    def __init__(self):
        self.image = images["polar_bear"]
        self.rect = self.image.get_rect()

    def on_click(self):
        """I made this method up; figure out how we detect button clicks"""
        pass


class ButtonPanel:
    def __init__(self):
        pass
        # TODO put a button here, or multiple, depending on what we decide
        # we want the game to look like


class CC:  # TODO game name goes here
    """Class should hold information about state of game
    This includes current environment value and such.
    Sprites and such should probably be held at class-level or module-level
     instead? maybe? idk lol
    """
    def __init__(self):
        self.exit_requested = False
        self.score = 0
        self.environment_image = None  # images["environment_neutral"]
        self.button_panel = ButtonPanel()
        self.clock = pygame.time.Clock()
        self.fullscreen = False
        # If we want to display the score, that shouldn't be too hard. If
        # we want to display the environment only instead, that works too.
        # TODO display environment_image in background
        # TODO add button panel to screen

    def update(self):
        """Called on new frame"""
        # TODO update score field, update environment image,
        # update anything we need to update in the button panel
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN
                                      and event.key == K_ESCAPE):
                self.exit_requested = True
                return

        keystate = pygame.key.get_pressed()
        pass
        self.clock.tick(40)

    def play(self):
        """Begins the game. Detect any exits and exit gracefully."""
        while not self.exit_requested:
            self.update()
        pygame.quit()


def main():
    if pygame.mixer and not pygame.mixer.get_init():
        raise OSError("Can't play sounds, sounds are required")
    # There's an issue with sounds that I need to work on; uploading this
    # version to the skeleton, I'll try to fix it.
    # pygame.mixer.music.load(sounds["beep"])
    # pygame.mixer.music.play(-1)
    game = CC()
    game.play()


if __name__ == "__main__":
    main()
