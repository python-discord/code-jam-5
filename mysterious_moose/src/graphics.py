import logging
import pygame


# gets logger
log = logging.getLogger("main.graphics")
log.setLevel(logging.INFO)
log.info("graphics logging initialised")


class Graphics:

    def __init__(self):

        pygame_initialisation = pygame.init()

        if pygame_initialisation == (8, 0):
            log.info("PyGame Initialised")
        else:
            log.critical(
                "PyGame did not start correctly, attempting to continue as it could be fine?"
            )

        log.info("creating display object")
        self.display = pygame.display.set_mode((1900, 1000))

        # in this section the file path and file name are separated to make it easier to read
        log.info("loading fonts")
        self.fonts = {"main": pygame.font.Font("assets/fonts/" + "Roboto-Regular.ttf")}

        log.info("loading images")
        self.images = {"example": pygame.image.load("assets/images/" + "example.jpg")}

    def update(self, to_render: list) -> None:
        """ to_render is a list of elements to render in order"""
        for obj in to_render:
            log.debug("rendering: " + str(obj))
            for element in obj:
                if element["type"] == "image":
                    self.display.blit(self.images[element["image"]], element["x"], element["y"])
                elif element["type"] == "box":
                    colour = element["colour"]
                    rect = (element["x"], element["y"], element["dx"], element["dy"])
                    if "edge_width" in element:
                        pygame.draw.rect(self.lcd, colour, rect, element["edge_width"])
                    else:
                        self.display.fill(colour, rect)

                elif element["type"] == "text":
                    log.debug("rendering text as follows: " + str(element))

                    colour = element["colour"] if "colour" in element else None
                    log.debug("fg_colour: " + str(colour))
                    bg_colour = element["bg"] if "bg" in element else None
                    style = element["style"] if "style" in element else None
                    rotation = element["rotation"] if "rotation" in element else int(0)

                    if element["type"] == "normal":
                        self.fonts[element["font"]].render_to(
                            self.display,
                            (element["x"], element["y"]),
                            element["text"],
                            style=style,
                            fgcolor=colour,
                            bgcolor=bg_colour,
                            rotation=rotation,
                            size=element["size"]
                        )
        pygame.display.update()
