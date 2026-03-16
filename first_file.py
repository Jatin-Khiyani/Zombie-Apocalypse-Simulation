# Module used to visulize simulation 
import pygame
import random

# Setting Fixed Screen Size : In the Future could take input from the user
WIDTH = 1280
HEIGHT = 720
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))

# Defining Colors 
COLOR_DEFINATION = {
    "grey" : (35,35,30),
    "light_gray" : (70,70,90),
    "white" : (255,248,240),
    "red" :(239,71,111),
    "blue": (17,138,178),
    "black" : (0,0,0)
}

# Associating color with different objects 
COLORS = {
    "background" : COLOR_DEFINATION["grey"],
    "light_grey" : COLOR_DEFINATION["white"],
    "healthy" : COLOR_DEFINATION["red"],
    "immune" : COLOR_DEFINATION["blue"],
    "dead" : COLOR_DEFINATION["black"]

}

# Defining a class for people 
class Person:

    # Function for setting position of a person
    def __init__(self):
        self.x = random.uniform(0,WIDTH)
        self.y = random.uniform(0,HEIGHT)
    
    def show(self,size = 10):
        pygame.draw.circle(SCREEN,COLOR_DEFINATION["white"],(self.x,self.y),size)


person1 = Person()
person2 = Person()
# Used to open and close the window for simulation 
animating = True
while animating:

    #Setting Background Color
    SCREEN.fill(COLORS["background"])

    person1.show()
    person2.show()
 
    #Update Screen
    pygame.display.flip()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            animating = False 