from .constants import CollisionType, TileType
from .object import PhysicalObject
from .resources import SNOWBALL_IMAGE


class Snowball(PhysicalObject):
    collision_type = CollisionType.SNOWBALL

    def __init__(self, x, y, velocity_x, velocity_y, image=None):
        super().__init__(img=SNOWBALL_IMAGE, x=x, y=y)
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y

    def update(self, dt):
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt

    def collide_tile(self, tile):
        if tile.tile_type == TileType.WALL_TILE:
            self.space.remove(self)
