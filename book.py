import pygame
from math import sin


class Book(object):
    font = None
    texture = None

    def __init__(self, text, pos):
        self.text = text
        self.pos = pos
        self.start_time = None
        self.time = 0.0

    def update(self, delta, pos):
        self.time += delta
        distance = abs(pos[0] - self.pos[0]) + abs(pos[1] - self.pos[1])
        if not self.start_time and distance < 5.0:
            self.start_time = self.time

    def render(self, screen, camera):
        if not Book.texture:
            Book.texture = pygame.image.load("data/art/book.png")
            Book.texture.set_colorkey((255, 0, 255))
        pos = (self.pos[0], self.pos[1] + sin(self.time * 8) / 2)
        pos = camera.screen_pos(pos)
        pos = (
            pos[0] - Book.texture.get_width() / 2,
            pos[1] - Book.texture.get_height() / 2
        )
        screen.blit(Book.texture, pos)

        if self.start_time:
            if not Book.font:
                Book.font = pygame.font.Font(None, 16)
            count = int((self.time - self.start_time) / 0.05)
            words = self.text[:count].split()
            lines = [""]
            for word in words:
                if len(lines[-1]) > 32:
                    lines.append(word)
                else:
                    lines[-1] += " " + word
            for i in range(len(lines)):
                texture = self.font.render(lines[i], 1, (255, 255, 255))
                pos = camera.screen_pos(self.pos)
                pos = (
                    pos[0] - texture.get_width() / 2,
                    pos[1] - texture.get_height() / 2 + i * 20 - 40
                )
                screen.blit(texture, pos)
