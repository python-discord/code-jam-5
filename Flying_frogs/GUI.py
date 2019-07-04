import pygame
pygame.init()

win = pygame.display.set_mode((922,675))
pygame.display.set_caption('Climate Change Project')


x = 922
y = 200
width = 256
height = 256
vel = 5
hitbox = (x, y, width, height)
move = [pygame.image.load('1.png'), pygame.image.load('2.png'), pygame.image.load('3.png'), pygame.image.load('2.png')]
bg = pygame.image.load('Background.png')

movecount = 0

def redraw():
    global movecount
    win.blit(bg, (0,0))
    if movecount + 1 >= 40:
        movecount = 0   
    win.blit(move[movecount//10], (x,y))
    pygame.draw.rect(win,(225,0,0),hitbox,2)
    movecount += 1    
    pygame.display.update()
    

#main loop
run = True
while run:
    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseposition = pygame.mouse.get_pos()
            if  mouseposition:
                print('Boom!')
    x-=vel
    hitbox = (x, y, width, height)
    redraw()

pygame.quit()
