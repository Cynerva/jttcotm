import os
import random
import pygame
from pygame.locals import *
from Box2D import *


try:
    os.makedirs("data/world")
except OSError:
    pass


class Chunk(object):
    underground_texture = None

    def __init__(self, world, chunk_pos):
        self.world = world
        self.chunk_pos = chunk_pos
        self.pos = (chunk_pos[0] * 512, chunk_pos[1] * 512)

        texture_filename = "data/world/%i_%i.tga" % self.chunk_pos
        if os.path.exists(texture_filename):
            self.texture = pygame.image.load(texture_filename)
        elif chunk_pos[1] <= 0:
            self.texture = Chunk.underground_texture
        else:
            self.texture = None

    def render(self, screen, camera):
        pos = camera.screen_pos(*self.pos)
        if self.texture:
            screen.blit(self.texture, pos)

    def save(self):
        pygame.image.save(self.texture, "data/world/%i_%i.tga" % self.chunk_pos)

    def unload(self):
        pass

class World(object):
    def __init__(self):
        self.b2world = b2World(gravity=(0, -100), doSleep=True)
        self.center = (0, 0)
        self.center_chunk = None
        self.chunks = {}

        Chunk.underground_texture = pygame.Surface((512, 512))
        for y in range(512):
            for x in range(512):
                a = random.uniform(128.0 * 0.9, 128.0)
                Chunk.underground_texture.set_at((x, y), (a, a, a))

    def update(self, delta):
        center_chunk = (int(self.center[0] / 512), int(self.center[1] / 512))
        center_chunk = (
            center_chunk[0] - 1 if self.center[0] < 0.0 else center_chunk[0],
            center_chunk[1] if self.center[1] < 0.0 else center_chunk[1] + 1
        )
        if center_chunk != self.center_chunk:
            self.center_chunk = center_chunk

            wanted = set()
            for x in range(-1, 2):
                for y in range(-1, 2):
                    chunk_pos = (center_chunk[0] + x, center_chunk[1] + y)
                    wanted.add((center_chunk[0] + x, center_chunk[1] + y))

            for chunk_pos, chunk in self.chunks.items():
                if not chunk_pos in wanted:
                    chunk.unload()
                    del self.chunks[chunk_pos]
            for chunk_pos in wanted:
                if not chunk_pos in self.chunks:
                    self.chunks[chunk_pos] = Chunk(self, chunk_pos)

        self.b2world.Step(delta, 8, 8)
        self.b2world.ClearForces()

    def render(self, screen, camera):
        for chunk in self.chunks.values():
            chunk.render(screen, camera)
