import pygame
#from pygame.locals import *
from time import time


class Game(object):
    def __init__(self):
        from camera import Camera
        from backgrounds import Starfield, LunarSurface
        self.starfield = Starfield()
        self.lunar_surface = LunarSurface()
        self.camera = Camera()

    def update(self, delta):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.camera.y += delta * 100.0
        if keys[pygame.K_a]:
            self.camera.x -= delta * 100.0
        if keys[pygame.K_s]:
            self.camera.y -= delta * 100.0
        if keys[pygame.K_d]:
            self.camera.x += delta * 100.0
        self.starfield.update(delta)
        self.lunar_surface.update(delta)
        pygame.event.pump()

    def render(self, screen):
        self.starfield.render(screen, self.camera)
        self.lunar_surface.render(screen, self.camera)
