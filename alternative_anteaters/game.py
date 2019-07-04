""" Game code """

import arcade
import constants


class MyGame(arcade.Window):

    """ Main application class """

    def __init__(self):

        # Setup window
        super().__init__(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, constants.SCREEN_TITLE)

        # Sprite lists
        self.player_list = None
        self.platform_list = None

        # Player sprite
        self.player_sprite = None

        # Scrolling
        self.view_left = 0
        self.view_bottom = 0

        # Engine
        self.physics_engine = None

        # Background
        """self.background = None
        """
        arcade.set_background_color(arcade.csscolor.SKY_BLUE)

    def setup(self):

        """ Game setup. Call to restart the game """

        """# Background
        self.background = arcade.load_texture("assets/images/sky1.png")
        """

        # Create sprite lists
        self.player_list = arcade.SpriteList()
        self.platform_list = arcade.SpriteList()

        # Setup the platform
        platform = arcade.Sprite("assets/images/ground1.png", constants.TILE_SCALING)
        for x in range(-int(platform.width) * 30, constants.SCREEN_WIDTH * 10, int(platform.width)):
            platform = arcade.Sprite("assets/images/ground1.png", constants.TILE_SCALING)
            platform.center_x = x
            platform.center_y = platform.height/2
            self.platform_list.append(platform)

        # Setup the player
        self.player_sprite = arcade.Sprite("assets/images/boy1.png", constants.CHARACTER_SCALING)
        self.player_sprite.center_x = self.player_sprite.width/2
        self.player_sprite.center_y = self.player_sprite.height/2 + platform.height
        self.player_list.append(self.player_sprite)

        # Scrolling
        self.view_left = 0
        self.view_bottom = 0

        # Physics engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.platform_list,
                                                             constants.GRAVITY)

    def on_draw(self):

        """ Game rendering """

        # Clear the screen
        arcade.start_render()

        # Background
        """
        arcade.draw_texture_rectangle(constants.SCREEN_WIDTH//2,
                                      constants.SCREEN_HEIGHT//2,
                                      constants.SCREEN_WIDTH,
                                      constants.SCREEN_WIDTH,
                                      self.background)
        """

        # Draw the sprites
        self.player_list.draw()
        self.platform_list.draw()

    def on_key_press(self, key, modifiers):

        """ Called on a key-press event """

        if key == arcade.key.SPACE:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = constants.JUMP_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -constants.PLAYER_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = constants.PLAYER_SPEED

    def on_key_release(self, key, modifiers):

        """ Called on a key-release event """

        if key == arcade.key.LEFT:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def update(self, delta_time):

        """ Game logic """

        # Update all sprites
        self.physics_engine.update()

        # Scrolling

        # Viewport
        changed = False

        # Scroll left
        left_boundary = self.view_left + constants.LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + constants.SCREEN_WIDTH - constants.RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + constants.SCREEN_HEIGHT - constants.TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + constants.BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed = True

        if changed:
            self.view_buttom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Scrolling
            arcade.set_viewport(self.view_left,
                                constants.SCREEN_WIDTH + self.view_left,
                                self.view_buttom,
                                constants.SCREEN_HEIGHT + self.view_buttom)


def main():

    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
