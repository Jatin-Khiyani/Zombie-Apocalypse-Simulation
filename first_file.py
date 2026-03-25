# Code Written using Youtube Tutorial https://youtube.com/playlist?list=PLBLV84VG7Md_JGMCHNOqvAvsTPc7zi1xB&si=FpVEBl7iPVz-pjh5

# Module used to visulize simulation 

import pygame
import random
import math
from matplotlib import pyplot


pygame.init()
# Setting Fixed Screen Size : In the Future could take input from the user
WIDTH = 1920
HEIGHT = 1080
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT),pygame.RESIZABLE)

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
# Creating Grids and Cells for better imporving computational complexity
class Cell():
    def __init__(self,row,col):
        self.row = row 
        self.col = col
        self.people = []

    def get_neighboring_cells(self,n_rows,n_cols):
        index = self.row * n_cols + self.col
        N = index - n_cols if self.row > 0 else None
        S = index + n_cols if self.row < n_rows - 1 else None
        W = index - 1 if self.col > 0 else None
        E = index + 1 if self.col < n_cols  - 1 else None
        NW = index - n_cols -1 if self.row > 0 and self.col > 0 else None
        NE = index - n_cols -1 if self.row > 0 and self.col < n_cols -1 else None
        SW = index + n_cols - 1 if self.row < n_rows -1 and self.col > 0 else None
        SE = index + n_cols + 1 if self.row < n_rows -1 and self.col < n_cols -1 else None
        return[i for i in [index,N,S,E,W,NW,NE,SW,SE]if i]


class Grid():
    def __init__(self,people,h_size = 20, v_size = 20):
        self.h_size = h_size
        self.v_size = v_size
        self.n_rows = HEIGHT// v_size
        self.n_cols = WIDTH // h_size
        self.cells = []
        for row in range(self.n_rows):
            for col in range(self.n_cols):
                self.cells.append(Cell(row,col))
        self.store_people(people)

    def store_people(self,people):
        for p in people:
            row = min(int(p.y / self.v_size), self.n_rows - 1)
            col = min(int(p.x / self.h_size), self.n_cols - 1)
            index = row * self.n_cols + col
            self.cells[index].people.append(p)
    
    def show(self,width = 1):
        for c in self.cells:
            x = c.col * self.h_size
            y = c.row *self.v_size
            rect = pygame.Rect(x,y,self.h_size,self.v_size)
            pygame.draw.rect(SCREEN,COLOR_DEFINATION["light_gray"],rect,width=width)

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
        self.recovery_counter = 0
        self.immunity_counter = 0


    # Function to show dots as persons 
    def show(self,size = 10):
        pygame.draw.circle(SCREEN,COLORS[self.state],(self.x,self.y),size)

    # Function to make dots move in random direction 
    def move(self,speed = 0.05):

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
    def get_infected(self, value = 1000):
        self.state = "infected"  
        self.recovery_counter = value

    
    def recover(self,value = 2000):
        self.recovery_counter -= 1
        if self.recovery_counter == 0:
            self.state = "immune"
            self.immunity_counter = value
    
    def lose_immunity(self):
        self.immunity_counter -= 1 
        if self.immunity_counter == 0:
            self.state = "healthy"

    def die(self,probablity = 0.00001):
        if random.uniform(0,1) < probablity:
            self.state = "dead"


class Pandemic():
    def __init__(self, n_people = 10000, size = 3, speed = 0.03,
    infect_dist = 10, recover_time = 200, immune_time = 1000,
    prob_catch = 0.1, prob_death = 0.005):
        
        self.people = [Person() for i in range (n_people)]
        self.size = size
        self.speed = speed
        self.infect_dist = infect_dist
        self.recover_time = recover_time
        self.immune_time = immune_time
        self.prob_catch = prob_catch
        self.prob_death = prob_death
        self.people[0].get_infected(self.recover_time)
        self.grid = Grid(self.people)
        self.record = []
        self.over = False
        

    def update_grid(self):
        self.grid = Grid(self.people)

     # for loop  to infect other people (Highly Computationally intesive needed to be changed in the future)
    def slowly_infect_people(self):
       
        for p in self.people:
            if p.state == "infected":
                for other in self.people:
                    if other.state == "healthy":
                        dist = math.sqrt((p.x-other.x)**2 + (p.y-other.y)**2)
                        if dist < self.infect_dist:
                            other.get_infected()
    

    def infect_people(self):
        for c in self.grid.cells:

            #move on if nobody is infected in that cell
            states = [p.state for p in c.people]
            if states.count("infected") == 0:
                continue

            #Create list of all/infected/healthy people in the (3x3) area 

            people_in_area = []
            for index in c.get_neighboring_cells(self.grid.n_rows,self.grid.n_cols):
                people_in_area += self.grid.cells[index].people
                infected_people = [p for p in people_in_area if p.state == "infected"]
                healthy_people = [p for p in people_in_area if p.state == "healthy"]

                if len(healthy_people) == 0:
                    continue

                # Loop Through the infected people 
                for i in infected_people:
                    for h in healthy_people:
                        dist = math.sqrt((i.x-h.x)**2 + (i.y-h.y)**2)
                        if dist < self.infect_dist:
                            if random.uniform(0,1) < self.prob_catch:
                                h.get_infected(self.recover_time)



    def run(self):
        self.update_grid()
        self.infect_people()

        for p in self.people:
            if p.state == "infected":
                p.die(self.prob_death)
                p.recover(self.immune_time)
                p.move(self.speed)
                p.show(self.size)
            if p.state == "immune":
                p.lose_immunity()
                p.move(self.speed)
                p.show(self.size)
            elif p.state == "healthy":
                p.move(self.speed)
                p.show(self.size)
            elif p.state == "dead":
                p.show(self.size)
    
    def keep_track(self):
        states = [p.state for p in self.people]
        n_infected = states.count("infected")
        n_dead = states.count("dead")
        n_healthy = states.count("healthy")
        self.record.append((n_infected,n_dead,n_healthy))
        if n_infected == 0:
            self.over = True

    def summarize(self):
        time_index = range(1,len(self.record)+1)
        infected_people = [r[0] for r in self.record]
        dead = [r[1] for r in self.record]
        healthy = [r[2] for r in self.record]

        fig, ax = pyplot.subplots()
        ax.plot(time_index,infected_people,color = "red")
        ax.set_xlabel("Period")
        ax.set_ylabel("People currently infected", color = "red")
        pyplot.show()


pandemic = Pandemic()

# Pygame loop
# Code to keep track of frame rate 
clock = pygame.time.Clock()
font = pygame.font.Font("freesansbold.ttf",32)
# Used to open and close the window for simulation 
animating = True
pausing = False
while animating and not pandemic.over:

    if not pausing:

        #Setting Background Color
        SCREEN.fill(COLORS["background"]) 

        # Run pandemic and keep track 
        pandemic.run()
        pandemic.keep_track()

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
        # user presses key on keyboard

        if event.type == pygame.KEYDOWN:
        # escape key to close the animation
            if event.key == pygame.K_ESCAPE:
                animating = False
        # return key to restart with a new pandemic
            if event.key == pygame.K_RETURN:
                pausing = False
                pandemic = Pandemic()

        # Space bar to pause and un pause animation
            if event.key == pygame.K_SPACE:
                pausing = not pausing

#Create Summary Plot of Pandemic
pandemic.summarize()

