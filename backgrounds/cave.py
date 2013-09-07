import random
import pygame
from pygame.locals import *

from lunar_surface import LunarSurface
from heightmap import heightmap_1d


class Cave(object):
    def __init__(self):
        self.lunarsurface = LunarSurface()
        self.texture = pygame.Surface((512, 512))
        self.surface = pygame.Surface((512, 512))
        self.surface.set_colorkey((255, 0, 255))
        self.surface.fill((255, 0, 255))
        heightmap = heightmap_1d(9)
        for x in range(512):
            height = int((heightmap[x] + 1.0) * 256 + 0)
            for y in range(512):
                a = random.uniform(16.0, 32.0)
                self.texture.set_at((x, y), (a, a, a))
            for y in range(512 - height, 512):
                a = random.uniform(16.0, 32.0)
                self.surface.set_at((x, y), (a, a, a))


    def update(self, delta):
        self.lunarsurface.update(delta)

    def render(self, screen, camera):
        self.lunarsurface.render(screen, camera)
        chunk_pos = (int(camera.pos[0] / 51.2), int(camera.pos[1] / 51.2))
        chunk_pos = (
            chunk_pos[0] - 1 if camera.pos[0] < 0.0 else chunk_pos[0],
            chunk_pos[1] if camera.pos[1] < 0.0 else chunk_pos[1] + 1,
        )

        for y in range(-1, 2):
            for x in range(-1, 2):
                pos = (
                    (chunk_pos[0] + x) * 51.2,
                    (chunk_pos[1] + y) * 51.2
                )
                if (chunk_pos[1] + y) < 0:
                    screen.blit(self.texture, camera.screen_pos(pos))
                elif (chunk_pos[1] + y) == 0:
                    screen.blit(self.surface, camera.screen_pos(pos))
