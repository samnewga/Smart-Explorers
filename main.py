import pygame as pg
import math
import random
from tkinter import *
from tkinter.font import Font

################################################### GUI ###################################################
################################################### GUI ###################################################
# Creates a tkinter window titled 'window' with a white background
window = Tk()
window.title("Final Project")
window.configure(background="black")

# Breaks the tkinter window into a top frame and bottom frame
topFrame = LabelFrame(window, background='black')
topFrame.pack()
bottomFrame = Frame(window, background='black')
bottomFrame.pack(side=BOTTOM)

buttonFont = Font(family="Arial Black", size=8)
textFont= Font(family="Arial Black", size=12)

# Text with program name information
name_text =("Project Name: Smart Exploration" \
            "\nBy: Samael Newgate" \
            "\nClass: CSC438 - Algorithms, Frameworks and Design Patterns - FA19212" \
            "\nAssignment: Final Project")


# Text with program description text
description_text = "Inspiration:" \
                   "\nThe idea for this project came from  a Genetic Algorithm called Smart Rockets." \
                   "\n\nDescription: " \
                   "\nUsing PyGame to show a visual representation of math equations and random" \
                   "\nactivities  to navigate through a course with obstacles in order to get to the final" \
                   "\ndestination.The A.I. learns to navigate through the course using a DNA like" \
                   "\nstoring/reproducing method. A failed attempt will be forgotten, while a attempt" \
                   "\nthat was either successful or closer to the goal  will be" \
                   "\nstored in the gene pool. The gene pool will allow for pairing/reproduction." \
                   "\nThis gene pool prioritizes the most successful attempts for the pairing process." \
                   "\nThere are a total of 5 levels, each getting more difficult for the explorers to navigate." \
                   "\nIn order for the explorers to move on to the next stage, 1/3 of them must succesfully" \
                   "\nnavigate through the course."

# Text with program guide text
guide_text = "How to use: " \
             "\nStep 1: Navigate through all the menu options to learn about the project." \
             "\nStep 2: Press the Run button(light blue) to run the program." \
             "\nStep 3: Let the program run(There is a total of 5 missions)." \
             "\nStep 4: Close program when done viewing." \
             "\n\nLegend:" \
             "\nFrame = Number of moves take/allowed." \
             "\nGeneration = Number of attempts for that stage." \
             "\nExplorers Alive = Number of explorers that are still alive." \
             "\nLast Generation = Stats from the last attempt  compared to the current." \
             "\nTotal Explorers = The number of explorers generated." \
             "\nSuccessful Explorers = Number of explorers that reached the goal." \
             "\nFitness = Success rate." \
             "\nFastest Time = Fastest explorer to reach the goal "

# Window that shows  name information text
def name_window():
    toplevel = Toplevel()
    toplevel.title("Name")
    label1 = Label(toplevel, text=name_text, height=0, width=70, background="lightblue")
    label1['font'] = textFont
    label1.pack()

#Window that shows description text
def description_window():
    toplevel = Toplevel()
    toplevel.title("Description")
    label2 = Label(toplevel, text=description_text, height=0, width=70, background="lightblue")
    label2['font'] = textFont
    label2.pack()

#Window that shows guide text,
def guide_window():
    toplevel = Toplevel()
    toplevel.title("Guide")
    label3 = Label(toplevel, text=guide_text, height=0, width=70, background="lightblue")
    label3['font'] = textFont
    label3.pack()

# Name button set to the top frame, name window is bound to this button
button1 = Button(topFrame, text='Name', relief=RIDGE,background='white', padx=18, pady=2, command = name_window)
button1['font'] = buttonFont
button1.pack(side=LEFT)

# Description button set to the top frame, description window is bound to this button
button2 = Button(topFrame, text='Description', relief=RIDGE, background='white', padx=18, pady=2, command = description_window)
button2['font'] = buttonFont
button2.pack(side=LEFT)

