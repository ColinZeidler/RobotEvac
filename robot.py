import pygame


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

    def set_dest(self, dest_pos):
        self.destination = dest_pos

    def update(self):
        if self.destination is not None:
            # move towards destination
            pass


class BotNet(object):
    def __init__(self, circle_center, bot_count=1, randomize=False):
        self.bots = []
        while bot_count > 0:
            startpos = circle_center
            if randomize:
                startpos = circle_center  # TODO make this random
            self.bots.append(Robot(bot_count, startpos, self))
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
