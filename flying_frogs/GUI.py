# Import modules
try:
    import pygame
    import random
except ImportError as err:
    print('Could not import modules. Please check you have got pygame. Error:\n' + str(err))
    quit()

# Initialise pygame
pygame.init()

# Set up window
win = pygame.display.set_mode((922, 675))
pygame.display.set_caption('Climate Change Project')

# Set up background
bg = pygame.image.load('Backgrounds//Background.png')

# Set up cursor
hammer = pygame.image.load('Cursor//hammer.png')

# Define control variables:
# Veichles on screen
onscreen = []
# Player's score
score = 25
# Mistakes the player has made
mistakes = 0
# y coordinates of the three lanes
lanes = [50, 300, 500]
# Set up clock
clock = pygame.time.Clock()
# Set up font for the score
Scorefont = pygame.font.Font('freesansbold.ttf', 32)
# To show if the player has lost or won
lose = False
comp = False
# To show what screen the player is on
introduction = True
rules = False
meaning = False


# Function to redraw the window
def redraw():

    # Introduction screen
    if introduction:
        # Mouse
        pygame.mouse.set_visible(True)
        # Background
        win.blit(pygame.image.load('Backgrounds//Introduction.png'), (0, 0))
        # Buttons
        win.blit(play.image, (play.x, play.y))
        win.blit(rulesbutton.image, (rulesbutton.x, rulesbutton.y))
        win.blit(meaningbutton.image, (meaningbutton.x, meaningbutton.y))

    # Rules screen
    elif rules:
        # Mouse
        pygame.mouse.set_visible(True)
        # Background
        win.blit(pygame.image.load('Backgrounds//Rules.png'), (0, 0))
        # Buttons
        win.blit(back.image, (back.x, back.y))

    elif meaning:
        # Mouse
        pygame.mouse.set_visible(True)
        # Background
        win.blit(pygame.image.load('Backgrounds//Meaning.png'), (0, 0))
        # Buttons
        win.blit(back.image, (back.x, back.y))

    # Game screen
    else:
        # Background
        win.blit(bg, (0, 0))

        # If the player has lost
        if lose:
            # Mouse
            pygame.mouse.set_visible(True)
            # Box
            win.blit(pygame.image.load('Boxes//LoseBox.png'), (276, 161))
            # Buttons
            win.blit(playagain.image, (playagain.x, playagain.y))
            win.blit(back.image, (290, 250))

        # If the player has won
        elif comp:
            # Mouse
            pygame.mouse.set_visible(True)
            # Box
            win.blit(pygame.image.load('Boxes//WinBox.png'), (276, 161))
            # Buttons
            win.blit(playagain.image, (playagain.x, playagain.y))
            win.blit(back.image, (290, 250))

        # If the game is ongoing
        else:
            for item in onscreen:
                # Check which image should be showing and show it
                if item.movecount + 1 >= len(item.move) * 10:
                    item.movecount = 0
                win.blit(item.move[item.movecount // 10], (item.x, item.y))
                item.movecount += 1

            # Hide mouse
            pygame.mouse.set_visible(False)
            (a, b) = pygame.mouse.get_pos()

            win.blit(hammer, (a, b))

        # Display score
        DisplayScore = Scorefont.render(
            'Score: ' + str(score), True, (0, 0, 0))
        ScoreRect = DisplayScore.get_rect()
        ScoreRect.center = (100, 40)
        win.blit(DisplayScore, ScoreRect)

        # Display mistakes
        DisplayMistakes = Scorefont.render(
            'Mistakes: ' + str(mistakes), True, (0, 0, 0))
        MistakesRect = DisplayMistakes.get_rect()
        MistakesRect.center = (822, 40)
        win.blit(DisplayMistakes, MistakesRect)

    # Update display
    pygame.display.update()


# Button class
class button(object):

    # Image to load for the button
    image = ''
    # Dimentions of image
    width = 0
    height = 0
    # Position on screen
    x = 0
    y = 0

    # Initialisation
    def __init__(self, image, width, height, x, y):
        self.image = image
        self.width = width
        self.height = height
        self.x = x
        self.y = y

    # Resets game (not used for all buttons)
    def pressed(self):
        global score
        global onscreen
        global lose
        global comp
        global mistakes
        onscreen = []
        score = 25
        mistakes = 0
        lose = False
        comp = False


# Define buttons
playagain = button(pygame.image.load(
    'Buttons//PlayAgainButton.png'), 200, 106, 365, 330)
back = button(pygame.image.load(
    'Buttons//Back.png'), 100, 82, 20, 150)
play = button(pygame.image.load(
    'Buttons//PlayButton.png'), 200, 106, 365, 200)
rulesbutton = button(pygame.image.load(
    'Buttons//RulesButton.png'), 200, 106, 365, 350)
meaningbutton = button(pygame.image.load(
    'Buttons//MeaningButton.png'), 200, 106, 365, 500)


# Car class
class car(object):

    # Shows if car is electric
    electric = False
    # Start position
    x = 922
    y = random.choice(lanes)
    # Size of image
    width = 256
    height = 256
    # How fast it moves
    vel = 5
    # Hitbox (to be calculated)
    hitbox = ()
    # Images of movement in order
    move = []
    # Keep track of which image to be on
    movecount = 0
    # How much the score changes by when destroyed or let go
    scorechange = 0

    # Initialisation
    def __init__(self, electric, move, vel, width, height, scorechange):
        self.electric = electric
        self.move = move
        self.vel = vel
        self.width = width
        self.height = height
        self.scorechange = scorechange
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.y = random.choice(lanes)

    # Show the car
    def show(self):
        onscreen.append(self)

    # What happens when destroyed
    def hit(self):
        global score
        global mistakes
        # Reset x and y values
        self.y = random.choice(lanes)
        self.x = 922
        # Change score appropriate to being electric or not
        if self.electric:
            score -= self.scorechange
            mistakes += 1
        elif not self.electric:
            score += self.scorechange
        # Remove itself from veiw
        onscreen.remove(self)

    # What happens when let go
    def letgo(self):
        global score
        global mistakes
        # Reset x and y values
        self.y = random.choice(lanes)
        self.x = 922
        # Change score appropriate to being electric or not
        if self.electric:
            score += self.scorechange
        elif not self.electric:
            score -= self.scorechange
            mistakes += 1
        # Remove itself from veiw
        onscreen.remove(self)


# Define cars (E stands for electric and F for fossil)
E1 = car(True,
         [pygame.image.load('Cars\\Electric.png')],
         5,
         168,
         92,
         3)

E2 = car(True,
         [pygame.image.load('Cars\\Taxi.png')],
         7,
         168,
         68,
         3)

F1 = car(False,
         [pygame.image.load('Cars\\Blackcar.png')],
         5,
         168,
         94,
         5)

F2 = car(False,
         [pygame.image.load('Cars\\Jeep.png')],
         10,
         168,
         72,
         5)


# List of available vehicles to chose from
vehicles = [E1, E2, F1, F2]


# To show if the game is running
run = True

# Main loop
while run:
    # Control the frame rate by ticking the clock
    clock.tick(50)

    # Respond to events
    for event in pygame.event.get():
        # Quit when closed
        if event.type == pygame.QUIT:
            run = False
        # Respond to mouse click
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get mouse position
            (a, b) = pygame.mouse.get_pos()
            # Check if car has been hit
            for i in onscreen:
                if b < i.hitbox[1] + \
                        i.hitbox[3] and b > i.hitbox[1] \
                        and a > i.hitbox[0] and a < i.hitbox[0] + i.hitbox[2]:
                    i.hit()

            # Check if button has been clicked
            # On introducton screen
            if introduction:
                # Check if mouse coordinates match the button/car's
                if b < play.y + play.height and b > play.y \
                        and a > play.x and a < play.x + play.width:
                    # Start game
                    playagain.pressed()
                    introduction = False
                    rules = False
                    meaning = False
                elif b < rulesbutton.y + rulesbutton.height \
                        and b > rulesbutton.y and a > rulesbutton.x \
                        and a < rulesbutton.x + rulesbutton.width:
                    # Display rules screen
                    introduction = False
                    rules = True
                    meaning = False
                if b < meaningbutton.y + meaningbutton.height \
                        and b > meaningbutton.y and a > meaningbutton.x \
                        and a < meaningbutton.x + meaningbutton.width:
                    # Display meaning screen
                    introduction = False
                    rules = False
                    meaning = True

            # On rules screen
            if rules:
                if back.y + back.height and b > back.y and a > back.x and a < back.x + back.width:
                    # Display introduction screen
                    rules = False
                    introduction = True
                    meaning = False

            if meaning:
                if back.y + back.height and b > back.y and a > back.x and a < back.x + back.width:
                    # Display introduction screen
                    rules = False
                    introduction = True
                    meaning = False

            # If the player has won or lost
            elif lose or comp:
                if b < playagain.y + \
                        playagain.height and b > playagain.y \
                        and a > playagain.x and a < playagain.x + playagain.width:
                    # Restart game
                    playagain.pressed()
                if b < 250 + back.height and b > 250 and a > 290 and a < 290 + back.width:
                    # Show introduction screen
                    introduction = True
                    rules = False

    # Add a random new car at intervals
    if pygame.time.get_ticks() % 75 == 0:
        random.choice(vehicles).show()

    # Move cars their assigned  distance
    for car in onscreen:
        car.x -= car.vel
        # Move their hitbox with them
        car.hitbox = (car.x, car.y, car.width, car.height)
        # Remove them and change score if moved offscreen
        if car.x < 0 - car.width:
            car.letgo()

    # Check for collisions
    for car in onscreen:
        # car is the car coming up behind
        for testcar in onscreen:
            # testcar is the car that might be ahead
            if not car == testcar:
                if car.y == testcar.y and car.x < testcar.x + testcar.width and car.x > testcar.x:
                    # car will travel directly behind testcar
                    car.x = testcar.x + testcar.width

    # Clear screen and lose if score is below 0
    if score < 0:
        lose = True
        onscreen = []

    # Clear screen and win if score is above 100
    if score >= 50:
        onscreen = []
        comp = True

    # Redraw window
    redraw()

# Quit if loop ends
pygame.quit()
