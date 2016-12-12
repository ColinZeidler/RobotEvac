import pygame
import math
import random
import time


class Robot(object):
    def __init__(self, id, start_pos, bot_net, circle_center, orbit_cw=None):
        self.id = id
        self.center = start_pos
        self.pos = start_pos
        self.float_pos = start_pos
        self.moveSpeed = 1
        self.color = (219, 86, 19)
        self.outline = (0, 0, 0)
        self.size = 5
        self.botNet = bot_net
        self.destination = None
        self.dest_evac = False
        self.orbit = False
        self.orbit_CW = orbit_cw
        self.c_center = circle_center
        self.trails = []

    def draw(self, surface):
        for trail in self.trails:
            trail.draw(surface)
        pygame.draw.circle(surface, self.color, self.pos, self.size, 0)
        pygame.draw.circle(surface, self.outline, self.pos, self.size, 1)
        if self.destination is not None:
            pygame.draw.circle(surface, (255, 0, 0), self.destination, 3, 0)

    def set_dest(self, dest_pos, evac=False):
        self.destination = dest_pos
        self.dest_evac = evac

    def update(self):
        self.trails.append(Trail(self.pos))
        if self.destination is not None:
            # move towards destination
            if self.pos != self.destination:
                d = math.sqrt((self.destination[0]-self.float_pos[0])**2 + (self.destination[1]-self.float_pos[1])**2)
                dt = self.moveSpeed
                t = dt /d
                x = (1 - t)*self.float_pos[0] + t*self.destination[0]
                y = (1 - t)*self.float_pos[1] + t*self.destination[1]
                self.float_pos = (x, y)
                self.pos = (int(round(x)), int(round(y)))
            if self.destination[0]-1 <= self.pos[0] <= self.destination[0]+1:
                if self.destination[1]-1 <= self.pos[1] <= self.destination[1]+1:

                    if self.dest_evac:
                        self.destination = None
                        self.orbit = False
                        self.botNet.exited(self)
                    else:
                        self.destination = None
                        self.orbit = True
                        if self.orbit_CW is None:
                            if random.randint(0, 1) == 0:
                                self.orbit_CW = True
                            else:
                                self.orbit_CW = False

        else:
            if self.orbit:
                r_speed = self.moveSpeed/75.0
                if not self.orbit_CW:
                    r_speed *= -1  # make direction CCW
                sA = math.sin(r_speed)
                cA = math.cos(r_speed)
                dx = (self.float_pos[0] - self.c_center[0])
                dy = (self.float_pos[1] - self.c_center[1])
                x = self.c_center[0] + cA * dx - sA * dy
                y = self.c_center[1] + sA * dx + cA * dy

                self.float_pos = (x, y)
                self.pos = (int(round(x)), int(round(y)))


class BotNet(object):
    def __init__(self, circle_center, bot_count=1, mode="none"):
        random.seed()
        self.bots = []
        self.bots_finished = []
        self.evac = EvacPoint(circle_center, 75, self)
        self.startTime = time.time()
        self.endTime = 0
        self.runTime = 0
        self.done = False

        randomize = False
        if mode == "both":
            randomize = True

        while bot_count > 0:
            startpos = circle_center
            if bot_count == 1 and mode == "one":
                randomize = True
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
            orbit_dir = None
            if mode == "none":
                orbit_dir = True if bot_count == 1 else False
            newBot = Robot(bot_count, startpos, self, circle_center, orbit_dir)
            newBot.set_dest(dest)

            self.bots.append(newBot)
            bot_count -= 1

    def exit_found(self, exit_pos):
        for bot in self.bots:
            bot.set_dest(exit_pos, evac=True)

    def update(self):
        for bot in self.bots:
            if bot not in self.bots_finished:
                bot.update()
                self.evac.update(bot.pos)

    def draw(self, surface):
        for bot in self.bots:
            bot.draw(surface)
        self.evac.draw(surface)

    def exited(self, bot):
        self.bots_finished.append(bot)
        if len(self.bots_finished) == len(self.bots):
            self.endTime = time.time()
            self.runTime = self.endTime - self.startTime
            self.done = True


class EvacPoint(object):
    def __init__(self, circle_center, radius, botNet):
        # choose random pos
        angle = random.random() * math.pi * 2
        x = circle_center[0] + math.cos(angle) * radius
        y = circle_center[1] + math.sin(angle) * radius
        self.pos = (int(round(x)), int(round(y)))

        self.botNet = botNet
        self.color = (66, 134, 244)
        self.size = 4

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.pos, self.size, 0)
        pygame.draw.circle(surface, (0, 0, 0), self.pos, self.size, 1)

    def update(self, botPos):
        if self.pos[0] - 2 <= botPos[0] <= self.pos[0] + 2:
            if self.pos[1] - 2 <= botPos[1] <= self.pos[1] + 2:
                self.botNet.exit_found(self.pos)


class Trail(object):
    def __init__(self, pos):
        self.color = (255, 0, 0)
        self.pos = pos
        self.size = 1

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.pos, self.size, 0)
