import random

score = 0

#set up car object
class car(object):
    electric = False
    image = 'Big bulky car and fumes'
    #How much the score changes by if guessed correctly or incorrectly
    scorechange = 0

    def __init__(self,electric,image,scorechange):
        self.electric = electric
        self.image = image
        self.scorechange = scorechange
        
    #Method to ask user to smash the car
    def smash(self):
        while True:
            answer = input('Is this car electric? (y/n): ')
            print('\n')
            if answer.lower() == 'n':
                return True
            elif answer.lower() == 'y':
                return False
            else:
                print('Please respond with y or n.\n')
                
    #Show the car (Someone who can use python graphics please change this)
    def show(self):
        print(self.image)

    #Shows car, asks if electric or not, produces approptiate output
    def evaluate(self):
        global score
        self.show()
        smashed = self.smash()
        if smashed and self.electric:
            print('Oh no! You smashed an electric car!\n')
            cars[self] -= 1
            score-=self.scorechange
        elif smashed and not self.electric:
            print('Well done! You smashed a bad car!\n')
            cars[self] += 1
            score+=self.scorechange
        elif not smashed and self.electric:
            print('Well done! You let an electric car go!\n')
            cars[self] += 1
            score+=self.scorechange
        elif not smashed and not self.electric:
            print('Oh no! You let a bad car go!\n')
            cars[self] -= 1
            score-=self.scorechange

#Cars
car1 = car(False,'Big bulky car and fumes',20)
car2 = car(True,'Silent small green car',10)

#Dictionary of cars. Value allows us to judge how often that car is guessed correctly
cars = {car1:0,car2:0}

carkeys = list(cars.keys())
random.shuffle(carkeys)


mode = input('Modes:\n1: Normal\n2: Endless\nWhat mode do you wish to play?: ')
print('\n')

if mode == '1':
    #Cycles through the cars and asking if electric or not and producing an output
    score = 0
    for i in carkeys:
        i.evaluate()
        print('Your score is: '+str(score)+'\n')

elif mode == '2':
    #Continues to pick random cars until the score is too low (currently until below 0)
    score = 100
    while score>0:
        random.choice(carkeys).evaluate()
        print('Your score is: '+str(score)+'\n')

#Show the cars you guessed best and worst
print('You guessed this car wrong most times:')
min(cars.items(), key=lambda x: x[1])[0].show()

print('You guessed this car right most times:')
max(cars.items(), key=lambda x: x[1])[0].show()