# Guide button set to the top frame, guide window is bound to this button
button3 = Button(topFrame, text='Guide', relief=RIDGE, background='white', padx=18, pady=2, command = guide_window)
button3['font'] = buttonFont
button3.pack(side=LEFT)

# Exit button set to the top frame, window.destroy is bound to this button which destroys all active windows
button4 = Button(topFrame, text='Run', relief=RIDGE, background='lightblue', padx=45, pady=2,command=window.destroy)
button4['font'] = buttonFont
button4.pack(side=LEFT)

# Photo for the menu is named photo1 and the file is set to image.png
# Image is bound to the tkinter window
# Background is set to black
photo1 = PhotoImage(file="image1.png")
menuimage = Label(window, image=photo1, background='black')
menuimage.pack()

# Main loop for the tkinter window
window.mainloop()

################################################### GUI ###################################################
################################################### GUI ###################################################


################################################ VARIABLES ################################################
################################################ VARIABLES ################################################

# Initializes a pygame instance
pg.init()

# Pygame width, size and screen dimension and name
width, height = 1280, 720
screenSize = pg.display.set_mode((width,height))
pg.display.set_caption("Smart Exploration")

# Frame per second set to 160 since that is the max the monitor used to make the project can handle
fps = 160

# Font is set to default to make sure the user has the required font to run the program
defaultFont = pg.font.SysFont(None, 100)


# The generation count is set to 0 at the start
generationCount = 0

# Explorer count set to 300
explorerCount = 300

# Level count set to 1 at start
levelCount = 1

# Success count set to 0 at start
successCount = 0

# Obstacles list
obstacles = [ ]

# Gene pool list
genePool = []

# Boolean set to false at start until a criteria is met
finished = False

# Used to keep track of time
time = pg.time.Clock()

# Using random range from 100000 for the seed
random.seed(random.randrange(100000))

# Frame limit for explorers
moveLimit = 500

# Used to count the frames
frameCount = 0

# Average fitness
averageFitness = 0

# Differences between the average fitness
averageFitnessDifference = 0

# Fastest time
fastestTime = 0

# Difference between fastest times
fastestTimeDifference = 0

# Counts the current explorer count and sets it as the number of alive explorers
aliveExplorerCount = explorerCount

# Difference between the success amounts
successCountDifference = 0

# Random generator for color of the level
levelColor = [random.randrange(100) + 100, random.randrange(100) + 100, random.randrange(100) + 100]

################################################ VARIABLES ################################################
################################################ VARIABLES ################################################


################################################## MAIN ###################################################
################################################## MAIN ###################################################

# Function to display the text
def ShowText(string, x, y, size = 40, color=(255, 255, 255)):
    funcFont = pg.font.SysFont(None, size)
    screenSize.blit(funcFont.render(string, True, color), (x, y))

# Function to map our low and high values
def Remap(low1, high1, low2, high2, value):
    return low2 + (value - low1) * (high2 - low2) / (high1 - low1)

# Function used to calculate the distance between to points
def Distance(x1, x2, y1, y2):
    return math.sqrt(math.pow(x1-x2,2) + math.pow(y1-y2,2))

# Class object to create the obsticles for the explorers
class Obstacle(object):
    def __init__(self, x, y, width, height):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.subsurface = pg.Surface((self.width, self.height))

     # Defines how the obstacles will be drawn
    def Draw(self):
        pg.draw.rect(screenSize, (((210,150,75))), (self.x, self.y, self.width, self.height))

# DNA class object that will be used for the genetic algorithm
# Generates random movements until the limit of frames is met
class DNA(object):
    def __init__(self, genes=None):
        self.array = []
        self.chain = pg.math.Vector2()
        if genes:
            self.array = genes
        else:
            for i in range(moveLimit):
                self.chain.xy = random.random()*2-1, random.random()*2-1
                self.array.append(self.chain.xy)

    # Defines how partners will be made within the gene pool, it will mix two genes and create a new array of motion options
    def CrossOver(self, partner):
        newGenes = []
        middle = math.floor(random.randrange(len(self.array)))
        for i in range(len(self.array)):
            if i < middle:
                newGenes.append(partner.array[i])
            else:
                newGenes.append(self.array[i])

        return DNA(newGenes)


