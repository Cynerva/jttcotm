import os
import sys
import random
import shutil
import math
from math import pi

import pygame
from pygame.locals import *
from Box2D import *

import states
import backgrounds
from world import World
from heightmap import heightmap_1d
from camera import Camera
from debug import draw_body


class SurfaceGenState(object):
    def __init__(self):
        self.world = World()
        self.heightmap = heightmap_1d(14)
        self.camera = Camera()
        self.x = 0
        shutil.rmtree("data/world")
        os.makedirs("data/world")

    def update(self, delta):
        raise states.StateChange(CaveGenState(self.world))
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    raise states.StateChange(states.PauseMenuState(self))

        left = self.heightmap[self.x] * 51.2
        right = self.heightmap[(self.x + 20) % 16384] * 51.2
        self.world.center = (self.x / 10.0, left)
        self.world.update(0.0)
        body = self.world.b2world.CreateStaticBody(
            shapes=b2PolygonShape(vertices=(
                (self.x / 10.0, left),
                (self.x / 10.0 + 2.0, right),
                (self.x / 10.0 + 2.0, right + 200.0),
                (self.x / 10.0, right + 200.0)
            )
        ))
        self.world.carve(body)
        self.world.b2world.DestroyBody(body)

        self.camera.pos = self.world.center

        self.x += 5
        if self.x > len(self.heightmap) - 5:
            self.world.unload()
            raise states.StateChange(CaveGenState(self.world))

    def render(self, screen):
        self.world.render(screen, self.camera)


class CaveGenState(object):
    def __init__(self, world):
        self.world = world
        self.camera = Camera(tracking=self)
        self.pos = (0.0, 52)
        self.angle = -pi / 2.0
        self.vel_angle = 0.0
        self.heightmap = heightmap_1d(14, mul=0.75)
        self.x = 0

    def update(self, delta):
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    raise states.StateChange(states.PauseMenuState(self))

        cos = math.cos(self.angle)
        sin = math.sin(self.angle)

        width = (self.heightmap[self.x] + 1.0) * 8.0 + 2.0
        vertices = [
            (self.pos[0] - sin * width, self.pos[1] + cos * width),
            (self.pos[0] + sin * width, self.pos[1] - cos * width)
        ]

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
            self.pos[0] + cos,
            self.pos[1] + sin
        )
        self.world.center = self.pos
        self.world.update(0.0)
        self.x = (self.x + 1) % len(self.heightmap)

        width = (self.heightmap[self.x] + 1.0) * 8.0 + 2.0
        vertices += [
            (
                self.pos[0] + sin * width + cos/2,
                self.pos[1] - cos * width + sin/2
            ),
            (
                self.pos[0] - sin * width + cos/2,
                self.pos[1] + cos * width + sin/2
            )
        ]

        body = self.world.b2world.CreateStaticBody(
            shapes=b2PolygonShape(vertices=vertices)
        )
        self.world.carve(body)
        self.world.b2world.DestroyBody(body)

        self.camera.update(delta)

    def render(self, screen):
        self.world.render(screen, self.camera)
