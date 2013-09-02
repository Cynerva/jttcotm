import pygame
from pygame.locals import *
from Box2D import *


class Chunk(object):
    def __init__(self, chunk_pos):
        self.texture = pygame.Surface(
            (512, 512),
            flags=SRCALPHA
        )
        self.pos = (chunk_pos[0] * 512, chunk_pos[1] * 512)

        # placeholder texture
        pygame.draw.line(self.texture, (255, 0, 0), (0, 0), (512, 512))
        pygame.draw.line(self.texture, (0, 255, 0), (0, 0), (0, 512))
        pygame.draw.line(self.texture, (0, 255, 0), (0, 0), (512, 0))
        pygame.draw.line(self.texture, (0, 255, 0), (512, 512), (0, 512))
        pygame.draw.line(self.texture, (0, 255, 0), (512, 512), (512, 0))

    def render(self, screen, camera):
        pos = camera.screen_pos(*self.pos)
        screen.blit(self.texture, pos)


class World(object):
    def __init__(self):
        self.b2world = b2World(gravity=(0, -100), doSleep=True)
        self.center = (0, 0)
        self.center_chunk = None
        self.chunks = {}

    def update(self, delta):
        center_chunk = (int(self.center[0] / 512), int(self.center[1] / 512))
        center_chunk = (
            center_chunk[0] - 1 if self.center[0] < 0.0 else center_chunk[0],
            center_chunk[1] if self.center[1] < 0.0 else center_chunk[1] + 1
        )
        if center_chunk != self.center_chunk:
            self.center_chunk = center_chunk
            self.chunks[center_chunk] = Chunk(center_chunk)

        self.b2world.Step(delta, 8, 8)
        self.b2world.ClearForces()

    def render(self, screen, camera):
        for chunk in self.chunks.values():
            chunk.render(screen, camera)
