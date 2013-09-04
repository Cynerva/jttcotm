import random
import shutil
from math import sin, cos, pi

import pygame
from pygame.locals import *
from Box2D import *

import backgrounds
from world import World
from heightmap import heightmap_1d
from camera import Camera
from states import StateChange
from debug import draw_body


class WorldGenState(object):
    def __init__(self):
        #self.state = SurfaceGenState()
        self.state = CaveGenState()

    def update(self, delta):
        pygame.event.pump() # TODO: remove this
        try:
            self.state.update(delta)
        except StateChange as change:
            self.state = change.state

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
        self.texture.fill((0, 0, 0, 0))

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
            self.world.unload()
            raise StateChange(CaveGenState())

    def render(self, screen):
        self.world.render(screen, self.camera)
        draw_body(self.body, screen, self.camera)


class CaveGenState(object):
    def __init__(self):
        self.world = World()
        self.camera = Camera(tracking=self)
        self.pos = (0.0, 52)
        self.angle = -pi / 2.0
        self.vel_angle = 0.0
        self.heightmap = heightmap_1d(10)
        self.x = 1000

    def update(self, delta):
        if self.pos[1] > -50.0 or self.angle > pi/4 or self.angle < -3*pi/4:
            self.vel_angle = -self.angle - pi / 2.0
        else:
            self.vel_angle += random.uniform(-0.001, 0.001)
        self.vel_angle = max(-0.01, min(0.01, self.vel_angle))

        self.angle += self.vel_angle
        if self.angle > pi / 2.0:
            self.angle -= 2.0 * pi
        if self.angle < -pi * 3.0 / 2.0:
            self.angle += 2.0 * pi

        self.pos = (
            self.pos[0] + cos(self.angle) / 4.0,
            self.pos[1] + sin(self.angle) / 4.0
        )
        self.world.center = self.pos
        self.world.update(0.0)

        size = (self.heightmap[self.x % len(self.heightmap)] + 1.0) * 4.0 + 2.0
        body = self.world.b2world.CreateStaticBody(
            position=self.pos,
            shapes=b2PolygonShape(box=(0.5, size))
        )
        body.angle = self.angle
        self.world.carve(body)
        self.world.b2world.DestroyBody(body)

        texture = pygame.Surface((10.0, size*20), flags=SRCALPHA)
        texture.fill((255, 255, 255, 255))
        texture = pygame.transform.rotate(texture, self.angle * 180.0 / pi)
        for y in range(texture.get_height()):
            for x in range(texture.get_width()):
                color = texture.get_at((x, y))
                if color == (255, 255, 255, 255):
                    texture.set_at((x, y), (0, 0, 0, 0))
                else:
                    texture.set_at((x, y), (255, 255, 255, 255))
        self.world.blit(texture, self.pos, special_flags=BLEND_RGBA_MIN)

        self.camera.update(delta)

        self.x -= 1
        if self.x == 0:
            self.world.unload()
            raise StateDone

    def render(self, screen):
        self.world.render(screen, self.camera)
