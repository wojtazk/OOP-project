from models.Pipe import Pipe


class LowerPipe(Pipe):
    def __init__(self, x, y, gravity, height, pipe_mid, pipe_end):
        super().__init__(x, y, gravity, height, pipe_mid, pipe_end)

        # adjust pipe's position (move it up basically)
        self.y = y - self.pipe_mid.get_height()
