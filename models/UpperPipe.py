from models.LowerPipe import LowerPipe


class UpperPipe(LowerPipe):
    def __init__(self, x, y, gravity, height, pipe_mid, pipe_end):
        super().__init__(x, y, gravity, height, pipe_mid, pipe_end)
        self.y = y  # reset the adjustment made in LowerPipe (it is not needed here)

        # adjust the pipe end drawing pos (make it render on the bottom of the pipe)
        self.pipe_end_y = self.y + height - self.pipe_end.get_height()

    def draw(self, screen):
        self.x -= self.velocity  # subtract velocity from x coordinate to make the pipe move

        screen.blit(self.pipe_mid, self.get_position())
        screen.blit(self.pipe_end, (self.x, self.pipe_end_y))
