import math
import random
import pygame
from Box2D import *

import backgrounds
from camera import Camera
from player import Player
from heightmap import heightmap_1d
from config import screen_height
from debug import draw_body


class LunarSurface(object):
    def __init__(self):
        """ Good god what is this even """
        self.background = backgrounds.LunarSurface()
        self.camera = Camera()
        self.world = b2World(gravity=(0, -100), doSleep=True)
 
        heightmap = heightmap_1d(12)
        for x in range(4096):
            heightmap[x] *= 128.0
        for x in range(1024, 4096):
            heightmap[x] += (((x - 2048) / 1024.0) ** 2.0 - 1.0) * 1024.0

        ground_shapes = []
        for x in range(4096/16-1):
            left = heightmap[x*16]
            right = heightmap[x*16+16]
            ground_shapes.append(b2PolygonShape(vertices=(
                (x * 16, left),
                (x * 16, left - 16),
                (x * 16 + 16, right - 16),
                (x * 16 + 16, right)
            )))
        self.ground = self.world.CreateStaticBody(
            position=(0, 0),
            shapes=ground_shapes
        )

        self.player = Player(self.world, (0, 500))

    def update(self, delta):
        pygame.event.pump() # TODO: remove this
        self.background.update(delta)
        self.world.Step(delta, 8, 8)
        self.world.ClearForces()
        self.player.update(delta)
        self.camera.x, self.camera.y = self.player.pos

    def render(self, screen):
        self.background.render(screen, self.camera)
        self.player.render(screen, self.camera)
        draw_body(self.ground, screen, self.camera)
