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
            position=(0, 0),
            shapes=b2PolygonShape(box=(190, 20, (0, 0), 0.5))
        )
        self.player = Player(self.world, (0, 200))

    def update(self, delta):
        pygame.event.pump() # TODO: remove this
        self.background.update(delta)
        self.world.Step(delta, 1, 1)
        self.world.ClearForces()
        self.player.update(delta)
        self.camera.x, self.camera.y = self.player.pos

    def render(self, screen):
        self.background.render(screen, self.camera)
        draw_body(self.ground, screen, self.camera)
        self.player.render(screen, self.camera)
