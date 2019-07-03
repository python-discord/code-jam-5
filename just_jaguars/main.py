# import statements
import pygame


# configuration
SCREEN_SIZE = (240, 180)
WINDOW_LOGO = None # relative filepath or None
WINDOW_HEADER = 'A bad game :(' # string or None


# initialization
pygame.init()


# loading assets (if possible without screen)


# configuring things with config
if WINDOW_LOGO:
	WINDOW_LOGO = pygame.image.load(WINDOW_LOGO)
	pygame.display.set_icon(WINDOW_LOGO)
else:
	print('Please add a "WINDOW_LOGO"')

if WINDOW_HEADER:
	pygame.display.set_caption(WINDOW_HEADER)
else:
	print('Please add a "WINDOW_HEADER"')


# event handlers


# screen initialization
screen = pygame.display.set_mode(SCREEN_SIZE)


# event handler loop
running = True

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: # allow user to quit
			running = False
