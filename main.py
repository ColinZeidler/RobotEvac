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

# Creating buttons
randStart = pygame.image.load("randstart.bmp")
randRect = randStart.get_rect()
centerStart = pygame.image.load("centerstart.bmp")
centerRect = centerStart.get_rect()
singleStart = pygame.image.load("onestart.bmp")
singleRect = singleStart.get_rect()

# position the buttons
randRect.move_ip([60, 275])
centerRect.move_ip([60, 350])
singleRect.move_ip([60, 425])
# end of buttons

run_count = 0
running = False
mode = ""

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            d = event.__dict__
            if d['button'] == 1:
                if randRect.left <= d['pos'][0] <= randRect.right:
                    if randRect.top <= d['pos'][1] <= randRect.bottom:
                        print "start all random pos 50 times"
                        mode = "both"
                        bots = BotNet(circle_center, 2, mode)
                        running = True
                        run_count = 0
                if centerRect.left <= d['pos'][0] <= centerRect.right:
                    if centerRect.top <= d['pos'][1] <= centerRect.bottom:
                        print "start all center 50 times"
                        mode = "none"
                        bots = BotNet(circle_center, 2, mode)
                        running = True
                        run_count = 0
                if singleRect.left <= d['pos'][0] <= singleRect.right:
                    if singleRect.top <= d['pos'][1] <= singleRect.bottom:
                        print "start one random pos 50 times"
                        mode = "one"
                        bots = BotNet(circle_center, 2, mode)
                        running = True
                        run_count = 0

    # colour background
    screen.fill((0xaa, 0xaa, 0xaa))
    # add circle
    pygame.draw.circle(screen, (0, 0, 0), circle_center, 75, 2)
    pygame.draw.circle(screen, (0, 0, 0), circle_center, 2, 0)

    screen.blit(randStart, randRect)
    screen.blit(centerStart, centerRect)
    screen.blit(singleStart, singleRect)

    if running and run_count < 50:
        bots.update()
        bots.draw(screen)
        if bots.done:
            print "run {}, time: {}".format(run_count, bots.runTime)
            run_count += 1
            bots = BotNet(circle_center, 2, mode)

    if run_count >= 50:
        running = False

    pygame.display.flip()
    pygame.time.delay(10)
