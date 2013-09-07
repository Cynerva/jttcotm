import sys
import pygame
from pygame.locals import *

import states
from config import screen_width


MENU_ENTRIES = [
    "Continue",
    "Exit to Main Menu"
]


class PauseMenuState(object):
    def __init__(self, parent):
        self.font = pygame.font.Font("data/fonts/GOODTIME.ttf", 16)
        self.selected = 0
        self.parent = parent

    def update(self, delta):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key in [K_w, K_UP]:
                    self.selected -= 1
                elif event.key in [K_s, K_DOWN]:
                    self.selected += 1
                elif event.key == K_RETURN:
                    if self.selected == 0:
                        raise states.StateChange(self.parent)
                    elif self.selected == 1:
                        raise states.StateChange(states.MainMenuState())
            elif event.type == QUIT:
                sys.exit(0)

        self.selected %= len(MENU_ENTRIES)

    def render(self, screen):
        self.parent.render(screen)
        screen.fill((64, 64, 64), special_flags=BLEND_MULT)

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

