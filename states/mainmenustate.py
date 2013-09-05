import sys
import pygame
from pygame.locals import *

from states import StateChange, MainGameState, WorldGenState
from config import screen_width


MENU_ENTRIES = [
    "New game",
    "Generate world",
    "Exit"
]


class MainMenuState(object):
    def __init__(self):
        self.font = pygame.font.Font(None, 16)
        self.selected = 0

    def update(self, delta):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_w:
                    self.selected -= 1
                elif event.key == K_s:
                    self.selected += 1
                elif event.key == K_RETURN:
                    if self.selected == 0:
                        raise StateChange(MainGameState())
                    elif self.selected == 1:
                        raise StateChange(WorldGenState())
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
