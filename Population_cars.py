import pygame
import random
from neuron import Population
from car import Car

def sortBests(elem):
    return elem[1]

class Population_cars:
    def __init__(self, PopNumber,id=0,prevBest=[]):


        self.id=id

        self.initialnumber=PopNumber
        self.still_alive=PopNumber
        self.actual_score=0

        self.death_records=[]

        self.death_lines=[
            [[200, 100], [600, 100],[900, 300],[850, 600],[560, 340],[250, 340],[250,390],[480,390],[500,530],[520,350],[850, 610]],
            [[200, 250], [600, 250],[750, 300],[750, 400],[600, 290],[200, 290],[200,460],[400,460],[550,660],[560,450],[850, 650]]
        ]


        self.checkpoints=[[self.death_lines[0][i],self.death_lines[1][i]] for i in range(len(self.death_lines[0]))]

        self.brains= Population(PopNumber,[5,4,4,3],prevBest)
        self.population=[]
        for i in range(PopNumber):
            self.population.append(Car(self.brains.population[i],i))
        while True:
            self.actual_score+=1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.draw()

            deleted=0
            for i in range(len(self.population)):
                car=self.population[i-deleted]

                car.advance_car()

                if self.actual_score%2==0:
                    car.takeDecision(self.death_lines)
                else:
                    car.takeSameDecision()

                if car.detectCollision(self.death_lines,self.checkpoints):
                    self.death_records.append((car.brain,car.fitness(self.checkpoints)))
                    self.still_alive-=1
                    self.population.pop(i-deleted)
                    deleted+=1

            if self.still_alive==0:
                self.nextGeneration()



            pygame.display.flip()

    def draw(self):
        global screen
        screen.fill((255, 255, 255))
        for car in self.population:
            full_car = car.positions.copy()
            last_x = full_car[2][0] + (full_car[0][0] - full_car[1][0])
            last_y = full_car[2][1] + (full_car[0][1] - full_car[1][1])
            full_car.append([last_x, last_y])
            if self.id!=1 and car.id<=4:
                pygame.draw.polygon(screen, (0,255,255), full_car, 0)
            else:
                pygame.draw.polygon(screen, (255,0,0), full_car, 0)
            #pygame.draw.circle(screen,[0,0,0],tuple(map(int,car.getCenter())),100,1)
        for death_line in self.death_lines:
            for i in range(len(death_line) - 1):
                pygame.draw.line(screen, [0, 0, 0], death_line[i], death_line[i+1], 3)
        for check_line in self.checkpoints:
            pygame.draw.line(screen, [100, 200, 100], check_line[0], check_line[1], 1)



    def nextGeneration(self):
        global pop
        self.death_records.sort(key=sortBests)
        thisBests = self.death_records[-5:]
        print(thisBests)
        pop=Population_cars(self.initialnumber,self.id+1,thisBests)










        # --------------------------------------------------------------------------------------------------



WINDOW_WIDTH = 1500
WINDOW_HEIGHT = 750
WINDOW_SIZE = [WINDOW_WIDTH, WINDOW_HEIGHT]


pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Car AI")

pop=Population_cars(100)