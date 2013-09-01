import pygame
from Box2D import *

import backgrounds
from camera import Camera
from player import Player
from debug import draw_body


class LunarSurface(object):
    def __init__(self):
        self.background = backgrounds.LunarSurface()
        self.camera = Camera()

        self.world = b2World(gravity=(0, -100), doSleep=True)
        self.ground = self.world.CreateStaticBody(
            position=(0, -125),
            shapes=b2PolygonShape(box=(190, 20))
        )
        self.player = Player(self.world)

    def update(self, delta):
        self.background.update(delta)
        self.world.Step(delta, 6, 2)
        self.world.ClearForces()
        self.player.update(delta)

    def render(self, screen):
        self.background.render(screen, self.camera)
        draw_body(self.ground, screen, self.camera)
        self.player.render(screen, self.camera)
