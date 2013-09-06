from threading import Thread
from time import time, sleep

import pygame


def play(filename):
    def start():
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.fadeout(2000)
        pygame.mixer.music.load(filename)
        pygame.mixer.music.set_volume(0.0)
        pygame.mixer.music.play(-1)
        start_time = time()
        cur_time = time()
        while cur_time < start_time + 2.0:
            pygame.mixer.music.set_volume((cur_time - start_time) / 2.0)
            cur_time = time()
        pygame.mixer.music.set_volume(2.0)
    thread = Thread(target=start)
    thread.daemon = True
    thread.start()
