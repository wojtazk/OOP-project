import pygame


class LowerPipe:
    def __init__(self, x, y, gravity, height):
        self.height = height

        # set pipe's position
        self.x = x
        self.y = y

        # load pipe's textures
        self.pipe_mid = pygame.image.load('images/pipe/pipe_mid.png')
        self.pipe_end = pygame.image.load('images/pipe/pipe_end.png')

        # scale pipe's textures
        pipe_mid_rec = (self.pipe_mid.get_width() / 2, height)  # scale to match the passed height
        pipe_end_rec = (self.pipe_end.get_width() / 2, self.pipe_end.get_height() / 2)
        self.pipe_mid = pygame.transform.scale(self.pipe_mid, pipe_mid_rec)  # override with scaled texture
        self.pipe_end = pygame.transform.scale(self.pipe_end, pipe_end_rec)  # override with scaled texture

        # adjust pipe's position (move it up basically)
        self.y = y - self.pipe_mid.get_height()

        self.velocity = gravity * 5

    def get_position(self):
        return pygame.Vector2(self.x, self.y)

    def get_height(self):
        return self.height

    def get_width(self):
        return self.pipe_end.get_width()

    def draw(self, screen):
        self.x -= self.velocity  # subtract velocity from x coordinate to make the pipe move

        screen.blit(self.pipe_mid, self.get_position())
        screen.blit(self.pipe_end, self.get_position())
