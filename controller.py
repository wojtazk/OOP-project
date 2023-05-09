import pygame
import sys
from pygame.locals import DOUBLEBUF  # flag to enable double buffering

from View import View
from models.Bird import Bird
from models.PipeGenerator import PipeGenerator
from models.Score import Score


class Controller:
    def __init__(self):
        # config
        self.WIDTH = 1280 / 1.3
        self.HEIGHT = 720 / 1.3

        self.FPS_LIMIT = 60

        # gravity
        self.GRAVITY = 1
        self.X_GRAVITY = 1

        self.CAPTION = "Bird Jumper"
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

        self.SCORE = None
        self.SCORE_FONT_SIZE = 30
        self.SCORE_MARGIN = 15

        self.counter = 0
        self.running = False
        self.is_paused = True
        self.game_over = False

    def play(self):
        pygame.init()

        # initialize view
        flags = DOUBLEBUF
        view = View(self.WIDTH, self.HEIGHT, flags, self.CAPTION, self.GAME_ICON, None)
        window = view.get_window()  # get window

        self.BG_IMG = self.BG_IMG.convert_alpha()  # convert bg

        # game clock
        clock = pygame.time.Clock()
        # noinspection PyUnusedLocal
        dt = 0  # delta time

        # initialize player_character, pipes and background
        self.initialize_assets()
        self.SCORE = Score(self.SCORE_FONT_SIZE, self.SCORE_MARGIN)

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

                    # increment score
                    # self.SCORE.increment()
                    # noinspection PyStatementEffect
                    self.SCORE + 1

                # checking for collisions with player_character
                if self.PLAYER_CHARACTER.check_for_collision(pipe):
                    # print warning to the console
                    print("\033[91m {}\033[00m".format(f'collision {pipe.get_positions()}'))
                    print("\033[94m {}\033[00m".format(f'your score: {self.SCORE.get_score()}'))
                    print()
                    self.restart()

            # restart if the bird is out of screen
            if self.PLAYER_CHARACTER.is_out_of_bounds(self.WIDTH):
                self.restart()

            # render score
            self.SCORE.draw(window)

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

        sys.exit()

    def initialize_assets(self):
        # background
        self.background = pygame.transform.scale(self.BG_IMG, (self.WIDTH, self.HEIGHT))

        # player character
        self.PLAYER_CHARACTER = Bird(self.WIDTH / 4, self.HEIGHT / 4, self.GRAVITY)

        # pipes setup
        self.PIPES_ARRAY = self.generate_pipes()
        self.last_pipe = self.PIPES_ARRAY[-1]

        # score
        # self.SCORE = Score(self.SCORE_FONT_SIZE, self.SCORE_MARGIN)

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

                    if self.game_over:
                        self.SCORE.reset()

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

                    if self.game_over:
                        self.SCORE.reset()

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
        pipe_width = PipeGenerator(0, 1000, 0, 0).get_width()
        pipe_total_width = pipe_width + self.PIPE_SPACING

        self.pipe_total_width = pipe_total_width

        pipes_needed = int(self.WIDTH // pipe_total_width) + 1  # + 1 for extra pipe

        pipes = []
        new_pipe_position = self.WIDTH
        for i in range(pipes_needed):
            new_pipe = PipeGenerator(new_pipe_position, self.HEIGHT, self.PIPE_GAP, self.X_GRAVITY)
            new_pipe_position += pipe_total_width

            pipes.append(new_pipe)

        return pipes
