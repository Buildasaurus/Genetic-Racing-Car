import math
import random
from tkinter import font
import pygame
import time

'''import cProfile, pstats, io
from pstats import SortKey
pr = cProfile.Profile()
pr.enable()'''

print("Loading...")
pygame.init()
width = 1280
height = 720
gamespeed = 4
window = pygame.display.set_mode((width,height))
running = True
import numpy as np
from math import pi

sizess = [3,3,2]


class NeuralNetwork:
    sizes = [3, 3, 2]
    def __init__(self, WB = None):
        self.weights = [np.random.randn(y, x) for x, y in zip(self.sizes[:-1], self.sizes[1:])]
        self.biases = [np.random.randn(y, 1) for y in self.sizes[1:]]
        i = 0
        if WB:
            self.weights = WB[0]
            self.biases = WB[1]
        else:
            for bias in self.biases:
                self.biases[i] = np.concatenate([np.array(j) for j in bias])
                i += 1

    def getOutput(self, a): #input is input neurons.
        for b, w in zip(self.biases, self.weights):
            a = np.dot(w, a) + b
        return a


class Sensors(): #Sensors for each car
    magnitude = 400
    angle = 60
    sensorcount = 3

    def __init__(self):
        self.sensorSignals = [0 for i in range(math.floor(-(self.sensorcount-1)/2), math.ceil(self.sensorcount/2))]

    def updateSensorSignals(self, position, velocity):
        for i in range(math.floor(-(self.sensorcount-1)/2), math.ceil(self.sensorcount/2)): # for each sensor
            # find the vector of the specific vector
            rotatedVelocity = velocity.rotate(2*i/(self.sensorcount)*self.angle)
            self.sensorSignals[i] = 1 # set to 1 as standard, which it also will be if no white is within 100 pixels
            try: # loop through all 100 pixels until a white one is found, if none is found, set value to 1. value is 0 if it right on top of car
                j = 1
                while j < self.magnitude:
                    sensorXY = rotatedVelocity.normalize()*j + position
                    sensorXY = (int(sensorXY.x), int(sensorXY.y))
                    intpos = (int(position.x), int(position.y))
                    a = pygame.Surface.get_at(window, sensorXY)
                    if a == pygame.Color("white"):
                        #pygame.draw.line(window, (155, 155, 155, 255), intpos, sensorXY)
                        self.sensorSignals[i] = 5*j/self.magnitude
                        break
                    j *= 2
            except:
                pass
                


class Car: 
    '''a single car, which also creates a neural network of its own, and senors of its own'''
    size = (1,1)
    checkPointColors =  [(0, 255, 0, 255), (0, 0, 255, 255), (255, 0, 0, 255), (255, 0, 255, 255),  (0, 255, 255, 255)]

    def __init__(self, spawnPoint, startDirection, WB = None):
        self.position = spawnPoint.copy()
        self.velocity = startDirection.copy()
        self.sensor = Sensors()
        self.laps = 0
        self.color = "red"

        if WB:
            self.network = NeuralNetwork(WB)
        else:
            self.network = NeuralNetwork()


    def updatePlacement(self):
        #update sensors
        self.sensor.updateSensorSignals(self.position, self.velocity)

        #give the sensors values as input
        output = self.network.getOutput(self.sensor.sensorSignals)
        degree = output[0] * gamespeed
        speed = sigmoid(output[1])*gamespeed + 0.00001

        #punish cars on white - and count laps
        try:
            surfaceColor = pygame.Surface.get_at(window, (int(self.position.x), int(self.position.y)))
            if surfaceColor == pygame.Color("white"): #slow down cars on white
                speed *= 0.1 
                self.color = "blue"
            elif surfaceColor == self.checkPointColors[(self.laps + 1)%5]: #update fitness - if crossed new checkpoint
                self.laps += 1
                global bestCar
                if self.laps > bestCar.laps:
                    self.highestFitness = self.laps
                    bestCar.color = "red"
                    self.color = "gold"
                    bestCar = self
            elif self.color == "blue": #if just normal car that should be red
                self.color = "red"

        except:
            speed = 0.0001

        #updaet the placement of the car.
        self.rotateCar(degree)
        self.velocity.scale_to_length(speed)
        self.position += self.velocity
        
    def getPlacement(self):
        if self.color == "gold":
            img_center = self.position - track.carSize
        else:
            img_center = self.position - tuple(q/2 for q in track.carSize)
        return img_center

    def rotateCar(self, angle):
        self.velocity = self.velocity.rotate(angle)


