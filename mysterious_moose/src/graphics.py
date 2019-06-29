import logging
import pygame
import pygame.freetype

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
        self.display = pygame.display.set_mode((1900, 960), pygame.RESIZABLE)

        # in this section the file path and file name are separated to make it easier to read
        log.info("loading fonts")
        self.fonts = {"main": pygame.freetype.Font("assets/fonts/" + "Roboto-Regular.ttf", 20)}

        log.info("loading images")
        self.images = {"example": pygame.image.load("assets/images/" + "example.jpg")}

    def update(self, to_render: list) -> None:
        """ to_render is a list of elements to render in order"""
        for obj in to_render:
            log.debug("rendering: " + str(obj))
            for element in obj:
                if element["type"] == "image":
                    # draws a loaded image onto the display
                    self.display.blit(self.images[element["image"]], element["dest"])

                elif element["type"] == "rect":
                    if "edge_width" in element:
                        pygame.draw.rect(
                            self.display,
                            element["colour"],
                            element["rect"],
                            element["edge_width"]
                        )
                    else:
                        # fill is used over .draw.rect as it can be faster
                        self.display.fill(element["colour"], element["rect"])

                elif element["type"] == "surface":
                    # draw a surface onto the display
                    self.display.blit(element["surface"], element["dest"])

                elif element["type"] == "bg":
                    # fill the entire display with a colour
                    self.display.fill(element["colour"])
        pygame.display.update()
