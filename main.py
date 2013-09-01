import pygame
from time import time

from game import Game
from config import size


def main():
    pygame.init()
    screen = pygame.display.set_mode(size)
    game = Game()

    last_time = time()
    while True:
        next_time = time()

        game.update(delta=next_time - last_time)
        game.render(screen)

        last_time = next_time


if __name__ == "__main__":
    main()
