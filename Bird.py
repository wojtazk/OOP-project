import pygame


class Bird:
    sprite = [
        pygame.image.load('images/bird/frame-1.png'),
        pygame.image.load('images/bird/frame-2.png'),
        pygame.image.load('images/bird/frame-3.png'),
        pygame.image.load('images/bird/frame-4.png'),
    ]
    animation_update_frequency = 5  # update every x frames

    def __init__(self):
        self.value = 0

