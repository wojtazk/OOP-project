import pygame


class Bird:
    def __init__(self, x, y, gravity):
        # set birds position
        self.x = x
        self.y = y

        # set the gravity constant
        self.GRAVITY = gravity

        # initialize bird
        self.bird = None  # (the latest rendered frame)
        self.bird_rotation = None

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

    def get_mask(self):
        return pygame.mask.from_surface(self.bird)

    def jump(self):
        self.is_jumping = True
        self.velocity = self.JUMP_VELOCITY  # set the velocity to jump height so the bird goes up (positive velocity)
        self.rotation_multiplier = 2.8  # it will make the bird rotate more, while jumping

    def draw(self, window):
        self.bird = self.SPRITE[self.animation_frame]
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
        self.bird_rotation = self.velocity * self.rotation_multiplier  # calculate bird's rotation
        self.bird = pygame.transform.rotate(self.bird, self.bird_rotation)

        # draw the bird on the window
        window.blit(self.bird, self.get_position())

    def draw_static(self, window):  # -> when game is paused
        window.blit(self.SPRITE[self.animation_frame], self.get_position())

    def animate_wings(self, counter):
        if counter % self.ANIMATION_UPDATE_FREQUENCY == 0:
            self.animation_frame += 1
        if self.animation_frame >= len(self.SPRITE):
            self.animation_frame = 0

    def check_for_collision(self, pipe):
        if not self.bird or not pipe:  # guard clause
            return False

        pipe_pos_dict = pipe.get_positions()  # {'upper_pipe': <Vector2(x, y)>, 'lower_pipe': <Vector2(x, y)>}
        pipe_mask_dict = pipe.get_masks()  # {'upper_pipe': [<Mask(pipe_mid)>, <Mask(pipe_end)>], 'lower_pipe': ...]}

        upper_pipe_pos = pipe_pos_dict['upper_pipe']  # <Vector2(x, y)>
        upper_pipe_mask = pipe_mask_dict['upper_pipe']  # [<Mask(pipe_mid)>, <Mask(pipe_end)>]

        lower_pipe_pos = pipe_pos_dict['lower_pipe']
        lower_pipe_mask = pipe_mask_dict['lower_pipe']

        bird_pos = self.get_position()
        bird_mask = self.get_mask()

        # check for collisions with upper pipe
        offset = (upper_pipe_pos.x - bird_pos.x, upper_pipe_pos.y - bird_pos.y)  # offset between pipe's part and bird
        if bird_mask.overlap(upper_pipe_mask[0], offset):
            return True  # collision
        if bird_mask.overlap(upper_pipe_mask[1], offset):
            return True

        # check for collisions with lower pipe
        offset = (lower_pipe_pos.x - bird_pos.x, lower_pipe_pos.y - bird_pos.y)
        if bird_mask.overlap(lower_pipe_mask[0], offset):
            return True
        if bird_mask.overlap(lower_pipe_mask[1], offset):
            return True

        return False  # no collisions

    def is_out_of_bounds(self, window_height):
        bird_height = self.SPRITE[0].get_height() + 100

        lower_boundary = window_height - bird_height - 200
        upper_boundary = 0 - bird_height - 50

        return self.y > lower_boundary or self.y < upper_boundary