class Carsystem: #all cars combined
    def __init__(self, spawnPoint, startDirection, systemSize, parents = None): #parents is a list of cars and fitness in tuples
        self.cars = []
        if parents:
            for i in range (systemSize):
                weights = []
                biases = []
                #mixed weights
                for j in range(len(sizess)-1):
                    ting = mixedList(np.concatenate(parents[0].network.weights[j]), np.concatenate(parents[1].network.weights[j]))
                    ting = np.reshape(ting, parents[1].network.weights[j].shape)
                    weights.append(ting)
                #mixed biases
                for j in range(len(sizess)-1):
                    ting = mixedList(parents[0].network.biases[j], parents[1].network.biases[j])
                    ting = np.reshape(ting, parents[1].network.biases[j].shape)
                    biases.append(ting)                
                self.cars.append(Car(spawnPoint,startDirection, WB = (weights,biases)))
        else:
            self.cars = [Car(spawnPoint, startDirection) for i in range(systemSize)]
            
class Player:
    checkPointColors =  [(0, 255, 0, 255), (0, 0, 255, 255), (255, 0, 0, 255), (255, 0, 255, 255),  (0, 255, 255, 255)]
    def __init__(self, spawnPoint, startDirection):
        self.position = spawnPoint.copy()
        self.velocity = startDirection.copy()
        self.laps = 0
        self.won = False

    def updatePlacement(self, speed, angle):
        self.velocity = self.velocity.rotate(angle)
        self.position += self.velocity
        surfaceColor = pygame.Surface.get_at(window, (int(self.position.x), int(self.position.y)))
        if surfaceColor == pygame.Color("white"): #slow down cars on white
            speed *= 0.1 
            self.color = "blue"
        elif surfaceColor == self.checkPointColors[(self.laps + 1)%5]: #update fitness - if crossed new checkpoint
            self.laps += 1
            if self.laps == 6:
                self.won = True

        self.velocity.scale_to_length(speed + 0.00001)


    def getPlacement(self):
        img_center = self.position - track.carSize
        return img_center

class trackManager:
    def __init__(self):
        self.setLevel("jLevel")
        self.carSize = (15,8)
        self.redCar = pygame.transform.scale(pygame.image.load("../data/Racerbil Rød.png"), self.carSize)
        self.goldCar = pygame.transform.scale(pygame.image.load("../data/Racerbil Guld.png"), tuple(q*2 for q in self.carSize))
        self.blueCar = pygame.transform.scale(pygame.image.load("../data/Racerbil blå.png"), self.carSize)
        self.systemSize = 80

    def setLevel(self, level): #returns new spawnpoints, images etc.
        if level == "jLevel":
            self.spawnPoint = pygame.Vector2(535.0, 500.0)
            self.startDirection = pygame.Vector2(0, -1)
            self.background = pygame.image.load("../data/Background - J level.png")
            #self.foreground=self.background
            self.foreground = pygame.image.load("../data/Foreground - J level.png")
        if level == "catLevel": 
            self.spawnPoint = pygame.Vector2(400, 100.0) # find new spawnpoint
            self.background = pygame.image.load("../data/Background - Cat level.png")
            #self.foreground=self.background
            self.foreground = pygame.image.load("../data/Foreground - Cat level.png")
            self.startDirection = pygame.Vector2(-1, 0.2)
            
####Functions####
def sigmoid(z):
    return 1.0/(1.0+np.exp(-z))
        
def mixedList(a, b):
    nyList = []
    for i in range (len(a)):
        rand = random.randint(1,2)
        if rand == 1:
            nyList.append(a[i] + np.random.normal(0,0.3))
        else:
            nyList.append(b[i] + np.random.normal(0,0.3))
    return nyList

def updateCarPlacemenet():
    for car in carsystem.cars:
        car.updatePlacement()
    #player car
    playerSpeed = 0
    playerAngle = 0
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        playerAngle -= gamespeed
    if keys[pygame.K_RIGHT]:
        playerAngle += gamespeed
    if keys[pygame.K_UP]:
        playerSpeed = gamespeed
    player.updatePlacement(playerSpeed, playerAngle)

