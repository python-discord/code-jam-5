import random
score = 0

#set up car object
class car(object):
    electric = False
    image = 'Big bulky car and fumes'

    def __init__(self,electric,image):
        self.electric = electric
        self.image = image
        
    #Method to ask user to smash the car
    def smash(self):
        while True:
            answer = input('Is this car electric? (y/n): ')
            if answer.lower() == 'n':
                return True
            elif answer.lower() == 'y':
                return False
            else:
                print('Please respond with y or n.')
                
    #Show the car (Someone who can use python graphics please change this)
    def show(self):
        print(self.image)

    #Shows car, asks if electric or not, produces approptiate output
    def evaluate(self):
            self.show()
            smashed=self.smash()
            if smashed and self.electric:
                print('Oh no! You smashed an electric car!')
                cars[self]-=1
            elif smashed and not self.electric:
                print('Well done! You smashed a bad car!')
                cars[self]+=1
            elif not smashed and self.electric:
                print('Well done! You let an electric car go!')
                cars[self]+=1
            elif not smashed and not self.electric:
                print('Oh no! You let a bad car go!')
                cars[self]-=1

#Cars
car1=car(False,'Big bulky car and fumes')
car2=car(True,'Silent small green car')

#Dictionary of cars. Value allows us to judge how often that car is guessed correctly
cars={car1:0,car2:0}

carkeys=list(cars.keys())
random.shuffle(carkeys)


mode=input('Modes:\n1: Standard\n2: Infinite\nWhat mode do you wish to play?: ')

if mode=='1':
    #Cycles through the cars and asking if electric or not and producing an output
    for i in carkeys:
        i.evaluate()

elif mode=='2':
    #Continues to pick random cars until the score is too low (currently until below 0)
    while score>=0:
        random.choice(carkeys).evaluate()
