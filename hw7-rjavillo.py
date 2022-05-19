# Name: Rainier Javillo
# Date: 12/3/2021
# File: hw7-rjavillo.py - In this game, the player controls a circle that can move in any direction (up/down and left/right) by moving the mouse. 
# Help from: https://youtu.be/cFlk9kyFtS0

import sys, pygame, time, random, math    # import libraries
from pygame.locals import *

pygame.init()                       # initialize pygame
size = width, height = 1280, 720    # size of the window, 1280, 720
black = 0, 0, 0                     # hex code for black
screen = pygame.display.set_mode(size, pygame.RESIZABLE)  # initialize a window or screen for display, of size 320x240
color = (128, 128, 128)             # hex code for gray


class LineObstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)             # initialize the sprite
        self.x = x                                      # x coord                             
        self.y = y                                      # y coord
        angle = 2 * math.pi * random.random()           # random angle
        mag = 2                                       # magnitude of the velocity vector is its speed
        self.vel_x = mag * math.cos(angle)              # velocity of x
        self.vel_y = -mag * math.sin(angle)             # velocity of y
    def line_angle(self):
        return math.atan2(-self.vel_y, self.vel_x)      # angle the line towards its direction of movement 
    def update(self):
        self.x += self.vel_x                            # move x coord by velocity of x
        self.y += self.vel_y                            # move y coord by velocity of y    
        direction = self.line_angle()                   # the direction of the line
        len_rand = (width/10)+random.randint(-10, 10)   # pick a random length about 1/10th the width of the screen
        x_dir = len_rand * math.cos(direction)          # move the x-coord 
        y_dir = len_rand * math.sin(direction)          # move the y-coord
        self.rect = pygame.draw.line(screen, color, (self.x+x_dir, self.y-y_dir), (self.x-x_dir, self.y+y_dir), 5)   # line(surface, color, start_pos, end_pos, width)

class PlayerCircle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)             # initialize the sprite
        self.x, self.y = pygame.mouse.get_pos()         # get the x-coord and y-coord from the mouse
        self.pos = [self.x, self.y]                     # put them together
        self.rect = pygame.draw.circle(screen, color, self.pos, 20)  # circle(surface, color, center, radius)
        
lines = []                                              # initialize the lines, empty at first
        
while 1:                                                # while true                                                         
    for event in pygame.event.get():                    # get events from the queue
        if event.type == pygame.QUIT: sys.exit()        # if event object is quit event, call sys.exit()
    screen.fill(black)                                  # make the screen black
    
    circle = PlayerCircle()                             # initialize the circle
    
    linesGroup = pygame.sprite.Group()                  # sprite group for lines 
    
    if random.uniform(0,1) <= 1/200:                   # control the rate of spawning new lines 
        x_rand = random.randrange(width+1)              # pick a random x coord
        y_rand = random.randrange(height+1)             # pick a random y coord
        lines += [LineObstacle(x_rand, y_rand) for i in range(1)]   # create a new line based on the random x and y, add to lines list
    
    for line in lines:              # for each line in lines list
        linesGroup.add(line)        # add line to sprite group
        
    for lineGroup in linesGroup:    # for each sprite in sprite group
        lineGroup.update()          # animate

    if pygame.sprite.spritecollide(circle, linesGroup, True):   # detect collision
        pygame.quit()                                           # quit the game
        sys.exit()                                              # exit
    
    pygame.display.flip()                       # update the contents of the entire display, similar to pygame.display.update()
    time.sleep (0.01)                           # suspend execution for 0.01s, acts as the refresh rate
