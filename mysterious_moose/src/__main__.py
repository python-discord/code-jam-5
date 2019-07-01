import logging
import src.loop as loop
import src.graphics as graphics


# logging
log = logging.getLogger("main")
log.info("initialising logging")
log.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter(
    fmt='%(asctime)s - %(name)s - %(levelname)s : %(message)s',
    datefmt='%H:%M:%S'))
log.addHandler(stream_handler)
log.info("Logging initialised")


log.info("Initialising graphics")
display = graphics.Graphics()
log.info("Initialising main loop")
loop = loop.Main(display)


log.info("Starting game")
loop()
