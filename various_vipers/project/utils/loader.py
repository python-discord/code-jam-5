import json
import os

from project.constants import PATH_DATA, USER_SETTINGS


def assert_user_settings():
    """Asserts that user settings file is present in data."""
    if "user_setting.json" not in os.listdir(str(PATH_DATA)):
        default_data = {"volume": 100, "mute": False, "show_fps": True}
        with open(str(USER_SETTINGS), "w", encoding="utf-8") as f:
            json.dump(default_data, f)


assert_user_settings()


class Load:
    """Represents static methods for loading json data."""

    @staticmethod
    def volume() -> float:
        """
        Returns the volume value from the user_settings.json file.

        Output ready for pygame.Sound.set_volume function.
        """
        with open(str(USER_SETTINGS), "r", encoding="utf-8") as f:
            data = json.load(f)

        if data["mute"]:
            return 0
        return data["volume"]

    @staticmethod
    def show_fps() -> float:
        """Returns show fps bool."""
        return data["show_fps"]


class Save:
    """Represents static methods for saving to json format."""

    @staticmethod
    def volume(vol: int) -> None:
        """Saves the volume from project.UI.page.options slider."""
        with open(str(USER_SETTINGS), "r", encoding="utf-8") as f:
            data = json.load(f)

        data["volume"] = vol

        if vol == 0:
            data["mute"] = True
        else:
            data["mute"] = False

        with open(str(USER_SETTINGS), "w", encoding="utf-8") as f:
            json.dump(data, f)

    def show_fps(state: bool) -> None:
        """Saves the volume from project.UI.page.options slider."""
        with open(str(USER_SETTINGS), "r", encoding="utf-8") as f:
            data = json.load(f)

        data["show_fps"] = state

        with open(str(USER_SETTINGS), "w", encoding="utf-8") as f:
            json.dump(data, f)
