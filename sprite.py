import pygame


class Sprite(object):
    def __init__(self, filename):
        self.image = pygame.image.load(filename)
        self.image.set_colorkey((255, 0, 255))
        self.mirror = False

    def update(self, delta, mirror=False):
        self.mirror = mirror

    def render(self, screen, camera, pos):
        image = self.image
        if self.mirror:
            image = pygame.transform.flip(self.image, True, False)
        pos = camera.screen_pos(pos)
        pos = (
            pos[0] - self.image.get_width() / 2,
            pos[1] - self.image.get_height() / 2
        )
        screen.blit(image, pos)


class Animation(object):
    def __init__(self, sprites):
        self.sprites = sprites
        self.index = 0
        self.time = 0.0

    def update(self, delta, mirror=False):
        self.time += delta
        while self.time > 1.0:
            self.index = (self.index + 1) % len(self.sprites)
            self.time -= 1.0
        self.sprites[self.index].update(delta, mirror)

    def render(self, screen, camera, pos):
        self.sprites[self.index].render(screen, camera, pos)
