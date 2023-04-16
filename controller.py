import pygame

from models.Bird import Bird


class Controller:
    def __init__(self):
        # config
        self.WIDTH = 1280
        self.HEIGHT = 720

        self.FPS_LIMIT = 60
        self.GRAVITY = 1

        self.GAME_ICON = pygame.image.load('images/duck-ga9276d9c3_640.png')
        self.BG_IMG = pygame.image.load('images/Mountains_Loopable_56x31.png')
        self.BG_COLOR = 'lightblue'

        self.PLAYER_CHARACTER = None

        self.counter = 0
        self.running = False

    def play(self):
        pygame.init()
        screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Bird Jumper")

        pygame.display.set_icon(self.GAME_ICON)

        # game clock
        clock = pygame.time.Clock()
        dt = 0  # delta time

        self.PLAYER_CHARACTER = Bird(screen.get_width() / 4, screen.get_height() / 4, self.GRAVITY)

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
