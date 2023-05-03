import pygame
from pygame.locals import DOUBLEBUF  # flag to enable double buffering

from models.Bird import Bird
from models.LowerPipe import LowerPipe
from models.UpperPipe import UpperPipe


class Controller:
    def __init__(self):
        # config
        self.WIDTH = 1280 / 1.3
        self.HEIGHT = 720 / 1.3

        self.FPS_LIMIT = 60
        # make the gameplay consistent regardless of the resolution
        self.GRAVITY = self.HEIGHT / 720
        self.X_GRAVITY = self.WIDTH / 1280

        self.GAME_ICON = pygame.image.load('images/duck-ga9276d9c3_640.png')
        self.BG_IMG = pygame.image.load('images/Mountains_Loopable_56x31.png')
        self.BG_COLOR = 'lightblue'

        self.PLAYER_CHARACTER = None

        self.counter = 0
        self.running = False

    def play(self):
        pygame.init()
        screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), DOUBLEBUF)

        # performance improvements
        screen.set_alpha(None)  # turn off alpha, it is not needed
        self.BG_IMG = self.BG_IMG.convert_alpha()  # convert bg
        self.GAME_ICON = self.GAME_ICON.convert_alpha()

        # set window caption and icon
        pygame.display.set_caption("Bird Jumper")
        pygame.display.set_icon(self.GAME_ICON)

        # game clock
        clock = pygame.time.Clock()
        dt = 0  # delta time

        # player character
        self.PLAYER_CHARACTER = Bird(screen.get_width() / 4, screen.get_height() / 4, self.GRAVITY)

        # pipes
        test_pipe = LowerPipe(self.WIDTH - 400, self.HEIGHT, self.X_GRAVITY, 200)
        test_pipe2 = LowerPipe(self.WIDTH, self.HEIGHT, self.X_GRAVITY, 250)
        test_pipe3 = LowerPipe(self.WIDTH + 400, self.HEIGHT, self.X_GRAVITY, 200)
        test_pipe4 = LowerPipe(self.WIDTH + 800, self.HEIGHT, self.X_GRAVITY, 450)

        test_pipe_upper = UpperPipe(self.WIDTH - 400, 0, self.X_GRAVITY, 200)
        test_pipe_upper2 = UpperPipe(self.WIDTH, 0, self.X_GRAVITY, 300)
        test_pipe_upper3 = UpperPipe(self.WIDTH + 400, 0, self.X_GRAVITY, 350)
        test_pipe_upper4 = UpperPipe(self.WIDTH + 800, 0, self.X_GRAVITY, 100)

        self.running = True
        while self.running:
            # events
            # pygame.QUIT event => the user clicked X
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    # on [space, w, arrow_up] press -> jump
                    if event.key in [pygame.K_SPACE, pygame.K_UP, pygame.K_w]:
                        self.PLAYER_CHARACTER.jump()

            # background
            background = pygame.transform.scale(self.BG_IMG, (self.WIDTH, self.HEIGHT))
            screen.fill(self.BG_COLOR)
            screen.blit(background, (0, 0))

            # increment counter on every tick
            self.counter += 1
            # reset counter if it exceeds FPS_LIMIT
            if self.counter > self.FPS_LIMIT:
                self.counter = 0

            # bird animation
            self.PLAYER_CHARACTER.animate_wings(self.counter)

            # render bird
            self.PLAYER_CHARACTER.draw(screen)

            # render Pipes
            test_pipe.draw(screen)
            test_pipe2.draw(screen)
            test_pipe3.draw(screen)
            test_pipe4.draw(screen)

            test_pipe_upper.draw(screen)
            test_pipe_upper2.draw(screen)
            test_pipe_upper3.draw(screen)
            test_pipe_upper4.draw(screen)

            # keys = pygame.key.get_pressed()
            # if keys[pygame.K_w]:
            #     self.player_pos.y -= 500 * dt
            # if keys[pygame.K_s]:
            #     self.player_pos.y += 500 * dt
            # if keys[pygame.K_a]:
            #     self.player_pos.x -= 500 * dt
            # if keys[pygame.K_d]:
            #     self.player_pos.x += 500 * dt

            # limit FPS
            # dt is delta time in seconds since last frame, used for frame-rate-independent physics.
            dt = clock.tick(self.FPS_LIMIT) / 1000  # divide by 1000 to convert to seconds

            # update the display
            pygame.display.update()

        pygame.quit()
