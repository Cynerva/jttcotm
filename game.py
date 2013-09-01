import pygame
from time import time


class Game(object):
    def __init__(self):
        from backgrounds import Starfield
        self.starfield = Starfield()

    def update(self, delta):
        self.starfield.update(delta)

    def render(self, screen):
        self.starfield.render(screen)
