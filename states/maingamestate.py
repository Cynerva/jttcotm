import math
import random
import pygame
from Box2D import *

import backgrounds
from camera import Camera
from player import Player
from world import World


class MainGameState(object):
    def __init__(self):
        """ Good god what is this even """
        self.background = backgrounds.LunarSurface()
        self.camera = Camera()
        self.world = World()
        self.player = Player(self.world)

    def update(self, delta):
        pygame.event.pump() # TODO: remove this
        self.background.update(delta)
        self.world.update(delta)
        self.player.update(delta)
        self.camera.x, self.camera.y = self.player.pos

    def render(self, screen):
        self.background.render(screen, self.camera)
        self.player.render(screen, self.camera)
        self.world.render(screen, self.camera)
