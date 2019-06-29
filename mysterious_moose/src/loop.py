import logging
import pygame
import src.menus as menus
import src.game as game

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
        # menus - when adding anything before check whether it should
        #         be in resolution_dependants as well
        self.main_menu = menus.MainMenu(graphics)
        self.options_menu = menus.Options(graphics)
        self.game_setup_options = menus.GameSetupOptions(graphics)

        # when the window resolution is changed this list is updated
        self.resolution_dependants = (self.main_menu, self.options_menu, self.game_setup_options)

    def _end(self):
        """ handles main loop completion """
        exit(self.exit_code)

    def _state(self):
        """ main code for loop """
        if self.state == 1:
            # main menu
            mouse_events = self.main_menu.display()

            # events:
            # "play" - transition to game setup state
            # "options" - transition to options state

            for event in mouse_events:
                if event == "play":
                    log.info("Transitioning to Game Setup")
                    self.state = 3
                elif event == "options":
                    log.info("Transitioning to Options")
                    self.state = 2

        elif self.state == 2:
            # options
            mouse_events = self.options_menu.display()

            # events: - (there are currently no events)

            for event in mouse_events:
                pass

        elif self.state == 3:
            # game setup
            mouse_events = self.game_setup_options.display()

            # events: - (there are currently no events)

            for event in mouse_events:
                if event == "play":
                    log.info("Starting Game!")
                    # initialise game
                    self.game = game.Game()
                    # transition to game state
                    self.state = 4

        elif self.state == 4:
            # game running
            self.game.update()

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
                    for to_update in self.resolution_dependants:
                        to_update.resolution_change()

            # execute state dependant code
            self._state()

        self._end()

    def __call__(self):
        """ starts the loop, this is Pythonic right? """
        self._repeat()
