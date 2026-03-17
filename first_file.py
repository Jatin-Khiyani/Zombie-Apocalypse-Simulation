# Code Written using Youtube Tutorial https://youtube.com/playlist?list=PLBLV84VG7Md_JGMCHNOqvAvsTPc7zi1xB&si=FpVEBl7iPVz-pjh5

# Module used to visulize simulation 

import pygame
import random
import math
pygame.init()
# Setting Fixed Screen Size : In the Future could take input from the user
WIDTH = 1280
HEIGHT = 720
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))

# Defining Colors 
COLOR_DEFINATION = {
    "grey" : (35,35,30),
    "light_gray" : (70,70,90),
    "white" : (255,248,240),
    "red" : (239,71,111),
    "blue": (17,138,178),
    "black" : (0,0,0)
}

# Associating color with different states
COLORS = {
    "background" : COLOR_DEFINATION["grey"],
    "light_grey" : COLOR_DEFINATION["white"],
    "healthy" : COLOR_DEFINATION["white"],
    "infected" : COLOR_DEFINATION["red"],
    "immune" : COLOR_DEFINATION["blue"],
    "dead" : COLOR_DEFINATION["black"]

}

# Defining a class for people 
class Person:

    # Function for setting position of a person
    def __init__(self):
        # Defining Position 
        self.x = random.uniform(0,WIDTH)
        self.y = random.uniform(0,HEIGHT)
        # Defining Velocity Vector 
        self.dx = 0
        self.dy = 0
        self.state = "healthy"

    # Function to show dots as persons 
    def show(self,size = 10):
        pygame.draw.circle(SCREEN,COLORS[self.state],(self.x,self.y),size)

    # Function to make dots move in random direction 
    def move(self,speed = 0.1):

        # Chaning the position according to velocity
        self.x += self.dx 
        self.y += self.dy

        # Updating Velocity 
        self.dx += random.uniform(-speed,speed)
        self.dy += random.uniform(-speed,speed)

        # Avoid Going out of bounds 
        if self.x >= WIDTH:
            self.x = WIDTH - 1
            self.dx *= -1
        if self.y  >= HEIGHT:
            self.y = HEIGHT - 1
            self.dy *= -1
        if self.x <=0:
            self.x = 1
            self.dx *= -1
        if self.y <= 0:
            self.y = 1
            self.dy *= -1
    def get_infected(self):
        self.state = "infected"

# Generating People
people = [Person() for i in range(1000)]
people[0].get_infected()

# Code to keep track of frame rate 

clock = pygame.time.Clock()
font = pygame.font.Font("freesansbold.ttf",32)
# Used to open and close the window for simulation 
animating = True
while animating:

    #Setting Background Color
    SCREEN.fill(COLORS["background"])

    # Showing people 
    for p in people:
        p.move()
        p.show()

    # for loop  to infect other people (Highly Computationally intesive needed to be changed in the future)
    for p in people:
        if p.state == "infected":
            for other in people:
                if other.state == "healthy":
                    dist = math.sqrt((p.x-other.x)**2 + (p.y-other.y)**2)
                    if dist < 20:
                        other.get_infected()
    
    #Update Screen and the clock
    clock.tick()
    clock_string = str(math.floor(clock.get_fps()))
    text = font.render(clock_string,True,COLOR_DEFINATION["blue"],COLORS["background"])
    text_box = text.get_rect(topleft=(10,10))
    SCREEN.blit(text,text_box)
    pygame.display.flip()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            animating = False 