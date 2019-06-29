import pygame
import utm

pygame.init()


class Game:
    def __init__(self):
        self.width = 1200
        self.height = 600
        self.bg_color = (255, 255, 255)  # Background color
        self.color = (0, 0, 0)
        self.window = pygame.display.set_mode((self.width, self.height))
        self.caption = pygame.display.set_caption('Code jam')
        self.map = pygame.image.load(r'map_objects/earth2.png')
        self.map = pygame.transform.scale(self.map, (self.width, self.height))  # Resize image to fit in window

        # Example latitude and longitude from Australia
        self.lat = -25.274398
        self.lon = 133.775136

        # Transform lat and lon into x and y coordinates with UTM
        self.x_utm = utm.from_latlon(self.lat, self.lon)
        self.y_utm = utm.from_latlon(self.lat, self.lon)

    def run(self):
        run = True
        window = self.window
        clock = pygame.time.Clock()

        # Printing for debugging to see if it's being correctly converted
        print(self.x_utm)
        print(self.y_utm)

        # Need to transform utm to x and y
        while run:
            clock.tick(60)  # Set to 60 fps
            window.fill(self.bg_color)
            window.blit(self.map, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                    pygame.quit()
                    quit()

                pygame.display.update()


game = Game()
game.run()
