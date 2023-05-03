import random

from models.LowerPipe import LowerPipe
from models.UpperPipe import UpperPipe


class Pipe:
    def __init__(self, x, window_height, gap, gravity):
        self.height = window_height - gap
        self.gap = gap

        self.upper_pipe_height = random.randint(100, int(self.height - 100))
        self.lower_pipe_height = self.height - self.upper_pipe_height

        self.upper_pipe = UpperPipe(x, 0, gravity, self.upper_pipe_height)
        self.lower_pipe = LowerPipe(x, window_height, gravity, self.lower_pipe_height)

    def draw(self, screen):
        self.upper_pipe.draw(screen)
        self.lower_pipe.draw(screen)



