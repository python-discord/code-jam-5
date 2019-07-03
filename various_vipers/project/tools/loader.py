import json

from project.constants import USER_SETTINGS


class Load:
    """Represents static methods for loading json data."""

    with open(str(USER_SETTINGS), "r", encoding="utf-8") as f:
        data = json.load(f)

    @staticmethod
    def volume() -> float:
        """
        Returns the volume value from the user_settings.json file.

        Output ready for pygame.Sound.set_volume function.
        """
        if Load.data["mute"]:
            return 0
        return Load.data["volume"]

    @staticmethod
    def show_fps() -> float:
        """Returns show fps bool."""
        return Load.data["show_fps"]


class Save:
    """Represents static methods for saving to json format."""

    with open(str(USER_SETTINGS), "r", encoding="utf-8") as f:
        data = json.load(f)

    @staticmethod
    def save_volume(vol: int) -> None:
        """Saves the volume from project.UI.page.options slider."""
        Save.data["volume"] = vol

        if vol == 0:
            Save.data["mute"] = True
        else:
            Save.data["mute"] = False

        with open(str(USER_SETTINGS), "w", encoding="utf-8") as f:
            json.dump(Save.data, f)
