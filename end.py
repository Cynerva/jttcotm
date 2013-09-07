import pygame
from pygame.locals import *
from math import sin

import states


class EndEvent(object):
    text = [
        "Ah,  hello there.   Welcome to the center of the moon!",
        "Oh,  me?   I'm just the man in the moon.  I live here.",
        "Don't act so shocked! It's rude you know.",
        "I don't get a lot of visitors down here, what with the moon rabbits.",
        "How did you befriend them?          .          .          .          You did befriend them, didn't you?",
        "I really don't want to have to clean up another set of blood stains.",
        "Hey,   I think I hear them coming.   They must really like you!"
    ]
    texture = None
    font = None

    def __init__(self, pos):
        self.pos = pos
        self.start_time = None
        self.time = 0.0
        self.fade = None

    def update(self, delta, pos, player_pos):
        self.time += delta
        pos = (pos[0] + self.pos[0], pos[1] + self.pos[1])
        distance = abs(player_pos[0] - pos[0]) + abs(player_pos[1] - pos[1])
        if not self.start_time and distance < 5.0:
            self.start_time = self.time
        if self.fade != None:
            self.fade += delta / 4.0
            if self.fade > 1.0:
                raise states.StateChange(states.MainMenuState())
        elif self.start_time:
            count = int((self.time - self.start_time) / 0.05)
            i = 0
            while count > len(EndEvent.text[i]) + 50:
                count -= len(EndEvent.text[i]) + 50
                i += 1
                if i >= len(EndEvent.text):
                    self.fade = 0.0
                    break

    def render(self, screen, camera, pos):
        if not EndEvent.texture:
            EndEvent.texture = pygame.image.load("data/art/maninthemoon.png")
            EndEvent.texture.set_colorkey((255, 0, 255))
        pos = (pos[0] + self.pos[0], pos[1] + self.pos[1])
        spos = (pos[0], pos[1] + sin(self.time * 8) / 8)
        spos = camera.screen_pos(spos)
        spos = (
            spos[0] - EndEvent.texture.get_width() / 2,
            spos[1] - EndEvent.texture.get_height() / 2
        )
        screen.blit(self.texture, spos)

        if self.start_time:
            if not EndEvent.font:
                EndEvent.font = pygame.font.Font("data/fonts/Prototype.ttf", 12)
            count = int((self.time - self.start_time) / 0.05)
            i = 0
            while count > len(EndEvent.text[i]) + 50 and i < len(EndEvent.text) - 1:
                count -= len(EndEvent.text[i]) + 50
                i += 1
            words = EndEvent.text[i][:count].split()
            lines = [""]
            for word in words:
                if len(lines[-1]) > 32:
                    lines.append(word)
                else:
                    lines[-1] += " " + word
            for i in range(len(lines)):
                texture = EndEvent.font.render(lines[i], 1, (255, 255, 255))
                spos = camera.screen_pos(pos)
                spos = (
                    spos[0] - texture.get_width() / 2,
                    spos[1] - texture.get_height() / 2 + i * 20 - 40
                )
                screen.blit(texture, spos)

        if self.fade != None:
            a = 255.0 - self.fade * 255.0
            screen.fill((a, a, a), special_flags=BLEND_MULT)
