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

    def update(self, delta, pos, player_pos):
        self.time += delta
        pos = (pos[0] + self.pos[0], pos[1] + self.pos[1])
        distance = abs(player_pos[0] - pos[0]) + abs(player_pos[1] - pos[1])
        if not self.start_time and distance < 5.0:
            self.start_time = self.time

    def render(self, screen, camera, pos):
        if not Book.texture:
            Book.texture = pygame.image.load("data/art/book.png")
            Book.texture.set_colorkey((255, 0, 255))
        pos = (pos[0] + self.pos[0], pos[1] + self.pos[1])
        spos = (pos[0], pos[1] + sin(self.time * 8) / 2)
        spos = camera.screen_pos(spos)
        spos = (
            spos[0] - Book.texture.get_width() / 2,
            spos[1] - Book.texture.get_height() / 2
        )
        screen.blit(Book.texture, spos)

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
                spos = camera.screen_pos(pos)
                spos = (
                    spos[0] - texture.get_width() / 2,
                    spos[1] - texture.get_height() / 2 + i * 20 - 40
                )
                screen.blit(texture, spos)
