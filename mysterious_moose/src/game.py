import logging
import pygame
import src.menus as menus

log = logging.getLogger("main.game")
log.setLevel(logging.INFO)
log.info("game loop logger initialised")


class Main:
    def __init__(self, graphics):
        """ initialises the program main loop """
        log.info("main loop initialising")
        self.state = 1
        self.exit_code = -1
        self.graphics = graphics
        self.main_menu = menus.MainMenu(graphics)
        self.options_menu = menus.Options(graphics)
        # when the window resolution is changed this list is updated
        self.resolution_dependants = (self.main_menu, self.options_menu)

    def _end(self):
        """ handles main loop completion """
        exit(self.exit_code)

    def _state(self):
        """ main code for loop """
        if self.state == 1:
            # main menu
            self.main_menu.display(self.events)
        elif self.state == 2:
            # options
            self.options_menu.display(self.events)
        elif self.state == 3:
            # game setup
            pass
        elif self.state == 4:
            # game running
            pass

    def _repeat(self):
        """ main loop """
        while self.exit_code == -1:
            # executed every loop
            pygame.event.pump()  # execute pygame background tasks
            self.events = pygame.event.get()
            log.debug("events: " + str(self.events))
            for event in self.events:
                if event.type == pygame.QUIT:
                    log.info("Quit event received")
                    self.exit_code = 0
                elif event.type == pygame.VIDEORESIZE:
                    pygame.display.set_mode((
                        800 if event.w < 800 else event.w,
                        600 if event.h < 600 else event.h
                    ), pygame.RESIZABLE)

            # execute state dependant code
            self._state()

        self._end()

    def __call__(self):
        """ starts the loop, this is Pythonic right? """
        self._repeat()
