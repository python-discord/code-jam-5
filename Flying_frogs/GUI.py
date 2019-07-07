'''
To do:
-Tell user to install pygame
-Comment code
-Make cars
-Change rules to be clearer on how to destroy a car
-Find out how to and submit work
'''


try:
    import pygame
    import random
except ImportError:
    print('Could not import modules. Please check your connection and try again later.')
    quit()

pygame.init()

win = pygame.display.set_mode((922, 675))
pygame.display.set_caption('Climate Change Project')

bg = pygame.image.load('Backgrounds//Background.png')

onscreen = []
score = 0
lanes = [50, 300, 500]
clock = pygame.time.Clock()
Scorefont = pygame.font.Font('freesansbold.ttf', 32)
lose = False
comp = False
introduction = True


def redraw():
    if introduction:
        win.blit(pygame.image.load('Backgrounds//Introduction.png'), (0, 0))
        win.blit(play.image, (play.x, play.y))
        win.blit(rulesbutton.image, (rulesbutton.x, rulesbutton.y))
    elif rules:
        win.blit(pygame.image.load('Backgrounds//Rules.png'), (0, 0))
        win.blit(back.image, (back.x, back.y))
    else:
        win.blit(bg, (0, 0))

        if lose:
            win.blit(pygame.image.load('LoseBox.png'), (276, 161))
            win.blit(playagain.image, (playagain.x, playagain.y))
            win.blit(back.image, (290, 250))
        elif comp:
            win.blit(pygame.image.load('WinBox.png'), (276, 161))
            win.blit(playagain.image, (playagain.x, playagain.y))
            win.blit(back.image, (290, 250))
        else:
            for item in onscreen:
                if item.movecount + 1 >= len(item.move)*10:
                    item.movecount = 0
                win.blit(item.move[item.movecount//10], (item.x, item.y))
                item.movecount += 1

        DisplayScore = Scorefont.render('Score: '+str(score), True, (0, 0, 0))
        ScoreRect = DisplayScore.get_rect()
        ScoreRect.center = (100, 40)
        win.blit(DisplayScore, ScoreRect)

    pygame.display.update()


class button(object):
    image = ''
    width = 0
    height = 0
    x = 0
    y = 0

    def __init__(self, image, width, height, x, y):
        self.image = image
        self.width = width
        self.height = height
        self.x = x
        self.y = y

    def pressed(self):
        global score
        global onscreen
        global lose
        global comp
        onscreen = []
        score = 0
        lose = False
        comp = False


playagain = button(pygame.image.load('Buttons//PlayAgainButton.png'), 200, 106, 365, 330)
play = button(pygame.image.load('Buttons//PlayButton.png'), 200, 106, 365, 450)
back = button(pygame.image.load('Buttons//Back.png'), 100, 82, 20, 150)
rulesbutton = button(pygame.image.load('Buttons//RulesButton.png'), 200, 106, 365, 250)


# Set up car object
class car(object):
    # If electric
    electric = False
    # Start position
    x = 922
    y = random.choice(lanes)
    # Size of image
    width = 256
    height = 256
    # How fast it moves
    vel = 5
    hitbox = ()
    # Images of movement
    move = []
    # Images of destruction
    # destroy = []
    movecount = 0
    scorechange = 0

    # How much the score changes by if guessed correctly or incorrectly
    scorechange = 0

    def __init__(self, electric, move, vel, width, height, scorechange):
        self.electric = electric
        self.move = move
        self.vel = vel
        self.width = width
        self.height = height
        self.scorechange = scorechange
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.y = random.choice(lanes)

    def show(self):
        onscreen.append(self)

    # Shows car, asks if electric or not, produces approptiate output
    def hit(self):
        global score
        self.y = random.choice(lanes)
        self.x = 922
        if self.electric:
            score -= self.scorechange
        elif not self.electric:
            score += self.scorechange
        onscreen.remove(self)

    def letgo(self):
        global score
        self.y = random.choice(lanes)
        self.x = 922
        if self.electric:
            score += self.scorechange
        elif not self.electric:
            score -= self.scorechange
        onscreen.remove(self)


# Replace these with actual cars. These are placeholders.
ambulance = car(False, [pygame.image.load('1.png'), pygame.image.load('2.png'), pygame.image.load('3.png'), pygame.image.load('2.png')], 5, 225, 110, 5)
policecar = car(True, [pygame.image.load('P1.png'), pygame.image.load('P2.png'), pygame.image.load('P3.png'), pygame.image.load('P2.png')], 10, 225, 110, 3)

vehicles = [ambulance, policecar]

# Main loop
introduction = True
rules = False
run = True
while run:
    clock.tick(50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            (a, b) = pygame.mouse.get_pos()
            for i in onscreen:
                if b < i.hitbox[1] + i.hitbox[3] and b > i.hitbox[1] and a > i.hitbox[0] and a < i.hitbox[0] + i.hitbox[2]:
                    i.hit()
            if introduction:
                if playagain.y + playagain.height and b > playagain.y and a > playagain.x and a < playagain.x + playagain.width:
                    playagain.pressed()
                    introduction = False
                elif rulesbutton.y + rulesbutton.height and b > rulesbutton.y and a > rulesbutton.x and a < rulesbutton.x + rulesbutton.width:
                    introduction = False
                    rules = True
            if rules:
                if back.y + back.height and b > back.y and a > back.x and a < back.x + back.width:
                    rules = False
                    introduction = True
            elif lose or comp:
                if b < playagain.y + playagain.height and b > playagain.y and a > playagain.x and a < playagain.x + playagain.width:
                    playagain.pressed()
                if b < 250 + back.height and b > 250 and a > 290 and a < 290 + back.width:
                    introduction = True

    if pygame.time.get_ticks() % 100 == 0:
        onscreen.append(random.choice(vehicles))

    for item in onscreen:
        item.x -= item.vel
        item.hitbox = (item.x, item.y, item.width, item.height)
        if item.x < 0-item.width:
            item.letgo()

    if score < 0:
        lose = True
        onscreen = []

    if score >= 100:
        onscreen = []
        comp = True

    redraw()

pygame.quit()
