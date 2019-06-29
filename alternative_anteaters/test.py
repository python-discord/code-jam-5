import pygame

pygame.init()

# Setup Game Window
size = width, height = 400, 300
win = pygame.display.set_mode(size)
pygame.display.set_caption("Alternative Anteaters")

x = 50
y = 50
w = 40
h = 60
vel = 5


def redrawGameWindow():

    # Draw game window here
    pygame.draw.rect(win, (0, 255, 0), (x, y, w, h))
    pygame.display.update()


# Main Loop
run = False
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        x -= vel

    if keys[pygame.K_RIGHT]:
        x += vel

    if keys[pygame.K_UP]:
        y -= vel

    if keys[pygame.K_DOWN]:
        y += vel

    redrawGameWindow()

pygame.quit()
