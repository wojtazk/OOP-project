import pygame


class Bird:
    def __init__(self, x, y, gravity):
        # set birds position
        self.x = x
        self.y = y

        # set the gravity constant
        self.GRAVITY = gravity

        # bird animation frames
        self.SPRITE = [
            pygame.image.load('images/bird/frame-1.png').convert_alpha(),
            pygame.image.load('images/bird/frame-2.png').convert_alpha(),
            pygame.image.load('images/bird/frame-3.png').convert_alpha(),
            pygame.image.load('images/bird/frame-4.png').convert_alpha(),
        ]
        self.scale_animation_frames()

        self.animation_frame = 0  # no. of current frame being displayed
        self.ANIMATION_UPDATE_FREQUENCY = 4  # update every x frames

        self.rotation_multiplier = 1.5

        self.is_jumping = False
        self.JUMP_VELOCITY = self.GRAVITY * 15

        self.velocity = 0

    def scale_animation_frames(self):
        i = 0
        for frame in self.SPRITE:
            self.SPRITE[i] = pygame.transform.scale(frame, (frame.get_width() / 8, frame.get_height() / 8))
            i += 1

    def get_position(self):
        return pygame.Vector2(self.x, self.y)

    def jump(self):
        self.is_jumping = True
        self.velocity = self.JUMP_VELOCITY  # set the velocity to jump height so the bird goes up (positive velocity)
        self.rotation_multiplier = 2.8  # it will make the bird rotate more, while jumping

    def draw(self, screen):
        bird = self.SPRITE[self.animation_frame]
        # bird_rec = (bird.get_width() / 8, bird.get_height() / 8)
        # bird = pygame.transform.scale(bird, bird_rec)

        if self.is_jumping:
            self.y -= self.velocity  # move the bird up
            # decrease velocity when bird gets higher
            self.velocity -= self.GRAVITY  # it's basically a parabola, +jump_velocity -> -jump_velocity
            if self.velocity < 0:  # < 0, because we don't want the bird to return to the position before jump
                self.is_jumping = False
                self.rotation_multiplier = 1.5  # return to the initial value
        else:
            self.y -= self.velocity  # subtract velocity from y coordinate to make the bird fall
            self.velocity -= self.GRAVITY  # decrease velocity by gravity constant

        # rotate the bird based on its velocity (jumping & falling)
        bird = pygame.transform.rotate(bird, self.velocity * self.rotation_multiplier)
        screen.blit(bird, self.get_position())

    def animate_wings(self, counter):
        if counter % self.ANIMATION_UPDATE_FREQUENCY == 0:
            self.animation_frame += 1
        if self.animation_frame >= len(self.SPRITE):
            self.animation_frame = 0
