import pygame
import random

from models.LowerPipe import LowerPipe
from models.UpperPipe import UpperPipe


class Pipe:
    def __init__(self, x, window_height, gap, gravity):
        self.height = window_height - gap
        self.gap = gap
        self.gravity = gravity

        self.upper_pipe_height = random.randint(50, int(self.height - 50))
        self.lower_pipe_height = self.height - self.upper_pipe_height

        self.upper_pipe = UpperPipe(x, 0, gravity, self.upper_pipe_height)
        self.lower_pipe = LowerPipe(x, window_height, gravity, self.lower_pipe_height)

    def draw(self, screen):
        self.upper_pipe.draw(screen)
        self.lower_pipe.draw(screen)

    def get_width(self):
        return self.upper_pipe.get_width()

    def is_visible(self):
        return self.upper_pipe.get_position().x + self.upper_pipe.get_width() > 0

    def get_x(self):
        return self.upper_pipe.get_x()

    def recycle(self, x):
        self.upper_pipe_height = random.randint(50, int(self.height - 50))
        self.lower_pipe_height = self.height - self.upper_pipe_height

        self.upper_pipe = UpperPipe(x, 0, self.gravity, self.upper_pipe_height)
        self.lower_pipe = LowerPipe(x, self.height + self.gap, self.gravity, self.lower_pipe_height)
