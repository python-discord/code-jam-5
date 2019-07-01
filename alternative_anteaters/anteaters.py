import arcade


# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 1
TILE_SCALING = 0.5
COIN_SCALING = 0.5


class MyGame(arcade.Window):
    """
    Main application class
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

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
        self.viem_left = 0

    def setup(self):
        """
        Sets up the game. Call this function to restart the game.
        """

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.viem_left = 0

        # Create the Sprite Lists
        self.coin_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()

        # Set up the player, specifically placing it at these coordinates
        self.player_sprite = arcade.Sprite()

    def on_draw(self):
        """ Render the screen. """

        arcade.start_render()
        # Code to draw the screen goes here.


def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
