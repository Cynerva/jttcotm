import pygame
from Box2D import *

from debug import draw_body


class Player(object):
    def __init__(self, world, pos=(0, 0)):
        self.body = world.CreateDynamicBody(position=pos)
        self.body.CreatePolygonFixture(box=(8, 16), density=1, friction=0.3)
        self.sensor = self.body.CreatePolygonFixture(
            box=(7.9, 2, (0, -16), 0),
            density=1,
            friction=0.3,
            isSensor = True
        )
        self.body.angle = 3.14

    def update(self, delta):
        self.body.angle -= self.body.angle*delta * 8.0

    def render(self, screen, camera):
        draw_body(self.body, screen, camera)
