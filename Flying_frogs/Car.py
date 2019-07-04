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
    #Show the car
    def show(self):
        print(self.image)

car1=car(False,'Big bulky car and fumes')
car2=car(True,'Silent small green car')

#Dictionary of cars. Value allows us to judge how often that car is guessed correctly
cars={car1:0,car2:0}

carkeys=list(cars.keys())
random.shuffle(carkeys)

#Cycles through the cars and asking if electric or not and producing an output
for i in carkeys:
    i.show()
    smashed=i.smash()
    if smashed and i.electric:
        print('Oh no! You smashed an electric car!')
        cars[i]-=1
    elif smashed and not i.electric:
        print('Well done! You smashed a bad car!')
        cars[i]+=1
    elif not smashed and i.electric:
        print('Well done! You let an electric car go!')
        cars[i]+=1
    elif not smashed and not i.electric:
        print('Oh no! You let a bad car go!')
        cars[i]-=1
