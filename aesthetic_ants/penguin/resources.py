import pyglet

loader = pyglet.resource.Loader(path="../resources")


def load_image(filename: str, centered: bool = False):
    image = loader.image(filename)

    if centered:
        image.anchor_x = image.width // 2
        image.anchor_y = image.width // 2

    return image


ENEMY_IMAGE = load_image("circle.png", centered=True)
PLAYER_IMAGE = load_image("penguin.png", centered=True)
