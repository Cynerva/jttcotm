import pygame
from time import time

from game import Game
from config import screen_size, screen_width, screen_height


def main():
    pygame.init()
    screen = pygame.display.set_mode((screen_width * 2, screen_height * 2))
    surface = pygame.Surface(screen_size)
    game = Game()

    last_time = time()
    while True:
        next_time = time()

        game.update(delta=next_time - last_time)
        surface.fill((0, 0, 0)) # TODO: consider removing this
        game.render(surface)
        pygame.transform.scale2x(surface, screen)
        pygame.display.flip()

        last_time = next_time


if __name__ == "__main__":
    main()
