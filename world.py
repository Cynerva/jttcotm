import os
import random
from copy import deepcopy

import pygame
from pygame.locals import *
from Box2D import *
from Polygon import Polygon
from debug import draw_body


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
        self.texture = None
        self.polygon = None
        self.body = None

        texture_filename = "data/world/%i_%i.tga" % self.chunk_pos
        if os.path.exists(texture_filename):
            self.texture = pygame.image.load(texture_filename)
        elif chunk_pos[1] <= 0:
            self.texture = Chunk.underground_texture
            self.polygon = Polygon((
                (-256, -256), 
                (-256, 256), 
                (256, 256), 
                (256, -256) 
            ))

        self.load_body()

    def load_body(self):
        if self.body:
            self.world.b2world.DestroyBody(self.body)
        if not self.polygon:
            return

        shapes = []
        for strip in self.polygon.triStrip():
            for i in range(len(strip) - 2):
                shapes.append(b2PolygonShape(
                    vertices=strip[i:i+3]
                ))
            shapes.append(b2PolygonShape(
                vertices=strip[-2:] + strip[:1]
            ))
            shapes.append(b2PolygonShape(
                vertices=strip[-1:] + strip[:2]
            ))

        self.body = self.world.b2world.CreateStaticBody(
            position=(self.pos[0] + 256, self.pos[1] - 256),
            shapes=shapes
        )

    def render(self, screen, camera):
        pos = camera.screen_pos(self.pos)
        if self.texture:
            screen.blit(self.texture, pos)
        if self.body:
            draw_body(self.body, screen, camera)
        screen.set_at(camera.screen_pos(self.pos), (255, 0, 0))

    def save(self):
        pygame.image.save(self.texture, "data/world/%i_%i.tga" % self.chunk_pos)

    def unload(self):
        pass

    def carve(self, body):
        if not self.polygon:
            return
        for fixture in body.fixtures:
            shape = fixture.shape
            vertices = [tuple(body.transform * x) for x in shape.vertices]
            vertices = [(x - self.pos[0] - 256, y - self.pos[1] + 256) for (x, y) in vertices]
            polygon = Polygon(vertices)
            self.polygon -= polygon
        self.load_body()
                
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

    def carve(self, body):
        for chunk in self.chunks.values():
            chunk.carve(body)
