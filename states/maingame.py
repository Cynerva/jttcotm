import sys
import math
import random
import pygame
from pygame.locals import *
from Box2D import *

import backgrounds
import states
from camera import Camera
from player import Player
from world import World


class MainGameState(object):
    def __init__(self):
        self.background = backgrounds.Cave()
        self.world = World()
        self.player = Player(self.world, (0, 100.0))
        self.camera = Camera((0, 100.0), tracking=self.player)

    def update(self, delta):
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    raise states.StateChange(states.PauseMenuState(self))

        self.world.center = self.player.pos

        self.background.update(delta)
        self.world.update(delta)
        self.player.update(delta)
        self.camera.update(delta)

    def render(self, screen):
        self.background.render(screen, self.camera)
        self.world.render(screen, self.camera)
        self.player.render(screen, self.camera)
