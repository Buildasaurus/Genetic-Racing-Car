import math
import random
import pygame

'''
import cProfile, pstats, io
from pstats import SortKey
pr = cProfile.Profile()
pr.enable()'''

pygame.init()
width = 600
height = 500

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
    magnitude = 100
    angle = 60
    sensorcount = 3

    def __init__(self):
        self.sensorSignals = [0 for i in range(math.floor(-(self.sensorcount-1)/2), math.ceil(self.sensorcount/2))]

    def updateSensorSignals(self, position, velocity): #velocity being the speed vector of the car
        x = position[0]
        y = position[1]
        for i in range(math.floor(-(self.sensorcount-1)/2), math.ceil(self.sensorcount/2)):
            rotatedVelocity = velocity.rotate(2*i/(self.sensorcount)*self.angle)
            try:
                sensorXY = (int(x + rotatedVelocity[0]*self.magnitude), int(y + rotatedVelocity[1]*self.magnitude))
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
        self.position = pygame.Vector2(60.0, 60.0)
        self.velocity = pygame.Vector2(0.0, 0.5)
        self.network = NeuralNetwork()
        self.sensor = Sensors()

    def getNewPlacement(self):
        #update sensors
        self.sensor.updateSensorSignals(self.position, self.velocity)
        #give the sensors values as input
        output = self.network.getOutput(self.sensor.sensorSignals)
        degree = output[0]
        speed = output[1]
        self.rotateCar(degree)
        self.position += self.velocity
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
        




carsystem = Carsystem(10)
background = pygame.image.load("track.png")

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
        pygame.draw.rect(window, pygame.Color("blue"), car.getNewPlacement())
    clock.tick(60)

    if i%60 == 0:
        print(clock.get_fps())
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