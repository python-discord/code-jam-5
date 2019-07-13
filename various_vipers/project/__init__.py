import logging

from project.constants import LOG_LEVEL


# Console handler for logging
console_handler = logging.StreamHandler()
console_handler.setLevel(LOG_LEVEL)

logging.basicConfig(level=LOG_LEVEL, handlers=[console_handler])
