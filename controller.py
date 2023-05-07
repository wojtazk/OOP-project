import pygame
from pygame.locals import DOUBLEBUF  # flag to enable double buffering

from models.Bird import Bird
from models.Pipe import Pipe


class Controller:
    def __init__(self):
        # config
        self.WIDTH = 1280 / 1.3
        self.HEIGHT = 720 / 1.3

        self.FPS_LIMIT = 60

        # make the gameplay consistent regardless of the resolution
        self.GRAVITY = 1
        self.X_GRAVITY = 1

        self.GAME_ICON = pygame.image.load('images/duck-ga9276d9c3_640.png')
        # noinspection SpellCheckingInspection
        self.BG_IMG = pygame.image.load('images/Mountains_Loopable_56x31.png')
        self.background = None
        self.BG_COLOR = 'lightblue'

        self.PLAYER_CHARACTER = None
        self.PIPES_ARRAY = None
        self.last_pipe = None

        self.PIPE_GAP = 250
        self.PIPE_SPACING = 300
        self.pipe_total_width = None

        self.counter = 0
        self.running = False
        self.is_paused = True
        self.game_over = False

    def play(self):
        pygame.init()
        window = pygame.display.set_mode((self.WIDTH, self.HEIGHT), DOUBLEBUF)

        # performance improvements
        window.set_alpha(None)  # turn off alpha, it is not needed
        self.BG_IMG = self.BG_IMG.convert_alpha()  # convert bg
        self.GAME_ICON = self.GAME_ICON.convert_alpha()

        # set window caption and icon
        pygame.display.set_caption("Bird Jumper")
        pygame.display.set_icon(self.GAME_ICON)

        # game clock
        clock = pygame.time.Clock()
        # noinspection PyUnusedLocal
        dt = 0  # delta time

        # initialize player_character, pipes and background
        self.initialize_assets()

        self.running = True
        while self.running:
            # events (keyboard / mouse inputs)
            self.handle_events()

            # if game over -> continue
            if self.game_over:
                continue

            # background
            window.fill(self.BG_COLOR)
            window.blit(self.background, (0, 0))

            # continue if the game is paused
            if self.is_paused:
                self.PLAYER_CHARACTER.draw_static(window)
                pygame.display.update()
                continue

            # increment counter on every tick
            self.increment_counter()

            # bird animation
            self.PLAYER_CHARACTER.animate_wings(self.counter)

            # render bird
            self.PLAYER_CHARACTER.draw(window)

            # render Pipes
            for pipe in self.PIPES_ARRAY:
                if pipe.is_visible():
                    pipe.draw(window)
                else:
                    pipe.recycle(self.last_pipe.get_x() + self.pipe_total_width)
                    self.last_pipe = pipe

                # checking for collisions with player_character
                if self.PLAYER_CHARACTER.check_for_collision(pipe):
                    # print warning to the console
                    print("\033[91m {}\033[00m".format(f'collision {pipe.get_positions()}'))
                    print()
                    self.restart()

            # limit FPS
            # dt is delta time in seconds since last frame, used for frame-rate-independent physics.
            # dt = clock.tick(self.FPS_LIMIT) / 1000  # divide by 1000 to convert to seconds
            clock.tick(self.FPS_LIMIT)  # set tick

            # update the display
            pygame.display.update()

        pygame.quit()

    def restart(self):
        # self.is_paused = True
        self.game_over = True
        self.counter = 0
        self.initialize_assets()

    @staticmethod
    def quit():
        if pygame.get_init():  # True if pygame is currently initialized
            pygame.quit()

        quit()

    def initialize_assets(self):
        # background
        self.background = pygame.transform.scale(self.BG_IMG, (self.WIDTH, self.HEIGHT))

        # player character
        self.PLAYER_CHARACTER = Bird(self.WIDTH / 4, self.HEIGHT / 4, self.GRAVITY)

        # pipes setup
        self.PIPES_ARRAY = self.generate_pipes()
        self.last_pipe = self.PIPES_ARRAY[-1]

    def handle_events(self):
        # pygame.QUIT event => the user clicked X
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.quit()
                return

            if event.type == pygame.KEYDOWN:
                # on [space, w, arrow_up] press -> jump
                if event.key in [pygame.K_SPACE, pygame.K_UP, pygame.K_w]:
                    self.PLAYER_CHARACTER.jump()

                    if self.is_paused or self.game_over:
                        self.is_paused = False
                        self.game_over = False
                    return

                # quit the game on escape key press
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    self.quit()
                    return

            if event.type == pygame.MOUSEBUTTONDOWN:
                # on mouse left click -> jump
                if event.button == pygame.BUTTON_LEFT:
                    self.PLAYER_CHARACTER.jump()

                    if self.is_paused or self.game_over:
                        self.is_paused = False
                        self.game_over = False
                    return

    def increment_counter(self):
        self.counter += 1
        # reset counter if it exceeds FPS_LIMIT
        if self.counter > self.FPS_LIMIT:
            self.counter = 0

    def generate_pipes(self):
        pipe_width = Pipe(0, 1000, 0, 0).get_width()
        pipe_total_width = pipe_width + self.PIPE_SPACING

        self.pipe_total_width = pipe_total_width

        pipes_needed = int(self.WIDTH // pipe_total_width) + 1  # + 1 for extra pipe

        pipes = []
        new_pipe_position = self.WIDTH
        for i in range(pipes_needed):
            new_pipe = Pipe(new_pipe_position, self.HEIGHT, self.PIPE_GAP, self.X_GRAVITY)
            new_pipe_position += pipe_total_width

            pipes.append(new_pipe)

        return pipes
