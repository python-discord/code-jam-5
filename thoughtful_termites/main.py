import platform
from thoughtful_termites.printer import windows


if __name__ == "__main__":
    system = platform.system()

    if system == "Windows":
        windows.listener()
