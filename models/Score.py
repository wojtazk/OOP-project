import pygame.font


class Score:
    def __init__(self, font_size, margin):
        self.margin = margin
        self.value = 0
        self.font = pygame.font.Font('fonts/PressStart2P/PressStart2P-Regular.ttf', font_size)
        self.score_surface = None

    def draw(self, window):
        self.score_surface = self.font.render(str(self.value), True, 'black')

        pos = (window.get_width() - self.score_surface.get_width() - self.margin, 0 + self.margin)
        window.blit(self.score_surface, pos)

    def increment(self):
        self.value += 1

    def get_score(self):
        return self.value

    def reset(self):
        self.value = 0
