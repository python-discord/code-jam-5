import pickle

from project.constants import USER_SETTINGS
from project.utils.singleton import Singleton


class UserData(Singleton):
    """User data holds settings, hiscores, etc.

    This class will be serialized and saved to file to be loaded
        each time the game is launched.
    """

    sound_volume: float = 30
    music_volume: float = 25

    sound_mute: bool = False
    music_mute: bool = False

    show_fps: bool = False

    # Game will be less detailed, but increases fps.
    # Drawing large, transparent images slows the game alot,
    #  this option disables inneficient detail draws.
    boost_fps: bool = False

    # Hiscores (seconds survived) in each game difficulty
    hiscore_medieval: float = 0
    hiscore_modern: float = 0
    hiscore_future: float = 0

    def save(self) -> None:
        """Serialize and save user data to the file."""
        with open(str(USER_SETTINGS), "wb+") as f:
            pickle.dump(self, f)

    def load(self) -> None:
        """Load and unserialize user data from the file."""
        try:
            with open(str(USER_SETTINGS), "rb") as f:
                self = pickle.load(f)
        except FileNotFoundError:
            self.save()
