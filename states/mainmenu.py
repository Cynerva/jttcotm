import sys
import pygame
from pygame.locals import *

import states
import music
from config import screen_width


MENU_ENTRIES = [
    "Start",
    "Generate world",
    "Exit"
]


class MainMenuState(object):
    def __init__(self):
        self.font = pygame.font.Font("data/fonts/Prototype.ttf", 16)
        self.selected = 0
        music.play("data/music/menu.ogg")

    def update(self, delta):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key in [K_w, K_UP]:
                    self.selected -= 1
                elif event.key in [K_s, K_DOWN]:
                    self.selected += 1
                elif event.key == K_RETURN:
                    if self.selected == 0:
                        raise states.StateChange(states.MainGameState())
                    elif self.selected == 1:
                        raise states.StateChange(states.SurfaceGenState())
                    elif self.selected == 2:
                        sys.exit(0)
            elif event.type == QUIT:
                sys.exit(0)

        self.selected %= len(MENU_ENTRIES)

    def render(self, screen):
        y = 128
        for i in range(len(MENU_ENTRIES)):
            entry = MENU_ENTRIES[i]
            if self.selected == i:
                texture = self.font.render(entry, 1, (255, 255, 255))
            else:
                texture = self.font.render(entry, 1, (128, 128, 128))
            x = screen_width / 2.0 - texture.get_width() / 2.0
            screen.blit(texture, (x, y))
                
            y += 32