# Class object for the explorers
# Checks to see if the explorer is alive, has crashed or won,
# Initializes a new DNA if no DNA is found
#  Saves the time of the box that wins
class SmartExplorer(object):
    def __init__(self, dna=None):
        self.alive = True
        self.crashed = False
        self.won = False
        self.wonTime = 0
        if dna:
            self.gene = DNA(dna)
        else:
            self.gene = DNA()

        # Sets the dimensions/styles of the object
        # Creates the surface for collision checking
        self.x, self.y = 10, height//2
        self.size = 6
        self.acc = pg.math.Vector2()
        self.acc.xy = 0, 0
        self.vel = pg.math.Vector2()
        self.vel.xy = 0, 0
        self.velLimit = 55
        self.burstColor = pg.Color("blue")
        self.burstSize = 10
        self.fitness = 0
        self.subsurface = pg.Surface((self.size, self.size))
        self.subsurface.fill((235,245,255))
        self.subsurface.set_alpha(300)

    # Function to detect the colision, collisions can happen both with obstacles and window edges
    # If collision is detected, reduce the alive count by 1
    def CheckCollision(self, arr):
        global aliveExplorerCount
        if self.x + self.size > width or self.x < 0 or self.y < 0 or self.y + self.size > height:
            self.crashed = True
        for item in arr:
            if self.subsurface.get_rect(topleft=(self.x, self.y)).colliderect(item.subsurface.get_rect(topleft=(item.x, item.y))):
                self.crashed = True
        if self.crashed:
            self.alive = False
            aliveExplorerCount -= 1

    # Function to calculate the fitness, the closer the distance between the explorer and the goal is the higher the score
    def CalculateFitness(self):
        dist = Distance(self.x, finish.x, self.y, finish.y)
        self.fitness = Remap(0, width, 1, 0, dist)


    # Updates the movement of the explorers and collision
    def Update(self):
        if self.crashed:
            self.subsurface.fill((128, 0, 0))
        if self.alive:
            self.acc = self.gene.array[frameCount]
            if self.subsurface.get_rect(topleft=(self.x, self.y)).colliderect(winRect) and not self.won:
                self.won = True
                self.wonTime = frameCount
            if self.won:
                self.x, self.y = finish.x, finish.y
                self.vel.xy = 0, 0
                self.acc.xy = 0, 0
                self.alive = False

        self.vel += self.acc
        if self.vel.x > self.velLimit and self.acc.x > 0:
            self.vel.x = self.velLimit
        if self.vel.x < -self.velLimit and self.acc.x < 0:
            self.vel.x = -self.velLimit
        if self.vel.y > self.velLimit and self.acc.y > 0:
            self.vel.y = self.velLimit
        if self.vel.y < -self.velLimit and self.acc.y < 0:
            self.vel.y = -self.velLimit
        self.x += self.vel.x
        self.y += self.vel.y

    # Draws the thruster and burst size, direction and power
    def Draw(self):
        if self.alive:
            if frameCount % 5 == 0:
                self.burstColor = pg.Color("red")
                self.burstSize = 5
            else:
                self.burstColor = pg.Color("orange")
                self.burstSize = 5

            if math.fabs(self.vel.x) > math.fabs(self.vel.y):
                if self.vel.x > 0:
                    pg.draw.rect(screenSize, self.burstColor, (self.x - 5, self.y + 3, self.burstSize, 3))
                else:
                    pg.draw.rect(screenSize, self.burstColor, (self.x + 10, self.y + 3, self.burstSize, 3))
            else:
                if self.vel.y > 0:
                    pg.draw.rect(screenSize, self.burstColor, (self.x + 3, self.y - 5, 3, self.burstSize))
                else:
                    pg.draw.rect(screenSize, self.burstColor, (self.x + 3, self.y + 10, 3, self.burstSize))
        screenSize.blit(self.subsurface, (self.x, self.y))

