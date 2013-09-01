import pygame
from time import time


class Game(object):
    def update(self, delta):
        pass

    def render(self, screen):
        pygame.draw.line(screen, (64, 0, 128), (0, 0), (400, 300))
        pass
