import math
import pygame
from Box2D import *

import backgrounds
from camera import Camera
from player import Player
from heightmap import heightmap_1d
from debug import draw_body


class LunarSurface(object):
    def __init__(self):
        self.background = backgrounds.LunarSurface()
        self.camera = Camera()
        self.world = b2World(gravity=(0, -100), doSleep=True)
 
        heightmap = heightmap_1d(8)
        ground_shapes = []
        heightmap[0] *= 128.0
        heightmap[0] += 256.0
        for x in range(1, 256):
            heightmap[x] *= 128.0
            heightmap[x] += (((x - 128.0) / 128.0) ** 2 - 1.0) * 1024.0 + 256.0
            left = heightmap[x - 1]
            right = heightmap[x]
            ground_shapes.append(b2PolygonShape(
                vertices=(
                    (x*10-10, left),
                    (x*10-10, left-20),
                    (x*10, right-20),
                    (x*10, right)
                )
            ))
        self.ground = self.world.CreateStaticBody(
            position=(0, 0),
            shapes=ground_shapes
        )

        self.player = Player(self.world, (0, 500))

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