# Goal point position, location, and detection
finish = pg.math.Vector2()
finish.xy = width-50, height//2
winSurface = pg.Surface((80, 80))
winRect = winSurface.get_rect(topleft=(finish.x-40, finish.y-40))

explorers = []
for i in range(explorerCount):
    explorers.append(SmartExplorer())

# Function used to handle the generations
# Handles the gene pool after every generation
# Has the stages map within with their set styles and obstacles
# Handles the creation of partners within the genene pool
def FinishGeneration():

    global finished, averageFitness, moveLimit, obstacles, successCount
    global generationCount, frameCount, levelCount, fastestTime
    global levelColor, averageFitnessDifference, fastestTimeDifference, successCountDifference, aliveExplorerCount

    tempLowestTime = fastestTime
    tempAvgFitness = averageFitness
    tempSuccessCount = successCount
    genePool.clear()
    maxFit = 0
    fastestTime = moveLimit
    lowestIndex = 0
    successCount = 0
    avgFitnessSum = 0
    maxFitIndex = 0
    for explorer in explorers:
        explorer.CalculateFitness()
        avgFitnessSum += explorer.fitness
        if explorer.fitness >= 1.0:
            successCount += 1
        if explorer.fitness > maxFit:
            maxFit = explorer.fitness
            maxFitIndex = explorers.index(explorer)
    successCountDifference = successCount - tempSuccessCount
    averageFitness = avgFitnessSum / len(explorers)
    averageFitnessDifference = averageFitness - tempAvgFitness

    for i, explorer in enumerate(explorers):
        if explorer.won:
            if explorer.wonTime < fastestTime:
                fastestTime = explorer.wonTime
                lowestIndex = i
    fastestTimeDifference = fastestTime - tempLowestTime

    for i, explorer in enumerate(explorers):
        n = int((explorer.fitness ** 2) * 100)
        if i == maxFitIndex:
            print(explorer.fitness)
            if successCount < 2:
                n = int((explorer.fitness ** 2) * 150)

        if i == lowestIndex and successCount > 1:
            n = int((explorer.fitness ** 2) * 500)           #

        for j in range(n):
            genePool.append(explorers[i])

    # If the success count of the explorers is the length divided by 3 add 1 to the level count
    if successCount >= len(explorers)//3:
        levelCount += 1

        # Level 1
        if levelCount == 1:
            moveLimit = 300
            obstacles = [

            ]

         # Level 2
        elif levelCount == 2:
            moveLimit = 350
            obstacles = [
                Obstacle(690, 0, 20, 400),
                Obstacle(690, 470, 20, 250),
            ]
         # Level 3
        elif levelCount == 3:
            moveLimit = 400
            obstacles = [
                Obstacle(350, 200, 20, 320),
                Obstacle(750, 200, 20, 320),
                Obstacle(550, 0, 20, 200),
                Obstacle(550, 520, 20, 200)
            ]

         # Level 4
        elif levelCount == 4:
            moveLimit = 400
            obstacles = [
                Obstacle(300, 0, 20, 400),
                Obstacle(500, 420, 20, 300),
                Obstacle(410, 250, 200, 20),
                Obstacle(650, 0, 20, 200),
                Obstacle(650, 670, 20, 50),
                Obstacle(670, 0, 20, 300),
                Obstacle(670, 570, 20, 150),
                Obstacle(690, 0, 20, 400),
                Obstacle(690, 470, 20, 250),
                Obstacle(710, 0, 20, 400),
                Obstacle(710, 470, 20, 250),
                Obstacle(730, 0, 20, 400),
                Obstacle(730, 470, 20, 250),
                Obstacle(800, 370, 300, 20),
                Obstacle(800, 470, 300, 20),
            ]

         # Level 5 , final stage
        elif levelCount == 5:
            moveLimit = 450
            obstacles = [
                Obstacle(200, 100, 20, 620),
                Obstacle(500, 0, 20, 380),
                Obstacle(500, 530, 20, 190),
                Obstacle(800, 300, 20, 420),
                Obstacle(800, 0, 20, 200),
                Obstacle(1100, 0, 20, 350),
                Obstacle(1100, 450, 20, 270),
            ]

        # Generates random colors for the level text
        levelColor = [random.randrange(150)+100, random.randrange(150)+100, random.randrange(150)+100]

        explorers.clear()
        generationCount = 0
        for i in range(explorerCount):
            explorers.append(SmartExplorer())
    else:
        for i, explorer in enumerate(explorers):
            randomIndex = random.randint(0, len(genePool) - 1)
            parentA = genePool[randomIndex].gene
            randomIndex = random.randint(0, len(genePool) - 1)
            parentB = genePool[randomIndex].gene
            child = parentA.CrossOver(parentB)
            explorers[i] = SmartExplorer(child.array)
        generationCount += 1
    frameCount = 0
    aliveExplorerCount = explorerCount
    finished = False

