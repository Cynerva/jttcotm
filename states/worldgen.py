import pygame
from pygame.locals import *
from Box2D import *
import random

import backgrounds
from world import World
from camera import Camera
from debug import draw_body


class WorldGenState(object):
    def __init__(self):
        self.background = backgrounds.LunarSurface()
        self.world = World()
        self.camera = Camera((0.0, 0.0))
        self.body = self.world.b2world.CreateStaticBody(
            shapes = b2PolygonShape(box=(25, 25))
        )

    def update(self, delta):
        pygame.event.pump() # TODO: remove this

        keys = pygame.key.get_pressed()
        if keys[K_w]:
            self.camera.pos = (self.camera.pos[0], self.camera.pos[1] + 10)
        if keys[K_a]:
            self.camera.pos = (self.camera.pos[0] - 10, self.camera.pos[1])
        if keys[K_s]:
            self.camera.pos = (self.camera.pos[0], self.camera.pos[1] - 10)
        if keys[K_d]:
            self.camera.pos = (self.camera.pos[0] + 10, self.camera.pos[1])

        self.world.center = self.camera.pos
        self.body.position = self.camera.pos
        self.body.angle = random.uniform(0.0, 3.1415926*2.0)
        self.world.carve(self.body)

        self.background.update(delta)
        self.world.update(delta)

    def render(self, screen):
        self.background.render(screen, self.camera)
        self.world.render(screen, self.camera)
        draw_body(self.body, screen, self.camera)
