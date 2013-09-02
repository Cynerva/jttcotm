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

        self.texture = pygame.Surface(
            (4096, 512),
            flags=pygame.SRCALPHA
        )
        for x in range(4096):
            top = int(256.0 - heightmap[x])
            for y in range(top, 512):
                a = random.uniform(192.0*0.9, 192.0)
                self.texture.set_at((x, y), (a, a, a))
            self.texture.set_at((x, top), (0, 0, 0))
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
        pos = self.camera.screen_pos(0, 256.0)
        screen.blit(self.texture, pos)
