import pickle

from project.constants import USER_SETTINGS
from project.utils.singleton import Singleton


class UserData(Singleton):
    """User data holds settings, hiscores, etc.

    This class will be serialized and saved to file to be loaded
        each time the game is launched.
    """

    volume: float = 50
    mute: bool = False
    show_fps: bool = False

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
