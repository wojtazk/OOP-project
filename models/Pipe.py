import pygame


class Pipe:
    def __init__(self, x, y, gravity, height, pipe_mid, pipe_end):
        self.height = height

        # set pipe's position
        self.x = x
        self.y = y

        # load pipe's textures
        self.pipe_mid = pipe_mid
        self.pipe_end = pipe_end

        # scale mid pipe's textures
        pipe_mid_rec = (self.pipe_mid.get_width(), height)  # scale to match the passed height
        self.pipe_mid = pygame.transform.scale(self.pipe_mid, pipe_mid_rec)  # override with scaled texture

        self.velocity = gravity * 5

    def get_position(self):
        return pygame.Vector2(self.x, self.y)

    def get_masks(self):
        return [
            pygame.mask.from_surface(self.pipe_mid),
            pygame.mask.from_surface(self.pipe_end)
        ]

    def get_height(self):
        return self.height

    def get_width(self):
        return self.pipe_end.get_width()

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def draw(self, window):
        self.x -= self.velocity  # subtract velocity from x coordinate to make the pipe move

        pos = self.get_position()
        window.blit(self.pipe_mid, pos)
        window.blit(self.pipe_end, pos)
