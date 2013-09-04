import random
import shutil

import pygame
from pygame.locals import *
from Box2D import *

import backgrounds
from world import World
from heightmap import heightmap_1d
from camera import Camera
from debug import draw_body


class WorldGenState(object):
    def __init__(self):
        self.state = SurfaceGenState()

    def update(self, delta):
        pygame.event.pump() # TODO: remove this
        self.state.update(delta)

    def render(self, screen):
        self.state.render(screen)


class SurfaceGenState(object):
    def __init__(self):
        self.world = World()
        self.heightmap = heightmap_1d(14)
        self.camera = Camera()
        self.x = 0
        self.body = None
        self.texture = pygame.Surface((2, 1024), SRCALPHA)
        for y in range(1024):
            self.texture.set_at((0, y), (0, 0, 0, 0))
            self.texture.set_at((1, y), (0, 0, 0, 0))

    def update(self, delta):
        left = self.heightmap[self.x] * 51.2
        right = self.heightmap[(self.x + 20) % 16384] * 51.2
        self.world.center = (self.x / 10.0, left)
        self.world.update(delta)
        self.body = self.world.b2world.CreateStaticBody(
            shapes=b2PolygonShape(vertices=(
                (self.x / 10.0, left),
                (self.x / 10.0 + 2.0, right),
                (self.x / 10.0 + 2.0, right + 200.0),
                (self.x / 10.0, right + 200.0)
            )
        ))
        self.world.carve(self.body)

        for x in range(self.x, self.x + 20):
            height = self.heightmap[x % 16384] * 51.2 + 51.2
            self.world.blit(self.texture, (x / 10.0, height), BLEND_RGBA_MIN)

        self.world.update(delta)

        self.camera.pos = self.world.center

        self.x += 5
        if self.x > len(self.heightmap) - 5:
            self.x = 0

    def render(self, screen):
        self.world.render(screen, self.camera)
        draw_body(self.body, screen, self.camera)
