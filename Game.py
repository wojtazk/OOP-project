import pygame
from Bird import Bird


class BirdJumper:
    # config
    WIDTH = 1280
    HEIGHT = 720

    FPS_LIMIT = 144

    GAME_ICON = pygame.image.load('images/duck-ga9276d9c3_640.png')
    BG_IMG = pygame.image.load('images/Mountains_Loopable_56x31.png')
    BG_COLOR = 'lightblue'

    GAME_CHARACTER = Bird()

    counter = 0

    def __init__(self):
        # pygame setup
        pygame.init()

        screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        pygame.display.set_caption("Bird Jumper")

        pygame.display.set_icon(self.GAME_ICON)

        clock = pygame.time.Clock()
        running = True
        dt = 0  # delta time

        player_pos = pygame.Vector2(screen.get_width() / 4, screen.get_height() / 2)

        while running:
            # events
            # pygame.QUIT event => the user clicked X
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

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
            if self.counter % self.GAME_CHARACTER.animation_update_frequency == 0:
                self.GAME_CHARACTER.value += 1
            if self.GAME_CHARACTER.value >= len(self.GAME_CHARACTER.sprite):
                self.GAME_CHARACTER.value = 0

            # render bird
            bird = self.GAME_CHARACTER.sprite[self.GAME_CHARACTER.value % len(self.GAME_CHARACTER.sprite)]
            bird_rec = (bird.get_width() / 8, bird.get_height() / 8)
            bird = pygame.transform.scale(bird, bird_rec)
            screen.blit(bird, player_pos)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                player_pos.y -= 500 * dt
            if keys[pygame.K_s]:
                player_pos.y += 500 * dt
            if keys[pygame.K_a]:
                player_pos.x -= 500 * dt
            if keys[pygame.K_d]:
                player_pos.x += 500 * dt

            # on space press -> jump
            if keys[pygame.K_SPACE]:
                player_pos.x += 10
                player_pos.y -= 10

            # limit FPS
            # dt is delta time in seconds since last frame, used for frame-rate-independent physics.
            dt = clock.tick(self.FPS_LIMIT) / 1000  # divide by 1000 to convert to seconds

            # update the display
            pygame.display.update()

        pygame.quit()
