import pygame
import random

from models.LowerPipe import LowerPipe
from models.UpperPipe import UpperPipe


class Pipe:
    # load pipes textures
    pipe_mid_texture = pygame.image.load('images/pipe/pipe_mid.png')
    pipe_end_texture = pygame.image.load('images/pipe/pipe_end.png')

    # scale pipe's textures
    pipe_mid_rec = (pipe_mid_texture.get_width() / 2, pipe_mid_texture.get_height())
    pipe_end_rec = (pipe_end_texture.get_width() / 2, pipe_end_texture.get_height() / 2)

    pipe_mid_texture = pygame.transform.scale(pipe_mid_texture, pipe_mid_rec)  # override with scaled texture
    pipe_end_texture = pygame.transform.scale(pipe_end_texture, pipe_end_rec)  # override with scaled texture

    def __init__(self, x, window_height, gap, gravity):
        self.height = window_height - gap
        self.gap = gap
        self.gravity = gravity

        #  make textures render ready
        self.pipe_mid_texture = self.pipe_mid_texture.convert_alpha()
        self.pipe_end_texture = self.pipe_end_texture.convert_alpha()

        self.upper_pipe_height = random.randint(50, int(self.height - 50))
        self.lower_pipe_height = self.height - self.upper_pipe_height

        self.upper_pipe = UpperPipe(x, 0, gravity, self.upper_pipe_height, self.pipe_mid_texture, self.pipe_end_texture)
        self.lower_pipe = LowerPipe(x, window_height, gravity, self.lower_pipe_height,
                                    self.pipe_mid_texture, self.pipe_end_texture)

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

        self.upper_pipe = UpperPipe(x, 0, self.gravity, self.upper_pipe_height,
                                    self.pipe_mid_texture, self.pipe_end_texture)
        self.lower_pipe = LowerPipe(x, self.height + self.gap, self.gravity, self.lower_pipe_height,
                                    self.pipe_mid_texture, self.pipe_end_texture)