def displayCars():
    a = pygame.Vector2(1, 0)
    for car in carsystem.cars:
        ang = -a.angle_to(car.velocity)
        if car.color == "red":
            rotatedCar = pygame.transform.rotate(track.redCar, ang)
        elif car.color == "blue":
            rotatedCar = pygame.transform.rotate(track.blueCar, ang)
        else:
            rotatedCar = pygame.transform.rotate(track.goldCar, ang)
        window.blit(rotatedCar, car.getPlacement())
    
    #display player
    ang = -a.angle_to(player.velocity)
    playerCar = pygame.transform.rotate(track.goldCar, ang)
    window.blit(playerCar, player.getPlacement())

def printInfo():
    print(clock.get_fps())
    maxfitness = 0
    secondbestFitness = 0
    for car in carsystem.cars:
        if car.laps > maxfitness:
            secondbestFitness = maxfitness
            maxfitness = car.laps
        elif car.laps > secondbestFitness:
            secondbestFitness = car.laps
    print(maxfitness, secondbestFitness)

def createNewGeneration(carsystem): #takes old generation as input
    maxfitness = (0,0) #(fitness, index)
    secondbestFitness = (0,0)
    j = 0
    for car in carsystem.cars:
        if car.laps > maxfitness[0]:
            secondbestFitness = maxfitness
            maxfitness = (car.laps, j)
        elif car.laps > secondbestFitness[0]:
            secondbestFitness = (car.laps, j)
        j += 1
    parents=(carsystem.cars[maxfitness[1]], carsystem.cars[secondbestFitness[1]])
    carsystem = []
    carsystem = Carsystem(track.spawnPoint, track.startDirection, track.systemSize, parents=parents)
    bestCar = carsystem.cars[0]
    player = Player(track.spawnPoint, track.startDirection)
    return carsystem, bestCar, player

def displayInfo():
    window.blit(track.foreground, (0,0))
    
    #Generation counter
    text = font.render('Generation: ' + str(generation), True, (255,255,255,255))
    window.blit(text, (width-400, 20))

    #Player score
    text = font.render('Your Score: ' + str(player.laps), True, (255,255,255,255))
    window.blit(text, (width-200, 20))

def refreshWindow():
    window.fill(pygame.Color("white"))
    window.blit(track.background, (0,0))

def newLevelScreen():
    #countDown
    for i in range(3,0,-1):
        refreshWindow()
        displayInfo()
        displayCars()
        text = largeLetters.render(str(i), True, (255,255,255,255))
        window.blit(text, (width/2, height/2))
        pygame.display.flip()
        time.sleep(1)
    
def winnerScreen():
    #count placement
    place = 1
    for car in carsystem.cars:
        if car.laps >= 6:
            place += 1
    text = largeLetters.render("You placed: " + str(place), True, (255,255,255,255))
    window.blit(text, (width/2-text.get_width()/2, height/2-text.get_height()/2))
    pygame.display.flip()
    time.sleep(2)
    

#Car Creation
track = trackManager()
carsystem = Carsystem(track.spawnPoint, track.startDirection, track.systemSize)   
bestCar = carsystem.cars[0]
player = Player(track.spawnPoint, track.startDirection)

#timing and generation
clock = pygame.time.Clock()
generation = 0
largeLetters = font = pygame.font.SysFont(None, 100)
font = pygame.font.SysFont(None, 24)
i = 0
newLevelScreen()
while running:
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
           running = False

    # set background color to our window
    refreshWindow()
    
    #update all cars placement
    updateCarPlacemenet()

    #print foreground and relevant text at top left
    displayInfo()

    #display all cars
    displayCars()  

    #print best car and fps
    if i%60 == 0:
        printInfo()

    # find new generation - reset level
    if player.won:
        winnerScreen()
        if generation == 1:
            track.setLevel("catLevel")
        carsystem, bestCar, player = createNewGeneration(carsystem)
        newLevelScreen()
        generation += 1
    
    #update framecounter
    i += 1


    # Update our window
    clock.tick(60)    
    pygame.display.flip()


# ... do something ...

'''pr.disable()
s = io.StringIO()
sortby = SortKey.CUMULATIVE
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print(s.getvalue())'''