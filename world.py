import os
import random
import pickle

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
        self.pos = (chunk_pos[0] * 51.2, chunk_pos[1] * 51.2)
        self.chunk_pos = (chunk_pos[0] % 32, chunk_pos[1])
        self.texture = None
        self.polygon = None
        self.body = None
        self.entities = []

        texture_filename = "data/world/%i_%i.tga" % self.chunk_pos
        if os.path.exists(texture_filename):
            self.texture = pygame.image.load(texture_filename)
            self.texture.set_colorkey((255, 0, 255))
        elif chunk_pos[1] <= 1:
            self.texture = Chunk.underground_texture

        data_filename = "data/world/%i_%i.dat" % self.chunk_pos
        if os.path.exists(data_filename):
            with open(data_filename) as fin:
                self.polygon, self.entities = pickle.load(fin)
        elif chunk_pos[1] <= 1:
            self.polygon = Polygon((
                (-25.6, -25.6), 
                (-25.6, 25.6), 
                (25.6, 25.6), 
                (25.6, -25.6) 
            ))

        self.load_body()

    def load_body(self):
        if self.body:
            self.world.b2world.DestroyBody(self.body)
            self.body = None
        if not self.polygon:
            return

        shapes = []
        for strip in self.polygon.triStrip():
            for i in range(len(strip) - 2):
                try:
                    shapes.append(b2PolygonShape(vertices=strip[i:i+3]))
                except:
                    pass

        self.body = self.world.b2world.CreateStaticBody(
            position=(self.pos[0] + 25.6, self.pos[1] - 25.6),
            shapes=shapes
        )

    def update(self, delta, pos):
        for entity in self.entities:
            entity.update(delta, pos)

    def render(self, screen, camera):
        pos = camera.screen_pos(self.pos)
        if self.texture:
            screen.blit(self.texture, pos)
        #if self.body:
        #    draw_body(self.body, screen, camera)
        for entity in self.entities:
            entity.render(screen, camera)

    def unload(self):
        if self.body:
            self.world.b2world.DestroyBody(self.body)
        if self.texture:
            pygame.image.save(
                self.texture, "data/world/%i_%i.tga" % self.chunk_pos
            )
        with open("data/world/%i_%i.dat" % self.chunk_pos, "w") as fout:
            pickle.dump((self.polygon, self.entities), fout)

    def carve(self, body):
        if not self.polygon:
            return
        if self.texture == Chunk.underground_texture:
            self.texture = Chunk.underground_texture.copy()
            self.texture.set_colorkey((255, 0, 255))
        for fixture in body.fixtures:
            shape = fixture.shape
            vertices = [tuple(body.transform * x) for x in shape.vertices]
            vertices = [
                (x - self.pos[0] - 25.6, y - self.pos[1] + 25.6)
                for (x, y) in vertices
            ]
            polygon = Polygon(vertices)
            self.polygon -= polygon
            if self.texture:
                draw_vertices = [
                    ((x + 25.6) * 10, 512 - (y + 25.6) * 10) for (x, y) in vertices
                ]
                pygame.draw.polygon(self.texture, (255, 0, 255), draw_vertices)
        self.load_body()

    def blit(self, texture, pos, special_flags=0):
        if self.texture == Chunk.underground_texture:
            self.texture = Chunk.underground_texture.copy()
            self.texture.set_colorkey((255, 0, 255))
        if self.texture:
            pos = (
                (pos[0] - self.pos[0]) * 10.0 - texture.get_width() / 2,
                (self.pos[1] - pos[1]) * 10.0 - texture.get_height() / 2
            )
            self.texture.blit(texture, pos, special_flags=special_flags)

class World(object):
    def __init__(self):
        self.b2world = b2World(gravity=(0, -10.0), doSleep=True)
        self.center = (0, 0)
        self.center_chunk = None
        self.chunks = {}

        Chunk.underground_texture = pygame.Surface((512, 512))
        Chunk.underground_texture.set_colorkey((255, 0, 255))
        for y in range(512):
            for x in range(512):
                a = random.uniform(112.0, 128.0)
                Chunk.underground_texture.set_at((x, y), (a, a, a))

    def update(self, delta):
        center_chunk = (int(self.center[0] / 51.2), int(self.center[1] / 51.2))
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

        for chunk in self.chunks.values():
            chunk.update(delta, self.center)

    def render(self, screen, camera):
        for chunk in self.chunks.values():
            chunk.render(screen, camera)

    def carve(self, body):
        for chunk in self.chunks.values():
            chunk.carve(body)

    def blit(self, texture, pos, special_flags=0):
        for chunk in self.chunks.values():
            chunk.blit(texture, pos, special_flags)

    def unload(self):
        for chunk in self.chunks.values():
            chunk.unload()
        self.chunks = {}
        self.center_chunk = None

    def add_entity(self, entity, pos):
        chunk_pos = (int(pos[0] / 51.2), int(pos[1] / 51.2))
        chunk_pos = (
            chunk_pos[0] - 1 if pos[0] < 0.0 else chunk_pos[0],
            chunk_pos[1] if pos[1] < 0.0 else chunk_pos[1] + 1
        )
        self.chunks[chunk_pos].entities.append(entity)

