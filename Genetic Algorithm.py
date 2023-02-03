import math
import random
import pygame
pygame.init()
width = 900
height = 400

window = pygame.display.set_mode((width,height))
running = True
import numpy as np
from math import cos, sin, pi


class NeuralNetwork:
    weights = []
    biases = []
    sizes = []
    def __init__(self):
        self.sizes = [3, 3, 1]
        self.weights = [np.random.randn(y, x) for x, y in zip(self.sizes[:-1], self.sizes[1:])]
        self.biases = [np.random.randn(y, 1) for y in self.sizes[1:]]

    def getOutput(self, a): #input is input neurons.
        for b, w in zip(self.biases, self.weights):
            a = sigmoid(np.dot(w, a) + np.concatenate([np.array(i) for i in b]))
        return a - 0.5

    



class Sensors(): #Sensors for each car
    magnitude = 100
    angle = 45
    sensorcount = 3
    sensorSignals = [0 for i in range(math.floor(-(sensorcount-1)/2), math.ceil(sensorcount/2))]

    def __init__(self):
        pass
    

    def updateSensorSignals(self, position, velocity): #velocity being the speed vector of the car
        x = position[0]
        y = position[1]
        for i in range(math.floor(-(self.sensorcount-1)/2), math.ceil(self.sensorcount/2)):
            rotatedVelocity = rotate(velocity, 2*i/(self.sensorcount)*self.angle)
            try:
                a = pygame.Surface.get_at(window, (int(x + rotatedVelocity[0]*self.magnitude), int(y + rotatedVelocity[1]*self.magnitude)))
                pygame.Surface.set_at(window, (int(x + rotatedVelocity[0]*self.magnitude), int(y + rotatedVelocity[1]*self.magnitude)), pygame.Color("blue"))

                if a ==  pygame.Color("white"):
                    self.sensorSignals[i] = 0
                else:
                    self.sensorSignals[i] = 1

            except:
                self.sensorSignals[i] = 1
                
    

class Car: #a single car, which also creates a neural network of its own, and senors of its own
    size = (10,10)
    position = []
    velocity = []
    sensor = Sensors()

    def __init__(self):
        self.position = np.array([60.0, 60.0])
        self.velocity = np.array([0.1, 0.1])
        self.network = NeuralNetwork()

    def getNewPlacement(self):
        #update sensors
        self.sensor.updateSensorSignals(self.position, self.velocity)
        #give the sensors values as input
        degree = self.network.getOutput(self.sensor.sensorSignals)
        self.rotateCar(degree)
        self.position += self.velocity
        return pygame.Rect(car.position[0], car.position[1], car.size[0], car.size[1])
        
    def rotateCar(self, angle):
        self.velocity[0], self.velocity[1] = rotate(self.velocity, angle)


class Carsystem: #all cars combined
    car = []
    def __init__(self, systemSize):
        self.car = [Car() for i in range(systemSize)]

#Functions
def sigmoid(z):
    return 1.0/(1.0+np.exp(-z))
        
def rotate(vector, degree):
    radians = np.deg2rad(degree)
    x = vector[0]
    y = vector[1]
    return np.array([x * cos(radians) + y * sin(radians), -x * sin(radians) + y * cos(radians)])





carsystem = Carsystem(100)
background = pygame.image.load("track.png")

while running:
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
           running = False
    # set background color to our window
    window.fill(pygame.Color("white"))
    window.blit(background, (0,0))
    
    for car in carsystem.car:
        pygame.draw.rect(window, pygame.Color("blue"), car.getNewPlacement())
        pygame.draw.line(window, pygame.Color("white"), car.position, car.position+100*car.velocity)

    # Update our window
    pygame.display.flip()