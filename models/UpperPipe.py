from models.Pipe import Pipe


class UpperPipe(Pipe):
    def __init__(self, x, y, gravity, height, pipe_mid, pipe_end):
        super().__init__(x, y, gravity, height, pipe_mid, pipe_end)

        # adjust the pipe_end drawing pos (make it render on the bottom of the pipe)
        self.pipe_end_y = self.y + height - self.pipe_end.get_height()

    def draw(self, window):
        self.x -= self.velocity  # subtract velocity from x coordinate to make the pipe move

        window.blit(self.pipe_mid, self.get_position())
        window.blit(self.pipe_end, (self.x, self.pipe_end_y))
