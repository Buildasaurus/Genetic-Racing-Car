import random
import pygame
pygame.init()
width = 900
height = 400

window = pygame.display.set_mode((width,height))
running = True
import numpy as np
from math import cos, sin


class NeuralNetwork:
    weights = []
    biases = []
    def __init__(self, varians):
        for i in range(8):
            self.weights.append(random.randint(-varians,varians))
        for i in range(3):
            self.weights.append(random.randint(-varians,varians))
    
    def getOutput(self, input): #input is input neurons.
        #hidden layer
        nueron0 = self.weights[0]*input[0]+ self.weights[1]*input[1] + self.weights[2]*input[2] + self.biases[0]
        neuron1 = self.weights[3]*input[0]+ self.weights[4]*input[1] + self.weights[5]*input[2] + self.biases[1]
        
        return nueron0*self.weights[6] + neuron1*self.weights[7] + self.biases[2]

class Car: #a single car, which also creates a neural network of its own, and senors of its own
    size = (100,100)
    network = NeuralNetwork(1)
    def __init__(self):
        self.position = np.array([float(random.randint(100,width-100)), float(random.randint(100,height-100))])
        self.velocity = np.array([0.1, 0.1])

    def getNewPlacement(self):
        self.position += self.velocity
        return pygame.Rect(car.position[0], car.position[1], car.size[0], car.size[1])

    def rotate(self, degree):

        radians = np.deg2rad(degree)
        x = self.velocity[0]
        y = self.velocity[1]

        self.velocity[0] =  x * cos(radians) + y * sin(radians)
        self.velocity[1] = -x * sin(radians) + y * cos(radians)


class Sensors: #Sensors for each car
    magnitude = 2

class Carsystem: #all cars combined
    car = []
    def __init__(self, systemSize):
        self.car = [Car() for i in range(systemSize)]


        





car = Car()
print(car.velocity)

carsystem = Carsystem(100)
print(carsystem.car)


while running:
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
           running = False
    # set background color to our window
    window.fill(pygame.Color("red"))
    
    car.rotate(0.1)
    pygame.draw.rect(window, pygame.Color("blue"), car.getNewPlacement())
    pygame.draw.line(window, pygame.Color("white"), car.position, car.position+1000*car.velocity)

    # Update our window
    pygame.display.flip()