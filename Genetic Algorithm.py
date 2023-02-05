import math
import random
import pygame

'''
import cProfile, pstats, io
from pstats import SortKey
pr = cProfile.Profile()
pr.enable()'''

pygame.init()
width = 440
height = 600

window = pygame.display.set_mode((width,height))
running = True
import numpy as np
from math import pi


class NeuralNetwork:
    def __init__(self):
        self.sizes = [3, 3, 2]
        self.weights = [np.random.randn(y, x) for x, y in zip(self.sizes[:-1], self.sizes[1:])]
        self.biases = [np.random.randn(y, 1) for y in self.sizes[1:]]
        i = 0
        for bias in self.biases:
            self.biases[i] = np.concatenate([np.array(j) for j in bias])
            i += 1

    def getOutput(self, a): #input is input neurons.
        for b, w in zip(self.biases, self.weights):
            a = np.dot(w, a) + b
        return a

    



class Sensors(): #Sensors for each car
    magnitude = 20
    angle = 80
    sensorcount = 3

    def __init__(self):
        self.sensorSignals = [0 for i in range(math.floor(-(self.sensorcount-1)/2), math.ceil(self.sensorcount/2))]

    def updateSensorSignals(self, position, velocity): #velocity being the speed vector of the car
        x = position[0]
        y = position[1]
        for i in range(math.floor(-(self.sensorcount-1)/2), math.ceil(self.sensorcount/2)):
            rotatedVelocity = velocity.rotate(2*i/(self.sensorcount)*self.angle)
            try:
                sensorXY = rotatedVelocity.normalize()*self.magnitude + position
                sensorXY = (int(sensorXY.x), int(sensorXY.y))
                a = pygame.Surface.get_at(window, sensorXY)
                pygame.Surface.set_at(window, sensorXY, pygame.Color("blue"))

                
                if a ==  pygame.Color("white"):
                    self.sensorSignals[i] = 0
                else:
                    self.sensorSignals[i] = 1

            except:
                self.sensorSignals[i] = 1
                


class Car: 
    '''a single car, which also creates a neural network of its own, and senors of its own'''
    size = (10,10)

    def __init__(self):
        self.position = pygame.Vector2(195.0, 18.0)
        self.velocity = pygame.Vector2(-0.5, 0)
        self.network = NeuralNetwork()
        self.sensor = Sensors()
        self.laps = 0
        self.lastColor = (69, 115, 197, 255)

    def updatePlacement(self):
        #update sensors
        self.sensor.updateSensorSignals(self.position, self.velocity)

        #update fitness - if crossed new checkpoint


        #give the sensors values as input
        output = self.network.getOutput(self.sensor.sensorSignals)
        degree = output[0] 
        speed = sigmoid(output[1]) + 0.0001

        #punish cars on white - and count laps
        try:
            a = pygame.Surface.get_at(window, (int(self.position.x), int(self.position.y)))
            if a == pygame.Color("white"):
                speed *= 0.1 
            elif a == (1, 177, 81, 255) and self.lastColor != a: #if first time on green
                self.laps += 1
                self.lastColor = a
            elif a == (69, 115, 197, 255) and self.lastColor != a: #if first time on blue
                self.laps += 1
                self.lastColor = a
        except:
            speed = 0.0001




        #return the new placement of the car.
        self.rotateCar(degree)
        self.velocity.scale_to_length(speed)
        self.position += self.velocity
        
    def getPlacement(self):
        return pygame.Rect(car.position[0], car.position[1], car.size[0], car.size[1])


    def rotateCar(self, angle):
        self.velocity = self.velocity.rotate(angle)


class Carsystem: #all cars combined
    car = []
    def __init__(self, systemSize):
        self.car = [Car() for i in range(systemSize)]

#Functions
def sigmoid(z):
    return 1.0/(1.0+np.exp(-z))
        




carsystem = Carsystem(100)
background = pygame.image.load("lilleRacerbaneMedStreger.png")

clock = pygame.time.Clock()  

i = 0
while running:
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
           running = False
    # set background color to our window
    window.fill(pygame.Color("white"))
    window.blit(background, (0,0))


    for car in carsystem.car:
        car.updatePlacement()
    
    for car in carsystem.car:
        pygame.draw.rect(window, pygame.Color("blue"), car.getPlacement())
    clock.tick(60)

    if i%60 == 0:
        print(clock.get_fps())
        maxfitness = 0
        secondbestFitness = 0
        for car in carsystem.car:
            if car.laps > maxfitness:
                secondbestFitness = maxfitness
                maxfitness = car.laps
            elif car.laps > secondbestFitness:
                secondbestFitness = car.laps
        print(maxfitness, secondbestFitness)
        strbuilder = ""
        for car in carsystem.car:
            strbuilder += " " + str(car.laps)
        print(strbuilder)


    i += 1

    # Update our window
    pygame.display.flip()


# ... do something ...
'''
pr.disable()
s = io.StringIO()
sortby = SortKey.CUMULATIVE
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print(s.getvalue())'''