'''
Starting point for the program
Initialize the UI here
'''

import sys
import pygame
from pygame.locals import *
from robot import Robot, BotNet

pygame.init()

size = width, height = 320, 500

screen = pygame.display.set_mode(size)
circle_center = (width/2, 200)
bots = BotNet(circle_center, 3, randomize=True)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    # colour background
    screen.fill((0xaa, 0xaa, 0xaa))
    # add circle
    pygame.draw.circle(screen, (0, 0, 0), circle_center, 75, 2)

    bots.update()
    bots.draw(screen)

    pygame.display.flip()
