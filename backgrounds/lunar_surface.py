import pygame
import random

from config import screen_size, screen_width, screen_height
from starfield import Starfield
from heightmap import heightmap_1d


class LunarSurface(object):
    def __init__(self, depth=3):
        self.textures = []
        mul = 0.125 / 2.0
        for _ in range(depth):
            texture = pygame.Surface(
                (512, screen_height),
                flags=pygame.SRCALPHA
            )
            heightmap = heightmap_1d(9)
            for x in range(512):
                min_y = int((heightmap[x] * mul + 1.0) / 2.0 * screen_height)
                for y in range(min_y, screen_height):
                    noise = random.uniform(0.9, 1.0)
                    color = tuple(255.0 * noise * mul for _ in range(3))
                    texture.set_at((x, y), color)
                texture.set_at((x, min_y), (0, 0, 0))
            self.textures.append(texture)
            mul *= 2

    def update(self, delta):
        pass

    def render(self, screen, camera):
        mul = 0.125
        for texture in self.textures:
            x = int(-camera.x * mul) % 512
            y = camera.y * mul
            screen.blit(texture, (x, y))
            screen.blit(texture, (x - 512, y))
            mul *= 2
