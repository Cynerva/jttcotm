import pygame


class TextEvent(object):
    font = None

    def __init__(self, text, pos):
        self.text = text
        self.pos = pos
        self.started = False
        self.time = 0.0

    def update(self, delta, pos):
        if abs(pos[0] - self.pos[0]) + abs(pos[1] - self.pos[1]) < 5.0:
            self.started = True
        if self.started:
            self.time += delta

    def render(self, screen, camera):
        if not TextEvent.font:
            TextEvent.font = pygame.font.Font(None, 16)
        text = self.text[:int(self.time / 0.05)]
        texture = self.font.render(text, 1, (255, 255, 255))
        pos = camera.screen_pos(self.pos)
        pos = (
            pos[0] - texture.get_width() / 2,
            pos[1] - texture.get_height() / 2
        )
        screen.blit(texture, pos)
