'''
Starting point for the program
Initialize the UI here
'''

import sys
import pygame
from robot import Robot, BotNet

pygame.init()

size = width, height = 320, 500

screen = pygame.display.set_mode(size)
circle_center = (width/2, 100)
bots = BotNet(circle_center, 2, randomize=True)

randStart = pygame.image.load("randstart.bmp")
randRect = randStart.get_rect()
centerStart = pygame.image.load("centerstart.bmp")
centerRect = centerStart.get_rect()
singleStart = pygame.image.load("onestart.bmp")
singleRect = singleStart.get_rect()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            d = event.__dict__
            if d['button'] == 1:
                if randRect.left <= d['pos'][0] <= randRect.right:
                    if randRect.bottom <= d['pos'][1] <= randRect.top:
                        print "start all random po 50 times"
                if centerRect.left <= d['pos'][0] <= centerRect.right:
                    if centerRect.bottom <= d['pos'][1] <= centerRect.top:
                        print "start all random po 50 times"
                if singleRect.left <= d['pos'][0] <= singleRect.right:
                    if singleRect.bottom <= d['pos'][1] <= singleRect.top:
                        print "start all random po 50 times"

    # colour background
    screen.fill((0xaa, 0xaa, 0xaa))
    # add circle
    pygame.draw.circle(screen, (0, 0, 0), circle_center, 75, 2)
    pygame.draw.circle(screen, (0, 0, 0), circle_center, 2, 0)

    screen.blit(randStart, randRect)
    screen.blit(centerStart, centerRect)
    screen.blit(singleStart, singleRect)



    bots.update()
    bots.draw(screen)

    pygame.display.flip()
    pygame.time.delay(10)