# Makes sure the obsticles of mission 1 are always cleared
if levelCount == 1:
    moveLimit = 300
    obstacles = [

    ]

# Whilte loop to keep the pygame window open
# Allows the program to be closed if the x is clicked
while True:
    time.tick(fps)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    # Frame text
    counterText = "Frame: " + str(frameCount)
    counterLimitText = " / " + str(moveLimit)

    # Fills the background with black
    screenSize.fill((0,0,0))

    # Draws the obsticles
    for wall in obstacles:
        wall.Draw()

    # Handles the explorer alive count, drawing and collisions
    for explorer in explorers:
        explorer.Draw()
        if explorer.alive:
            explorer.CheckCollision(obstacles)
            explorer.Update()

    # Text that live generates the current stats
    ShowText(counterText, 10, 30)
    ShowText(counterLimitText, 160, 33, 30)
    ShowText("Generation: " + str(generationCount), 10, 80)
    ShowText("Explorer's Alive: " + str(aliveExplorerCount), 10, 110, 30)
                                                                            # .
    ShowText("Last Geneneration:", 10, 550, 45)
    ShowText("Total Explorers:             " + str(len(explorers)), 30, 590, 25)
    ShowText("Successful Explorers:   " + str(successCount), 30, 610, 25)
    if successCountDifference > 0:
        ShowText("+" + str(successCountDifference), 250, 610, 25, pg.Color(0,255,255)) # .
    else:                                                                   # .
        ShowText("-" + str(-successCountDifference), 250, 610, 25, pg.Color("red"))  # .

    ShowText("Fitness:            " + str(round(averageFitness, 3)), 30, 630, 25)
    if averageFitnessDifference > 0:
        ShowText("+" + str(round(averageFitnessDifference, 3)), 250, 630, 25, pg.Color("green"))
    else:
        ShowText("-" + str(round(-averageFitnessDifference, 3)), 250, 630, 25, pg.Color("red"))

    ShowText("Fastest Time :           " + str(fastestTime), 30, 650, 25)
    if fastestTimeDifference > 0:
        ShowText("+" + str(fastestTimeDifference), 250, 650, 25, pg.Color("red"))
    else:
        ShowText("-" + str(-fastestTimeDifference), 250, 650, 25, pg.Color("green"))

    ShowText("Stage " + str(levelCount), 550, 20, 80, levelColor)
    if levelCount == 5:
        ShowText("Final", 604, 80, 40, levelColor)

    # Draws the final goal circle
    pg.draw.circle(screenSize, pg.Color(0,255,255), (int(finish.x), int(finish.y)), 35)       #

    # Updates the screen
    pg.display.update()

    # Keeps count of the frames allowed per mission/generation
    if (frameCount >= moveLimit-1 and levelCount < 6) or aliveExplorerCount <= 0:
        frameCount = moveLimit-1
        finished = True
    else:
        frameCount += 1

    # Initiates the reset
    if finished:
        FinishGeneration()

################################################## MAIN ###################################################
################################################## MAIN ###################################################