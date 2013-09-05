import pygame
from time import time

from states import MainMenuState, StateChange
from config import screen_size, screen_width, screen_height


def main():
    pygame.init()
    screen = pygame.display.set_mode((screen_width * 2, screen_height * 2))
    surface = pygame.Surface(screen_size)
    state = MainMenuState()

    last_time = time()
    while True:
        next_time = time()

        try:
            state.update(delta=next_time - last_time)
        except StateChange as change:
            state = change.state

        surface.fill((0, 0, 0)) # TODO: consider removing this
        state.render(surface)
        pygame.transform.scale2x(surface, screen)
        pygame.display.flip()

        last_time = next_time


if __name__ == "__main__":
    main()
