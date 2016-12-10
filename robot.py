import pygame
import math
import random


class Robot(object):
    def __init__(self, id, start_pos, bot_net):
        self.id = id
        self.center = start_pos
        self.pos = start_pos
        self.moveSpeed = 2
        self.color = (219, 86, 19)
        self.outline = (0, 0, 0)
        self.size = 5
        self.botNet = bot_net
        self.destination = None

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.pos, self.size, 0)
        pygame.draw.circle(surface, self.outline, self.pos, self.size, 1)
        if self.destination is not None:
            pygame.draw.circle(surface, (255, 0, 0), self.destination, 3, 0)

    def set_dest(self, dest_pos):
        self.destination = dest_pos

    def update(self):
        if self.destination is not None:
            # move towards destination
            if self.pos != self.destination:
                d = math.sqrt((self.destination[0]-self.pos[0])**2 + (self.destination[1]-self.pos[1])**2)
                dt = self.moveSpeed
                t = dt /d
                x = int((1 - t)*self.pos[0] + t*self.destination[0])
                y = int((1 - t)*self.pos[1] + t*self.destination[1])
                self.pos = (x, y)
            else:
                print "bot {id} reached dest".format(id=self.id)
                self.destination = None


class BotNet(object):
    def __init__(self, circle_center, bot_count=1, randomize=False):
        random.seed()
        self.bots = []
        while bot_count > 0:
            startpos = circle_center
            if randomize:
                t = 2*math.pi*random.random()
                u = random.random() + random.random()
                r = 2-u if u > 1 else u
                r *= 75
                x = circle_center[0] + int(r*math.cos(t))
                y = circle_center[1] + int(r*math.sin(t))
                startpos = (x, y)

                vX = startpos[0] - circle_center[0]
                vY = startpos[1] - circle_center[1]
                magV = math.sqrt(vX*vX + vY*vY)
                dest = (int(circle_center[0]+vX / magV * 75), int(circle_center[1]+vY / magV * 75))
            else:
                dest = (circle_center[0], circle_center[1] + 75)

            newBot = Robot(bot_count, startpos, self)
            newBot.set_dest(dest)

            self.bots.append(newBot)
            bot_count -= 1

    def exit_found(self, exit_pos):
        for bot in self.bots:
            bot.set_dest(exit_pos)

    def update(self):
        for bot in self.bots:
            bot.update()

    def draw(self, surface):
        for bot in self.bots:
            bot.draw(surface)
