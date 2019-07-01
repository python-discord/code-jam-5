import arcade
import constants


class MyGame(arcade.Window):
    """
    Main application class
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(constants.SCREEN_WIDTH,
                         constants.SCREEN_HEIGHT,
                         constants.SCREEN_TITLE)

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        # Lists that keep track of our sprites
        self.coin_list = None
        self.wall_list = None
        self.player_list = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Physics Engine
        self.physics_engine = None

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

    def setup(self):
        """
        Sets up the game. Call this function to restart the game.
        """

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Create the Sprite Lists
        # self.coin_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.background_list = arcade.SpriteList()

        # Set up the player, specifically placing it at these coordinates
        self.player_sprite = arcade.Sprite("images/player_2/player_stand.png",
                                           constants.CHARACTER_SCALING)
        self.player_sprite.center_x = constants.PLAYER_START_X
        self.player_sprite.center_y = constants.PLAYER_START_Y
        self.player_list.append(self.player_sprite)

        # Create the `physics engine`
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.wall_list,
                                                             gravity_constant=constants.GRAVITY)

    def on_draw(self):
        """ Render the screen. """

        # Clear the screen to the background color
        arcade.start_render()

        # Draw our sprites
        self.wall_list.draw()
        self.background_list.draw()
        self.player_list.draw()

    def on_key_press(self):
        pass

    def on_key_release(self):
        pass

    def update(self, delta_time):
        """ Movement and Game logic """

        # Update Sprites
        self.physics_engine.update()


def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
