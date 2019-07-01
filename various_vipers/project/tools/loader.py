import json

from project.constants import USER_SETTINGS


def get_volume() -> float:
    """
    Returns the volume value from the user_settings.json file.

    Output ready for pygame.Sound.set_volume function.
    """
    with open(str(USER_SETTINGS), "r", encoding="utf-8") as f:
        data = json.load(f)

    if data["mute"]:
        return 0
    return data["volume"]


def save_volume(vol: int) -> None:
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
