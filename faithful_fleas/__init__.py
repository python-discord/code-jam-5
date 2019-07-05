import logging


# Console handler prints to terminal
console_handler = logging.StreamHandler()
level = logging.DEBUG
console_handler.setLevel(level)


# Silence irrelevant loggers
logging.getLogger('discord').setLevel(logging.ERROR)
logging.getLogger('aiosqlite').setLevel(logging.ERROR)
logging.getLogger('websockets').setLevel(logging.ERROR)

# Setup new logging configuration
logging.basicConfig(
    format='%(asctime)s : %(name)s : %(levelname)s: %(message)s',
    datefmt="%D %H:%M:%S",
    level=logging.DEBUG,
    handlers=[console_handler]
)
logging.getLogger().info('Logging setup complete!')
