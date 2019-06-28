import logging
import os
import src.game as game
import src.graphics as graphics


# logging
log = logging.getLogger("main")
log.info("initialising logging")
log.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter(
    fmt='%(asctime)s - %(name)s - %(levelname)s : %(message)s',
    datefmt='%Y-%j %H:%M:%S'))
log.addHandler(stream_handler)
log.info("Logging initialised")


log.info("Initialising graphics")
display = graphics.Graphics()
log.info("Initialising main loop")
game = game.Main(display)


log.info("Starting game")
game()
