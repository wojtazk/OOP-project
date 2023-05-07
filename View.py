import pygame


class View:
    def __init__(self, width, height, flags, caption, icon, alpha=None):
        self.window = pygame.display.set_mode((width, height), flags)

        pygame.display.set_caption(caption)

        icon_converted = icon.convert_alpha()
        pygame.display.set_icon(icon_converted)

        self.window.set_alpha(alpha)

    def get_window(self):
        return self.window
